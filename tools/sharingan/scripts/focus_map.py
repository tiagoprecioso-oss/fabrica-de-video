#!/usr/bin/env python3
"""focus_map: depth of field, focus behaviour and framing per shot.

Sharpness is measured content-independently: for every grid cell we compare
edge gradient peaks at two smoothing scales (sigma 1 vs 3). A step edge blurred
by sigma_b gives  R = sqrt((sb^2+9)/(sb^2+1)), so we can invert R into an
estimated blur sigma in pixels, instead of using raw Laplacian variance (which
mostly measures how much text is in the cell). Flat cells are "no data".

Per shot it reports:
  * dof            deep / shallow-band (tilt-shift) / spot / soft-overall
  * band           orientation (horizontal / vertical / diagonal, degrees) + position
  * rack_focus     sharp region moving independently of the camera, or blur level changing
  * framing        macro / medium / wide from the median height of sharp UI elements (glyphs)
  * heatmap PNG    per shot (red = sharp)

usage: focus_map.py video.mp4 --shots shots.json [-o focus.json] [--png-dir focus/]
"""
import argparse
import math
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import dump, iter_frames, load, probe, r  # noqa: E402

AW = 640          # analysis width
GR, GC = 9, 16    # grid rows/cols
SHARP_SIGMA = 1.6  # blur sigma (analysis px) under which a cell counts as in focus


