#!/usr/bin/env python3
"""look: the finishing layer (grain, vignette, bloom, chromatic aberration, grade, letterbox).

Everything here is a heuristic on sampled frames; it describes the OPTICAL
finish, not the UI theme. Dark/light mode, brand colours and palette are
deliberately not reported (a recreation should keep its own product's theme).

  grain      Immerkaer noise sigma (8-bit levels) measured only on flat pixels
  vignette   corner/centre luma ratio of the per-pixel MEDIAN frame (content averages out)
  bloom      glow ratio: luma just outside highlights vs further out
  chroma     R/B channel misregistration in corner vs centre patches (px)
  grade      black/white points, contrast, saturation, warm/cool bias
  letterbox  black bars (active picture area)

usage: look.py video.mp4 [-o look.json] [--samples 40]
"""
import argparse
import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import dump, iter_frames, probe, r  # noqa: E402

NK = np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]], np.float32)


def grain_sigma(g):
    g = g.astype(np.float32)
    conv = np.abs(cv2.filter2D(g, -1, NK))
    gx = cv2.Sobel(cv2.GaussianBlur(g, (0, 0), 1.5), cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(cv2.GaussianBlur(g, (0, 0), 1.5), cv2.CV_32F, 0, 1)
    flat = np.hypot(gx, gy) < 12
    flat = cv2.erode(flat.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    lum = cv2.GaussianBlur(g, (0, 0), 3)
    flat &= (lum > 12) & (lum < 243)  # clipped pixels hide grain
    if flat.mean() < 0.02:
        return None
    return float(math.sqrt(math.pi / 2) / 6 * conv[flat].mean())


def ca_shift(bgr):
    h, w = bgr.shape[:2]
    p = min(h, w) // 5
    def shift(y, x):
        b = bgr[y:y + p, x:x + p, 0].astype(np.float32)
        rr = bgr[y:y + p, x:x + p, 2].astype(np.float32)
        if b.std() < 8 or rr.std() < 8:
            return None
        b = b - cv2.GaussianBlur(b, (0, 0), 3)
        rr = rr - cv2.GaussianBlur(rr, (0, 0), 3)
        win = cv2.createHanningWindow((p, p), cv2.CV_32F)
        (dx, dy), resp = cv2.phaseCorrelate(b, rr, win)
        return math.hypot(dx, dy) if resp > 0.05 else None
    corners = [shift(0, 0), shift(0, w - p), shift(h - p, 0), shift(h - p, w - p)]
    centre = shift(h // 2 - p // 2, w // 2 - p // 2)
    cs = [c for c in corners if c is not None]
    return (float(np.median(cs)) if cs else None), centre


def bloom_ratio(g):
    g = g.astype(np.float32)
    hi = (g > 235).astype(np.uint8)
    if hi.mean() < 0.0005 or hi.mean() > 0.5:
        return None
    d1 = cv2.dilate(hi, np.ones((9, 9), np.uint8)) - hi
    d2 = cv2.dilate(hi, np.ones((41, 41), np.uint8)) - cv2.dilate(hi, np.ones((25, 25), np.uint8))
    if d1.sum() < 50 or d2.sum() < 50:
        return None
    return float(g[d1 > 0].mean() / (g[d2 > 0].mean() + 1e-3))


def analyze(path, samples=40):
    info = probe(path)
    n = max(1, info["frames"])
    pick = set(np.linspace(0, n - 1, min(samples, n)).astype(int).tolist())
    grains, cas, cents, blooms, smalls, stats = [], [], [], [], [], []
    for i, f in iter_frames(path, width=min(1920, info["width"]), gray=False):
        if i not in pick:
            continue
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        gs = grain_sigma(g)
        if gs is not None:
            grains.append(gs)
        c, cc = ca_shift(f)
        if c is not None:
            cas.append(c)
        if cc is not None:
            cents.append(cc)
        b = bloom_ratio(g)
        if b is not None:
            blooms.append(b)
        smalls.append(cv2.resize(f, (320, int(320 * f.shape[0] / f.shape[1])), interpolation=cv2.INTER_AREA))
        hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
        stats.append((np.percentile(g, 1), np.percentile(g, 99), np.percentile(g, 95) - np.percentile(g, 5),
                      hsv[..., 1].mean() / 255, float(f[..., 2].mean()) - float(f[..., 0].mean())))
    medf = np.median(np.array(smalls), axis=0).astype(np.float32)
    lum = cv2.cvtColor(medf.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    # letterbox: rows/cols that are near-black in the median frame
    h, w = lum.shape
    top = int(np.sum(np.cumprod((lum.mean(1) < 8)[:h // 3])))
    bot = int(np.sum(np.cumprod((lum.mean(1) < 8)[::-1][:h // 3])))
    lef = int(np.sum(np.cumprod((lum.mean(0) < 8)[:w // 3])))
    rig = int(np.sum(np.cumprod((lum.mean(0) < 8)[::-1][:w // 3])))
    act = lum[top:h - bot or h, lef:w - rig or w]
    ah, aw = act.shape
    yy, xx = np.mgrid[0:ah, 0:aw]
    rr = np.hypot((xx - aw / 2) / (aw / 2), (yy - ah / 2) / (ah / 2)) / math.sqrt(2)
    centre = float(np.median(act[rr < 0.3]))
    corner = float(np.median(act[rr > 0.85]))
    prof = [r(float(np.median(act[(rr >= a) & (rr < a + 0.2)])) / (centre + 1e-6), 3) for a in (0, .2, .4, .6, .8)]
    falloff = 1 - corner / (centre + 1e-6)
    st = np.array(stats)
    gs = float(np.median(grains)) if grains else None
    bl = float(np.median(blooms)) if blooms else None
    ca = float(np.median(cas)) if cas else None
    cac = float(np.median(cents)) if cents else None
    res = {
        "grain": {"sigma_8bit": r(gs, 2),
                  "label": None if gs is None else ("none/clean" if gs < 0.8 else ("fine" if gs < 2.5 else ("medium" if gs < 5 else "heavy"))),
                  "note": "codec denoising lowers this; treat < 1.0 on heavily compressed sources as unknown"},
        "vignette": {"corner_falloff": r(falloff, 3), "radial_profile": prof,
                     "label": "none" if falloff < 0.08 else ("subtle" if falloff < 0.2 else ("medium" if falloff < 0.35 else "strong")),
                     "note": "content-dependent: verify on the contact sheet when the UI itself is darker at the edges"},
        "bloom": {"glow_ratio": r(bl, 3), "label": None if bl is None else ("likely" if bl > 1.25 else ("subtle" if bl > 1.1 else "none"))},
        "chromatic_aberration": {"corner_shift_px": r(ca, 2), "centre_shift_px": r(cac, 2),
                                 "label": None if ca is None else ("visible" if ca - (cac or 0) > 1.0 else ("subtle" if ca - (cac or 0) > 0.4 else "none"))},
        "grade": {"black_point": r(np.median(st[:, 0]), 1), "white_point": r(np.median(st[:, 1]), 1),
                  "contrast_p95_p5": r(np.median(st[:, 2]), 1), "saturation": r(np.median(st[:, 3]), 3),
                  "warm_minus_cool": r(np.median(st[:, 4]), 1),
                  "lifted_blacks": bool(np.median(st[:, 0]) > 18), "crushed_whites": bool(np.median(st[:, 1]) >= 254)},
        "letterbox_px_at_320w": {"top": top, "bottom": bot, "left": lef, "right": rig},
        "theme": "ignored on purpose (dark/light mode, palette, brand colours are not part of the audiovisual grammar)",
        "samples": len(smalls),
    }
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("-o", "--out")
    ap.add_argument("--samples", type=int, default=40)
    a = ap.parse_args(argv)
    res = analyze(a.video, a.samples)
    if a.out:
        dump(res, a.out)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
