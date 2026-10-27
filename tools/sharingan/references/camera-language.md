# Camera language, measured

How video-sharingan turns "the camera slowly glides over the UI" into numbers, plus
the traps we hit on real launch videos.

## Conventions

| quantity | definition | unit |
|---|---|---|
| content velocity `vx, vy` | translation of the **frame centre** between frames, from a RANSAC similarity fit | px/s, native |
| `center_speed_px_s_1080p` | ‖v‖ rescaled to a 1920×1080 diagonal so mobile/desktop/4K compare | px/s |
| `%W/s` | speed / frame width × 100 (1080p: 19.2 px/s = 1 %W/s) | %/s |
| `scale_pct_s` | growth of on-screen scale per second, `((1+s½)^(1/0.5) − 1)·100` from 0.5 s windows | %/s |
| `motion_px_s_1080p` | mean displacement of a 9×5 grid of points (zoom-aware: catches pure push-ins) | px/s |
| `rotation_deg_s` | in-plane rotation (roll) | °/s |
| `perspective_drift` | median keystone of 1 s homographies (corner disagreement vs best affine / diagonal) | fraction |

**Sign:** content sliding **left** (`vx < 0`) means the camera trucks **right**. Content sliding **down**
(`vy > 0`) means the camera pedestals **up**. Scale growing means push-in.

## Move vocabulary

| label | signal |
|---|---|
| `static` | grid motion < stop threshold (default 2 px/s @1080p) everywhere |
| `truck-left/right` | horizontal centre translation ≥ 25 % of speed, no perspective change |
| `pedestal-up/down` | vertical centre translation ≥ 25 % of speed, no perspective change |
| `pan-*` / `tilt-*` | same as truck/pedestal **with** perspective change (`perspective_drift` > 0.01 per s, ≈ a 3°/s rotation) |
| `push-in` / `pull-out` | scale rate > +0.25 %/s / < −0.25 %/s |
| `roll-cw/ccw` | |rotation| > 0.5 °/s |
| `orbit` | perspective change while the centre barely translates |

Combined moves are joined with `+` (e.g. `truck-right+pedestal-up+push-in`). On a flat screen recording,
truck and pan are mathematically the same 2D motion. They only separate when perspective visibly changes.

## Easing

The per-frame grid motion is integrated into a 0→1 progress curve and fitted (RMSE) against
`linear`, `power1–3.in/out/inOut` and `sine.inOut` (GSAP names; the brief also gives the CSS
cubic-bézier). Caveat: references usually **cut mid-move**, so a shot can be a slice of a longer
eased move. Check `speed_thirds_rel` (relative speed in each third of the shot): a slice of an
ease-in-out looks like a gentle ramp, not a full S-curve.

## "Never stops"

A shot passes when no frame's smoothed grid motion falls below the stop threshold **and** the slowest frame
is ≥ 25 % of the shot's median (so an ease that decelerates to almost nothing also fails). `enters_moving`
and `exits_moving` tell you whether the editor cut in/out mid-move.

## Pull-out detection

Per-frame scale is too noisy (and biased) for slow zooms, so scale is measured **directly between frames
0.5 s apart**. A shot is flagged when its total scale change is < −0.5 %, or when ≥ 3 windows read < −0.3 %.
Windows that overlap a detected UI event are reported as `reflow_suspect_at_s` and not counted (see below).

## Traps we hit in production (and the fix that's now built in)

1. **UI reflow looks like a cut.** A list collapsing after a filter changes a third of the frame in one frame.
   Pixel and histogram detectors fire. Fix: a candidate is a cut only if the camera **trajectory** breaks: the
   motion before equals the motion after, and features that didn't change still land where that motion
   predicts. Across a real cut, zero features do.
2. **UI reflow looks like a pull-out.** Rows sliding up shrink the fitted similarity for a few windows
   (−0.6 to −1.0 % per 0.5 s). Fix: windows overlapping a UI event are reported separately.
3. **Per-frame scale is biased.** At about 0.06 % per frame, per-frame RANSAC fits over-read push-ins by 5–10 %. Fix:
   rates come from 0.5 s window fits, which match synthetic ground truth to about 0.01 %/s.
4. **Shallow DOF hides features.** Trackers lock onto the sharp band, which is what you want (it's the
   subject), but very soft shots can go `untracked`. Lower `--track-width` noise or set cuts manually.
5. **Mobile vs desktop speeds.** A mobile reference at 21 px/s and a desktop one at 53 px/s can both be
   "slow". Compare in %W/s or at the 1080p-equivalent, never in raw px.
6. **Cross-check with a second tracker.** `--method orb` is independent of LK. If they disagree by more than about 5 %,
   look at the shot by eye before trusting either.

## Focus and framing

Sharpness per grid cell is estimated as a **blur sigma** from the ratio of edge-gradient peaks at two
smoothing scales, so a cell full of text and a cell with one sharp line read the same. Raw Laplacian
variance would mostly measure how much text there is. Framing comes from the median height of sharp
UI elements (glyphs): macro ≥ 3.5 % of frame height, medium 1.6–3.5 %, wide < 1.6 %.
