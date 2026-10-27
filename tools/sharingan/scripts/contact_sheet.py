#!/usr/bin/env python3
"""contact_sheet: images an agent (or a human) can actually read.

  overview.png  ~N evenly spaced frames, labelled with timecode / frame / shot
  shots.png     one row per shot: first, 25%, 50%, 75%, last frame + measured move

Pure OpenCV (no drawtext/fontconfig dependency). Read these BEFORE trusting the
numbers: they are how you catch a dissolve, a whip, a flash frame or a false cut.

usage: contact_sheet.py video.mp4 [--shots shots.json] [--camera camera.json] [-d outdir]
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import iter_frames, load, probe, shot_of, tc  # noqa: E402

TW = 320


def label(img, text, y=18, scale=0.45):
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, 1)
    cv2.rectangle(img, (2, y - h - 5), (min(img.shape[1] - 1, 10 + w), y + 5), (20, 20, 20), -1)
    cv2.putText(img, text, (6, y), cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), 1, cv2.LINE_AA)


def build(path, shots_doc=None, camera=None, outdir=".", tiles=35, cols=7):
    info = probe(path)
    fps, n = info["fps"], info["frames"]
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    over_idx = list(np.linspace(0, max(0, n - 1), min(tiles, n)).astype(int))
    shots = shots_doc["shots"] if shots_doc else [{"index": 1, "start_frame": 0, "end_frame": n, "dur_s": n / fps}]
    shot_idx = {}
    for s in shots:
        a, b = s["start_frame"], s["end_frame"] - 1
        for q, k in enumerate(np.linspace(a, b, 5).astype(int)):
            shot_idx.setdefault(int(k), []).append((s["index"], q))
    want = set(over_idx) | set(shot_idx)
    grab = {}
    for i, f in iter_frames(path, width=TW, gray=False):
        if i in want:
            grab[i] = f
    if not grab:
        raise SystemExit("[sharingan] no frames decoded")
    th = next(iter(grab.values())).shape[0]
    cam = {c["index"]: c for c in (camera or {}).get("shots", [])}
    # overview
    tilesimg = []
    for i in over_idx:
        im = grab.get(i, np.zeros((th, TW, 3), np.uint8)).copy()
        label(im, f"{tc(i / fps)}  f{i}  s{shot_of(i, shots)}")
        tilesimg.append(im)
    while len(tilesimg) % cols:
        tilesimg.append(np.zeros_like(tilesimg[0]))
    rows = [np.hstack(tilesimg[k:k + cols]) for k in range(0, len(tilesimg), cols)]
    cv2.imwrite(str(out / "overview.png"), np.vstack(rows))
    # per-shot strips
    strips = []
    for s in shots:
        a, b = s["start_frame"], s["end_frame"] - 1
        ims = []
        for q, k in enumerate(np.linspace(a, b, 5).astype(int)):
            im = grab.get(int(k), np.zeros((th, TW, 3), np.uint8)).copy()
            label(im, f"{tc(k / fps)} f{k}")
            ims.append(im)
        head = np.full((26, TW * 5, 3), 30, np.uint8)
        c = cam.get(s["index"], {})
        mv = c.get("move", "")
        extra = ""
        if c.get("center_speed_px_s") is not None:
            extra = f"  {c['center_speed_px_s']} px/s  scale {c.get('scale_pct_s')} %/s  ease {(c.get('ease') or {}).get('best')}"
        label(head, f"SHOT {s['index']}  {tc(s['start_frame'] / fps)}-{tc(s['end_frame'] / fps)}  ({s['dur_s']}s)  {mv}{extra}", y=18, scale=0.5)
        strips.append(np.vstack([head, np.hstack(ims)]))
    cv2.imwrite(str(out / "shots.png"), np.vstack(strips))
    return {"overview": str(out / "overview.png"), "shots": str(out / "shots.png")}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--shots")
    ap.add_argument("--camera")
    ap.add_argument("-d", "--dir", default=".")
    ap.add_argument("--tiles", type=int, default=35)
    a = ap.parse_args(argv)
    print(build(a.video, load(a.shots) if a.shots else None, load(a.camera) if a.camera else None, a.dir, a.tiles))


if __name__ == "__main__":
    main()
