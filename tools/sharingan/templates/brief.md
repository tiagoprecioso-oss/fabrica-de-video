# Recreation brief: <reference name>

<!--
video-sharingan brief template. `sharingan analyze` fills most of this automatically
(brief.md); use this file when writing or editing a brief by hand.

Rules of the format (after Hyperframes' "Recreating something you saw"):
  * transcribe MOTION, not just composition: durations, camera path, what moves when
  * every value is an ABSOLUTE target ("push-in +1.2 %/s"), never a relative nudge ("zoom a bit more")
  * the distilled spec at the top must be paste-able into a generator on its own
  * discrete facts (timings, counts, rates) transfer losslessly; continuous qualities
    (bloom falloff, grain feel) get a number AND a short perceptual note
-->

> **Distilled spec:** <N> s <W>x<H> at <fps> fps, <k> shots (<min>–<max> s, mean <asl> s) joined by 0-frame hard cuts.
> Camera: <linear / eased>, <never stops / holds>, <a>–<b> px/s of on-screen motion at 1080p (<p>–<q> %W/s),
> push-in <x>–<y> %/s, <never pulls out / pulls out in shots …>. Optics: <deep / tilt-shift band>, grain <…>,
> vignette <…>. Audio: <music / sfx-only / silent> at <bpm> BPM; cuts <on / off> the beat; SFX <on UI events / none>.

## 0. Scope

- Copy the **audiovisual grammar**: camera, optics, edit, pacing, sound.
- **Ignore** theme (dark/light mode), palette, typography, branding, the reference's content and copy.
- Motion = **content motion on screen** at 1080p-equivalent px. The camera moves the opposite way.

## 1. Global specs

| | |
|---|---|
| Format | <W>×<H> (<orientation>), <fps> fps |
| Duration | <s> s |
| Shots | <k> · ASL <s> · range <min>–<max> s · <cuts/min> cuts/min |
| Transitions | <hard cuts only / dissolves at …> |
| End | <cut to black / static end card <s> s / none> |
| Audio | <class>, <bpm> BPM |

## 2. Camera rules

- **Golden rule:** <one sentence, e.g. "linear and continuous: the camera never stops and never pulls back">
- **Speed window:** <a>–<b> px/s at 1080p (<p>–<q> %W/s), median <m>; speed cv ≤ <cv> inside a shot.
- **Scale:** push-in +<x> to +<y> %/s (+<x/2>…<y/2> % per 0.5 s); pull-out <never / shots …>.
- **Easing:** <linear (GSAP `ease: "none"`) / power2.inOut …> on the camera.
- **Never stops:** <yes/no>; slowest frame ≥ <v> px/s; shots enter moving and are cut mid-move: <yes/no>.
- **One move per shot:** <truck / pedestal / push-in / combos>, no whip / orbit / roll / shake unless listed.

## 3. Framing & staging

- Sequence: <macro → medium → wide …>; wider framings arrive <by cut / by pull-out>.
- Sharp element height <min>–<max> % of frame height (macro ≥ 3.5 %, wide < 1.6 %).
- Staging: <flat screen recording / UI on a tilted 3D plane (pitch …°, yaw …°) / device mockup>.

## 4. Optics & look

- DOF: <deep / tilt-shift band (orientation, angle, sharp ≈ x % of frame)>; focus <locked / rack at t=…>.
- Grain <σ … 8-bit levels>, vignette <corners ≈ x % of centre>, bloom <…>, chromatic aberration <…>.
- Perceptual note: <one line on what it should *feel* like>.

## 5. Editing & pacing

- Shot durations: <list>. Cut rhythm: <regular / accelerating / on the beat>.
- Open with <…>, build to <…>, close with <…>.

## 6. UI action vs camera

- UI micro-animations: <count> at <times>; each lands in <n> frames.
- The contrast: <slow ambient lens vs fast precise UI>. The UI acts on its own; no cursor unless <…>.

## 7. Audio

- <music bed: tempo, feel> · <SFX: which, synced to what, tolerance>.
- Cuts vs beat: <on beat x % / not synced>. Nothing on the cuts unless <…>.

## 8. Shot table

| # | in → out | dur | move | speed px/s (1080p) | scale %/s | ease | never stops | framing | DOF | UI action | audio |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 00:00.00 → 00:00.00 | | | | | | | | | | |

## 9. Do

- ✅ <absolute, testable rule>

## 10. Don't

- ❌ <absolute, testable rule>

## 11. Self-check (QC gates)

Render → `sharingan analyze render.mp4 -o render-analysis` → `sharingan compare ref/analysis.json render-analysis/analysis.json`.

- [ ] camera speed per moving shot inside <a·0.85>–<b·1.15> px/s
- [ ] `frames_below_stop == 0` in every shot
- [ ] no 0.5 s window with scale < −0.3 % (reflow-suspect windows reviewed by eye)
- [ ] shot durations inside <…>; cuts are 0-frame
- [ ] contact sheet reviewed: no dissolve, flash frame or important element cropped at the end of a push-in

## 12. Deviations from the reference

| what | reference | ours | why |
|---|---|---|---|
| | | | |