def blur_grid(g):
    g = g.astype(np.float32)
    out = np.full((GR, GC), np.nan, np.float32)
    mags = []
    for s in (1.0, 3.0):
        b = cv2.GaussianBlur(g, (0, 0), s)
        gx = cv2.Sobel(b, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(b, cv2.CV_32F, 0, 1, ksize=3)
        mags.append(np.hypot(gx, gy) * s)  # scale-normalised so a sharp step gives ratio ~R
    h, w = g.shape
    for i in range(GR):
        for j in range(GC):
            ys, ye = i * h // GR, (i + 1) * h // GR
            xs, xe = j * w // GC, (j + 1) * w // GC
            p1 = np.percentile(mags[0][ys:ye, xs:xe], 98)
            p3 = np.percentile(mags[1][ys:ye, xs:xe], 98)
            if p3 < 24:  # flat cell, no edges to judge
                continue
            R = (p1 / p3) * 3.0  # undo the scale normalisation of the ratio: R = g1/g3
            R = max(R, 1.02)  # caps the estimate at ~14 px (beyond that it's just 'very soft')
            sb2 = (9 - R * R) / (R * R - 1)
            out[i, j] = min(math.sqrt(max(sb2, 0.0)), 12.0)
    return out


def element_height(g, mask_cells):
    """Median height (px) of edge components inside sharp cells: glyph / UI element size."""
    e = cv2.Canny(cv2.GaussianBlur(g, (3, 3), 0), 60, 140)
    h, w = g.shape
    m = cv2.resize(mask_cells.astype(np.uint8), (w, h), interpolation=cv2.INTER_NEAREST)
    e = e * (m > 0)
    e = cv2.dilate(e, np.ones((1, 3), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats((e > 0).astype(np.uint8), 8)
    hs = [st[k, cv2.CC_STAT_HEIGHT] for k in range(1, n)
          if 4 <= st[k, cv2.CC_STAT_HEIGHT] <= h * 0.25 and st[k, cv2.CC_STAT_WIDTH] / max(1, st[k, cv2.CC_STAT_HEIGHT]) < 12
          and st[k, cv2.CC_STAT_AREA] >= 6]
    return float(np.median(hs)) if len(hs) >= 8 else None


def band_shape(mask):
    ys, xs = np.nonzero(mask)
    if len(ys) < 3:
        return None
    pts = np.c_[xs / GC, ys / GR * (9 / 16)]  # aspect-correct coordinates
    c = pts.mean(0)
    cov = np.cov((pts - c).T)
    ev, evec = np.linalg.eigh(cov)
    major = evec[:, 1]
    ang = (math.degrees(math.atan2(major[1], major[0])) + 180) % 180
    elong = float(math.sqrt(ev[1] / (ev[0] + 1e-6)))
    a = min(ang, 180 - ang)
    orient = "horizontal" if a < 20 else ("vertical" if abs(ang - 90) < 20 else "diagonal")
    return {"orientation": orient, "angle_deg": r(ang, 1), "elongation": r(elong, 2),
            "center": [r(c[0], 2), r(c[1] / (9 / 16), 2)]}


def analyze(path, shots_doc, camera=None, png_dir=None, samples_per_s=4):
    info = probe(path)
    fps = info["fps"]
    H = info["height"]
    step = max(1, int(round(fps / samples_per_s)))
    shots = shots_doc["shots"]
    want = {}
    for s in shots:
        a, b = s["start_frame"], s["end_frame"] - 1
        idx = set(range(a + 1, b, step)) | {a, (a + b) // 2, b}
        for k in idx:
            want[k] = s["index"]
    data = {s["index"]: [] for s in shots}
    mids = {}
    for i, f in iter_frames(path, width=AW, gray=False):
        if i not in want:
            continue
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        grid = blur_grid(g)
        si = want[i]
        data[si].append((i, grid, g))
        s = shots[si - 1]
        if i == (s["start_frame"] + s["end_frame"] - 1) // 2:
            mids[si] = f
    scale_native = info["width"] / AW
    out = []
    cam = {c["index"]: c for c in (camera or {}).get("shots", [])}
    for s in shots:
        rows = data[s["index"]]
        stack = np.array([x[1] for x in rows])
        import warnings
        with warnings.catch_warnings(), np.errstate(all="ignore"):
            warnings.simplefilter("ignore", RuntimeWarning)
            medgrid = np.nanmedian(stack, axis=0)
        valid = np.isfinite(medgrid)
        res = {"index": s["index"], "samples": len(rows)}
        if valid.sum() < 6:
            res.update(dof="unknown", note="not enough edges to judge focus")
            out.append(res)
            continue
        sharp = valid & (medgrid < SHARP_SIGMA)
        frac = float(sharp.sum() / valid.sum())
        blurred = medgrid[valid & ~sharp]
        band = band_shape(sharp)
        if frac >= 0.8:
            dof = "deep"
        elif frac <= 0.05:
            dof = "soft-overall"
        elif band and band["elongation"] >= 2.0:
            dof = "shallow-band"
        else:
            dof = "shallow-spot"
        # temporal: centroid of the sharp region per sample + global blur level
        cents, levels = [], []
        for _, gg, _ in rows:
            v = np.isfinite(gg)
            sm = v & (gg < SHARP_SIGMA)
            levels.append(float(np.nanmedian(gg)) if v.any() else np.nan)
            if sm.sum() >= 2:
                ys, xs = np.nonzero(sm)
                cents.append((xs.mean() / GC, ys.mean() / GR))
        rack = False
        shift = None
        if len(cents) >= 3 and dof != "deep":
            c0, c1 = np.array(cents[0]), np.array(cents[-1])
            shift = float(np.linalg.norm(c1 - c0))
            cm = cam.get(s["index"], {})
            tp = cm.get("travel_px") or [0, 0]
            cam_shift = math.hypot(tp[0] / info["width"], tp[1] / H)
            rack = shift > 0.2 and abs(shift - cam_shift) > 0.15
        lv = np.array(levels, float)
        lv = lv[np.isfinite(lv)]
        focus_pull = bool(lv.size >= 3 and (np.max(lv) - np.min(lv)) > 2.0)
        # framing from element height in the sharp region of the middle sample
        _, gmid, gimg = rows[len(rows) // 2]
        eh = element_height(gimg, sharp if sharp.any() else valid)
        eh_pct = eh / gimg.shape[0] * 100 if eh else None
        framing = None
        if eh_pct is not None:
            framing = "macro" if eh_pct >= 3.5 else ("medium" if eh_pct >= 1.6 else "wide")
        res.update({
            "dof": dof,
            "sharp_fraction": r(frac, 3),
            "blur_sigma_native_px": {"sharp_cells_median": r(np.median(medgrid[sharp]) * scale_native, 2) if sharp.any() else None,
                                     "blurred_cells_median": r(np.median(blurred) * scale_native, 2) if blurred.size else None,
                                     "max": r(np.nanmax(medgrid) * scale_native, 2)},
            "band": band if dof.startswith("shallow") else None,
            "rack_focus_suspected": bool(rack),
            "sharp_region_shift": r(shift, 3),
            "focus_level_change": focus_pull,
            "element_height_pct_h": r(eh_pct, 2),
            "framing": framing,
            "grid_blur_sigma": [[r(v * scale_native, 1) if np.isfinite(v) else None for v in row] for row in medgrid],
        })
        if png_dir is not None and s["index"] in mids:
            Path(png_dir).mkdir(parents=True, exist_ok=True)
            img = mids[s["index"]].copy()
            h, w = img.shape[:2]
            heat = np.zeros((GR, GC, 3), np.uint8)
            for i in range(GR):
                for j in range(GC):
                    v = medgrid[i, j]
                    if not np.isfinite(v):
                        heat[i, j] = (60, 60, 60)
                    else:
                        t = float(np.clip(1 - (v - 0.5) / 4.0, 0, 1))  # 1 = sharp
                        heat[i, j] = (int(255 * (1 - t)), 40, int(255 * t))
            heat = cv2.resize(heat, (w, h), interpolation=cv2.INTER_NEAREST)
            vis = cv2.addWeighted(img, 0.55, heat, 0.45, 0)
            cv2.putText(vis, f"shot {s['index']}  dof={dof}  sharp={frac:.0%}  framing={framing}", (10, 24),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imwrite(str(Path(png_dir) / f"focus_shot{s['index']:02d}.png"), vis)
        out.append(res)
    hs = [x.get("element_height_pct_h") for x in out]
    return {"shots": out,
            "summary": {
                "dof_labels": sorted({x["dof"] for x in out}),
                "any_rack_focus": any(x.get("rack_focus_suspected") for x in out),
                "framing_sequence": [x.get("framing") for x in out],
                "element_height_pct_h": {"min": r(min([h for h in hs if h] or [0]), 2), "max": r(max([h for h in hs if h] or [0]), 2)},
                "method": "two-scale edge ratio -> blur sigma per cell (content-independent); framing from sharp element height",
            }}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--shots", required=True)
    ap.add_argument("--camera", help="camera.json (lets rack-focus ignore camera-driven shifts)")
    ap.add_argument("-o", "--out")
    ap.add_argument("--png-dir")
    a = ap.parse_args(argv)
    res = analyze(a.video, load(a.shots), load(a.camera) if a.camera else None, a.png_dir)
    if a.out:
        dump(res, a.out)
    for s in res["shots"]:
        print(s["index"], s["dof"], s.get("sharp_fraction"), (s.get("band") or {}).get("orientation"),
              s.get("framing"), s.get("element_height_pct_h"), "rack" if s.get("rack_focus_suspected") else "")


if __name__ == "__main__":
    main()
