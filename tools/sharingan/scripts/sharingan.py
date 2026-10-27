#!/usr/bin/env python3
"""video-sharingan: copy the technique, not the pixels.

  sharingan analyze ref.mp4 [-o out/]          full pipeline -> analysis.json + brief.md + sheets
  sharingan probe|cuts|sheet|camera|focus|look|audio ...   individual steps
  sharingan brief out/analysis.json            re-render the brief
  sharingan compare ref/analysis.json render/analysis.json   QC gates (exit 1 on failure)
"""
import argparse
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import audio as audio_mod  # noqa: E402
import brief as brief_mod  # noqa: E402
import camera_track  # noqa: E402
import compare as compare_mod  # noqa: E402
import contact_sheet  # noqa: E402
import cuts as cuts_mod  # noqa: E402
import focus_map  # noqa: E402
import look as look_mod  # noqa: E402
import probe as probe_mod  # noqa: E402
from common import VERSION, dump, probe  # noqa: E402

EYE = r"""
      .-~~~-.
    /  .-.-.  \     video-sharingan v{v}
   |  ( (@) )  |    copy the technique, not the pixels
    \  '-'-'  /
      '-~~~-'
"""


def analyze(video, out, method="lk", stop=2.0, cut_method="auto", manual_cuts=None, title=None, skip_audio=False):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    def step(msg):
        print(f"[{time.time() - t0:6.1f}s] {msg}", flush=True)

    step("probe")
    info = probe(video)
    step(f"cuts ({info['frames']} frames @ {info['fps']} fps)")
    shots = cuts_mod.detect(video, cut_method, manual=manual_cuts)
    dump(shots, out / "parts" / "shots.json")
    step(f"camera tracking ({len(shots['shots'])} shots, {method})")
    cam = camera_track.track(video, shots, method=method, stop_thr=stop)
    dump(cam, out / "parts" / "camera.json")
    step("focus / framing")
    foc = focus_map.analyze(video, shots, cam, png_dir=out / "focus")
    dump(foc, out / "parts" / "focus.json")
    step("look")
    lk = look_mod.analyze(video)
    dump(lk, out / "parts" / "look.json")
    au = None
    if not skip_audio:
        step("audio")
        au = audio_mod.analyze(video, shots, cam)
        dump(au, out / "parts" / "audio.json")
    step("contact sheets")
    contact_sheet.build(video, shots, cam, out / "sheets")
    analysis = {
        "tool": "video-sharingan", "version": VERSION,
        "source": info,
        "edit": {k: shots[k] for k in ("cuts", "shots", "stats", "transition_note")},
        "camera": cam, "focus": foc, "look": lk, "audio": au,
        "artifacts": {"overview": "sheets/overview.png", "shots": "sheets/shots.png", "focus": "focus/"},
    }
    dump(analysis, out / "analysis.json")
    (out / "brief.md").write_text(brief_mod.render(analysis, title))
    step(f"done -> {out / 'analysis.json'} + {out / 'brief.md'}")
    return analysis


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(EYE.format(v=VERSION))
        print(__doc__)
        return
    cmd, rest = argv[0], argv[1:]
    sub = {"probe": probe_mod.main, "cuts": cuts_mod.main, "sheet": contact_sheet.main, "camera": camera_track.main,
           "focus": focus_map.main, "look": look_mod.main, "audio": audio_mod.main, "brief": brief_mod.main,
           "compare": compare_mod.main}
    if cmd in sub:
        return sub[cmd](rest)
    if cmd != "analyze":
        raise SystemExit(f"unknown command {cmd!r}; try: analyze, {', '.join(sub)}")
    ap = argparse.ArgumentParser(prog="sharingan analyze")
    ap.add_argument("video")
    ap.add_argument("-o", "--out", help="output dir (default: sharingan-<video stem>)")
    ap.add_argument("--method", default="lk", choices=["lk", "orb"], help="feature tracker")
    ap.add_argument("--stop", type=float, default=2.0, help="'stopped' threshold in 1080p px/s")
    ap.add_argument("--cut-method", default="auto", choices=["auto", "ffmpeg", "threshold"])
    ap.add_argument("--cuts", help="manual cut times (s), comma separated: overrides detection")
    ap.add_argument("--title")
    ap.add_argument("--no-audio", action="store_true")
    a = ap.parse_args(rest)
    print(EYE.format(v=VERSION))
    manual = None
    if a.cuts:
        fps = probe(a.video)["fps"]
        manual = [int(round(float(x) * fps)) for x in a.cuts.split(",") if x.strip()]
    out = a.out or f"sharingan-{Path(a.video).stem}"
    analyze(a.video, out, a.method, a.stop, a.cut_method, manual, a.title, a.no_audio)


if __name__ == "__main__":
    main()
