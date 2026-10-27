#!/usr/bin/env python3
"""brief: turn analysis.json into a recreation brief (markdown) + do/don't rules.

The brief follows the Hyperframes "recreating references" advice: transcribe
motion (not just composition), state every value as an ABSOLUTE target, and
distil the constants into a paste-able spec paragraph.

usage: brief.py analysis.json [-o brief.md] [--title "..."]
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import load, tc  # noqa: E402


def fmt(x, unit="", nd=1):
    if x is None:
        return "n/a"
    if isinstance(x, float):
        x = round(x, nd)
    return f"{x}{unit}"


def rng(lo, hi, unit="", nd=1):
    if lo is None or hi is None:
        return "n/a"
    if round(lo, nd) == round(hi, nd):
        return fmt(lo, unit, nd)
    return f"{fmt(lo, '', nd)}–{fmt(hi, unit, nd)}"


def derive(a):
    """Compute the numbers the brief and the rules share."""
    cam = a["camera"]
    shots = cam["shots"]
    moving = [s for s in shots if s.get("move") not in ("static", "untracked", "drift")]
    trans = [s for s in moving if (s.get("center_speed_px_s_1080p") or 0) >= 2]
    lin = lambda s: (s.get("ease") or {}).get("best") == "linear"  # noqa: E731
    # linear shots: steady speed; eased shots: average speed over the shot (the peak is not a target)
    sp = [s["center_speed_px_s_1080p"] if lin(s) else s.get("mean_speed_px_s_1080p") or s["center_speed_px_s_1080p"] for s in trans]
    pw = [x / 19.2 for x in sp]
    push = [s["scale_pct_s"] for s in shots if (s.get("scale_pct_s") or 0) > 0.25]
    pulls = [s for s in shots if (s.get("pull_out") or {}).get("detected")]
    p5 = [s["motion_px_s_1080p"]["p5"] for s in moving if s.get("motion_px_s_1080p")]
    eases = Counter((s.get("ease") or {}).get("best") for s in moving if s.get("ease"))
    cvs = [s["speed_cv"] for s in trans if s.get("speed_cv") is not None and lin(s)]
    durs = [s["dur_s"] for s in a["edit"]["shots"]]
    return dict(shots=shots, moving=moving, sp=sp, pw=pw, push=push, pulls=pulls, p5=p5, eases=eases, cvs=cvs,
                durs=durs, static=[s for s in shots if s.get("move") == "static"],
                rolls=[s for s in shots if "roll" in (s.get("move") or "")],
                shake=max([s.get("shake_px") or 0 for s in shots] or [0]),
                cut_moving=all(s.get("exits_moving") for s in moving[:-1]) if len(moving) > 1 else None,
                never=cam["summary"].get("camera_never_stops"))


def rules(a, d):
    do, dont = [], []
    au = a.get("audio") or {}
    lk = a.get("look") or {}
    fo = a.get("focus") or {}
    if d["sp"]:
        do.append(f"Move the camera at {rng(min(d['sp']), max(d['sp']), ' px/s')} at 1080p "
                  f"({rng(min(d['pw']), max(d['pw']), ' %W/s', 2)}) of on-screen subject motion; median {fmt(sorted(d['sp'])[len(d['sp']) // 2], ' px/s')}.")
    if d["eases"] and set(d["eases"]) == {"linear"}:
        do.append("Tween every camera move linearly (GSAP `ease: \"none\"`, CSS `linear`). Constant velocity inside a shot"
                  + (f" (speed cv ≤ {max(d['cvs']):.2f})." if d["cvs"] else "."))
        dont.append("No ease-in/ease-out on the camera. Easing belongs to the UI micro-animations, not the lens.")
    elif d["eases"]:
        do.append("Camera easing per shot: " + ", ".join(f"{k} ×{v}" for k, v in d["eases"].items()) + " (see shot table).")
    if d["never"]:
        do.append(f"The camera never stops: every frame moves (slowest frame ≥ {fmt(min(d['p5']), ' px/s')} at 1080p). Shots start already moving.")
        dont.append("No holds, no settle at the end of a move, no static frames.")
    elif d["static"]:
        do.append(f"Static shots exist ({', '.join(str(s['index']) for s in d['static'])}); keep them locked off, no drift.")
    if d["cut_moving"]:
        do.append("Cut while the camera is still moving (hard cut mid-move).")
    if d["push"]:
        do.append(f"Push-ins at {rng(min(d['push']), max(d['push']), ' %/s', 2)} of scale (absolute: {rng(min(d['push']) / 2, max(d['push']) / 2, '', 2)} % per 0.5 s).")
    if not d["pulls"]:
        dont.append("Never pull out / zoom out. Scale only grows within a shot; a wider framing arrives only through a cut.")
    if a["edit"]["stats"]["cut_count"] and "dissolve" not in (a["edit"].get("transition_note") or ""):
        dont.append("No dissolves, whip pans, blur or zoom transitions: 0-frame hard cuts only (verify on the contact sheet).")
    if not d["rolls"]:
        dont.append("No roll / dutch angle and no orbit unless the shot table says so.")
    if d["shake"] < 0.3:
        dont.append("No handheld shake or camera noise: the move is mathematically smooth.")
    dofs = Counter(s.get("dof") for s in fo.get("shots", []))
    if dofs.get("shallow-band"):
        bands = [s["band"]["orientation"] for s in fo["shots"] if s.get("band")]
        do.append(f"Shallow depth of field as a {Counter(bands).most_common(1)[0][0]} tilt-shift band in "
                  f"{dofs['shallow-band']}/{len(fo['shots'])} shots (see shot table); keep the subject inside the sharp band.")
    if fo.get("summary", {}).get("any_rack_focus") is False and fo.get("shots"):
        dont.append("No rack focus (none detected): the sharp region never jumps to a new subject mid-shot.")
    g = (lk.get("grain") or {}).get("label")
    if g in ("fine", "medium", "heavy"):
        do.append(f"Film grain: {g} (σ≈{lk['grain']['sigma_8bit']} 8-bit levels after compression; render ~1.3× that).")
    v = lk.get("vignette") or {}
    if v.get("label") in ("subtle", "medium", "strong"):
        do.append(f"Vignette: {v['label']} (corners ≈{round((1 - v['corner_falloff']) * 100)}% of centre luminance).")
    if (lk.get("bloom") or {}).get("label") in ("likely", "subtle"):
        do.append("Soft bloom/halation on bright UI elements.")
    if (lk.get("chromatic_aberration") or {}).get("label") in ("visible", "subtle"):
        do.append("Very subtle chromatic aberration toward the corners only.")
    cls = au.get("class")
    if cls == "silent":
        do.append("No audio track.")
    elif cls:
        cuts = (au.get("cuts") or {})
        if cls.startswith("music"):
            do.append(f"Music bed at {fmt(au.get('tempo_bpm'), ' BPM', 0)}.")
        if cuts.get("verdict", "").startswith("cuts are cut to the music"):
            do.append(f"Cut on the beat ({round(cuts['on_beat_fraction'] * 100)}% of cuts within ±{cuts['tolerance_ms']} ms of a beat).")
        elif cuts.get("verdict") == "cuts are not synced to audio":
            dont.append("Don't put whooshes or hits on the cuts; cuts are not driven by the audio.")
        ue = au.get("ui_events") or {}
        if ue.get("synced_fraction") and ue["synced_fraction"] >= 0.5 and ue["synced_fraction"] > 2 * (ue.get("chance") or 0):
            do.append(f"Sync a short SFX (tick/click/type) to UI state changes ({round(ue['synced_fraction'] * 100)}% land within one frame).")
    ui = a["camera"].get("ui_events") or []
    if ui:
        do.append(f"Let the UI act on its own: {len(ui)} real micro-animations/state changes under a slow camera; the contrast is the style.")
    dont.append("Don't copy the reference's theme, palette or branding. Keep your own product's UI; copy the grammar.")
    return do, dont


def _spd(s):
    if (s.get("ease") or {}).get("best") not in (None, "linear"):
        return s.get("mean_speed_px_s_1080p")
    return s.get("center_speed_px_s_1080p")


def render(a, title=None):
    src = a["source"]
    ed = a["edit"]
    d = derive(a)
    do, dont = rules(a, d)
    fo = {s["index"]: s for s in (a.get("focus") or {}).get("shots", [])}
    au = a.get("audio") or {}
    lk = a.get("look") or {}
    st = ed["stats"]
    title = title or src["file"]
    L = []
    w = L.append
    # ---- distilled spec paragraph
    parts = [f"{src['duration_s']} s {src['width']}x{src['height']} at {round(src['fps'], 3)} fps, {st['shot_count']} shots "
             f"({rng(min(d['durs']), max(d['durs']), ' s', 2)}, mean {st['asl_s']} s) joined by hard cuts."]
    if d["sp"]:
        parts.append(f"Camera: {('linear, ' if set(d['eases']) == {'linear'} else '')}"
                     f"{'never stops, ' if d['never'] else ''}{rng(min(d['sp']), max(d['sp']), ' px/s')} of on-screen motion at 1080p"
                     + (f", push-in {rng(min(d['push']), max(d['push']), ' %/s', 2)}" if d["push"] else "")
                     + (", never pulls out." if not d["pulls"] else ", includes pull-outs."))
    dof = Counter(s.get("dof") for s in fo.values()).most_common(1)
    if dof:
        parts.append(f"Optics: mostly {dof[0][0]} focus; grain {(lk.get('grain') or {}).get('label')}, vignette {(lk.get('vignette') or {}).get('label')}.")
    if au:
        parts.append(f"Audio: {au.get('class')}" + (f" at {fmt(au.get('tempo_bpm'), ' BPM', 0)}" if au.get("tempo_bpm") else "") + ".")
    w(f"# Recreation brief: {title}\n")
    w(f"> **Distilled spec:** {' '.join(parts)}\n")
    w("Generated by video-sharingan from measurements. Values are absolute targets; re-measure your render "
      "with `sharingan compare` instead of nudging by eye.\n")
    w("## 0. Scope\n")
    w("- Copies the **audiovisual grammar** only: camera, optics, edit, pacing, sound.")
    w("- **Ignores** theme (dark/light mode), palette, typography, branding and the reference's content.")
    w("- Motion is reported as *content motion on screen*; the camera moves the opposite way.\n")
    w("## 1. Global specs\n")
    w("| | |\n|---|---|")
    w(f"| Format | {src['width']}×{src['height']} ({src['orientation']}, {src['aspect']}:1), {round(src['fps'], 3)} fps |")
    w(f"| Duration | {src['duration_s']} s |")
    w(f"| Shots | {st['shot_count']} · ASL {st['asl_s']} s · median {st['median_shot_s']} s · range {st['min_shot_s']}–{st['max_shot_s']} s · {st['cuts_per_min']} cuts/min |")
    w("| Transitions | hard cuts (0 frames) |")
    w(f"| Audio | {au.get('class', 'n/a')}{(', ' + fmt(au.get('tempo_bpm'), ' BPM', 0)) if au.get('tempo_bpm') else ''} |\n")
    w("## 2. Camera rules\n")
    cs = a["camera"]["summary"]
    w(f"- **Speed window:** {rng(min(d['sp']), max(d['sp']), ' px/s') if d['sp'] else 'n/a'} at 1080p-equivalent "
      f"({rng(min(d['pw']), max(d['pw']), ' %W/s', 2) if d['pw'] else 'n/a'}).")
    w(f"- **Scale:** push-in {rng(min(d['push']), max(d['push']), ' %/s', 2) if d['push'] else 'none'}; "
      f"pull-out {'in shots ' + ', '.join(str(s['index']) for s in d['pulls']) if d['pulls'] else 'never'}.")
    w(f"- **Easing:** {', '.join(f'{k} ×{v}' for k, v in d['eases'].items()) or 'n/a'}"
      f"{'; linear shots hold speed cv ≤ ' + format(max(d['cvs']), '.2f') + (' (constant velocity)' if max(d['cvs']) <= 0.2 else '') if d['cvs'] else ''}.")
    w(f"- **Never stops:** {'yes' if d['never'] else 'no'} · slowest frame p5 ≥ {fmt(min(d['p5']) if d['p5'] else None, ' px/s')} · "
      f"cut while moving: {'yes' if d['cut_moving'] else 'no' if d['cut_moving'] is not None else 'n/a'}.")
    w(f"- **Roll / shake:** {'roll in ' + str(len(d['rolls'])) + ' shots' if d['rolls'] else 'no roll'}; max jitter {d['shake']:.2f} px.")
    vocab = Counter(m for s in d["shots"] for m in (s.get("move") or "").split("+") if m)
    w(f"- **Vocabulary:** {', '.join(f'{k} ×{v}' for k, v in vocab.most_common())}.\n")
    w("## 3. Framing & staging\n")
    fr = [fo.get(s["index"], {}).get("framing") for s in d["shots"]]
    w(f"- Framing sequence: {' → '.join(x or '?' for x in fr)}.")
    hs = [fo.get(s["index"], {}).get("element_height_pct_h") for s in d["shots"]]
    hs2 = [h for h in hs if h]
    if hs2:
        w(f"- Sharp UI element height: {min(hs2)}–{max(hs2)} % of frame height (macro ≥ 3.5 %, wide < 1.6 %).")
    w("- Wider framings arrive by **cut**, not by pulling the camera back" if not d["pulls"] else "- Some shots widen by pulling out (see table).")
    w("")
    w("## 4. Optics & look\n")
    for i, s in fo.items():
        band = s.get("band") or {}
        w(f"- Shot {i}: DOF **{s.get('dof')}** (sharp {round((s.get('sharp_fraction') or 0) * 100)}% of frame"
          f"{', ' + band.get('orientation', '') + ' band at ' + str(band.get('angle_deg')) + '°' if band else ''}"
          f"{', rack focus suspected' if s.get('rack_focus_suspected') else ''}).")
    g = lk.get("grain") or {}
    v = lk.get("vignette") or {}
    w(f"- Grain: {g.get('label')} (σ {g.get('sigma_8bit')}). Vignette: {v.get('label')} (corner falloff {v.get('corner_falloff')}). "
      f"Bloom: {(lk.get('bloom') or {}).get('label')}. Chromatic aberration: {(lk.get('chromatic_aberration') or {}).get('label')}.\n")
    w("## 5. Editing & pacing\n")
    w(f"- {st['shot_count']} shots, ASL {st['asl_s']} s; durations: {', '.join(str(x) for x in d['durs'])} s.")
    ui = a["camera"].get("ui_events") or []
    w(f"- UI micro-animations detected: {len(ui)} ({', '.join(tc(e['time_s']) for e in ui[:20])}{' …' if len(ui) > 20 else ''}).")
    if ui and d["sp"]:
        w(f"- Contrast: camera median ≈{sorted(d['sp'])[len(d['sp']) // 2]} px/s vs UI state changes that land within "
          f"{max(e['dur_s'] for e in ui)} s (micro-animations are fast, the lens is not).")
    w("")
    w("## 6. Audio\n")
    if au.get("has_audio") is False or au.get("class") == "silent":
        w("- Silent.\n")
    else:
        w(f"- Class: **{au.get('class')}** · tempo {fmt(au.get('tempo_bpm'), ' BPM', 1)} (beat strength {au.get('beat_strength')}) · "
          f"silence {au.get('silence_fraction')} · peak {au.get('peak_dbfs')} dBFS · RMS {au.get('rms_dbfs')} dBFS.")
        c = au.get("cuts") or {}
        if c:
            w(f"- Cuts: {c.get('verdict')} (on beat {c.get('on_beat_fraction')}, on any onset {c.get('on_onset_fraction')}, chance {c.get('chance_on_onset')}).")
        ue = au.get("ui_events") or {}
        if ue:
            w(f"- UI events with a sound within one frame: {ue.get('synced_fraction')} (chance {ue.get('chance')}).")
        if au.get("off_beat_onsets_s"):
            w(f"- Off-beat accents (likely SFX): {', '.join(str(x) for x in au['off_beat_onsets_s'][:16])} s.")
        w("")
    w("## 7. Shot table\n")
    w("Speed = steady speed for linear shots, average speed for eased shots.\n")
    w("| # | in → out | dur | move | speed px/s (1080p) | %W/s | scale %/s | ease | never stops | framing | DOF | UI events |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for s, e in zip(d["shots"], ed["shots"]):
        f = fo.get(s["index"], {})
        w(f"| {s['index']} | {tc(e['start_s'])} → {tc(e['end_s'])} | {e['dur_s']} | {s.get('move')} | "
          f"{fmt(_spd(s))} | {fmt((_spd(s) or 0) / 19.2, '', 2)} | {fmt(s.get('scale_pct_s'), '', 2)} | "
          f"{(s.get('ease') or {}).get('best', '—')} | {'yes' if s.get('never_stops') else 'no'} | {f.get('framing') or '—'} | "
          f"{f.get('dof') or '—'} | {len(s.get('ui_events') or [])} |")
    w("")
    w("## 8. Do\n")
    for x in do:
        w(f"- ✅ {x}")
    w("\n## 9. Don't\n")
    for x in dont:
        w(f"- ❌ {x}")
    w("\n## 10. Self-check (QC gates for your render)\n")
    w("Render, then run `sharingan analyze render.mp4 -o render-analysis` and "
      "`sharingan compare <this>/analysis.json render-analysis/analysis.json`. Gates:\n")
    if d["sp"]:
        w(f"- [ ] Median camera speed per moving shot inside {rng(min(d['sp']) * 0.85, max(d['sp']) * 1.15, ' px/s')} (1080p).")
    if d["never"]:
        w("- [ ] `frames_below_stop == 0` in every shot (camera never stops).")
    if not d["pulls"]:
        w("- [ ] No 0.5 s window with scale < −0.3 % (no pull-out). Layout reflow can fake one: check those frames by eye.")
    w(f"- [ ] Shot durations within {rng(min(d['durs']) * 0.8, max(d['durs']) * 1.2, ' s', 2)}; cuts are 0-frame.")
    if set(d["eases"]) == {"linear"}:
        w("- [ ] Every moving shot classifies as `linear` ease.")
    w("- [ ] Contact sheet reviewed by eye: no dissolve, no flash frame, nothing important cropped at the end of a push-in.\n")
    w("## 11. Deviations from the reference (fill in)\n")
    w("Fidelity is the default. When you deviate on purpose (e.g. dropping a pull-out the reference has), log it here with the reason, "
      "so the next iteration doesn't \"fix\" it back.\n")
    w("| what | reference | ours | why |\n|---|---|---|---|\n| | | | |\n")
    w("## Provenance\n")
    w(f"- video-sharingan {a.get('version')} · source `{src['file']}` · tracker {cs.get('method')} @ {cs.get('tracking_width')} px · "
      "per-shot rates from direct 0.5 s window fits.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("analysis")
    ap.add_argument("-o", "--out")
    ap.add_argument("--title")
    a = ap.parse_args(argv)
    md = render(load(a.analysis), a.title)
    if a.out:
        Path(a.out).write_text(md)
    else:
        print(md)


if __name__ == "__main__":
    main()
