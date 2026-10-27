#!/usr/bin/env python3
"""camera_track: measure camera language per shot, in numbers.

Per consecutive frame pair inside a shot we fit a similarity transform
(Shi-Tomasi + pyramidal Lucas-Kanade with a forward/backward check, or ORB +
Hamming matching) with RANSAC, and decompose it into:

  * centre translation      -> vx, vy, speed in px/s (native, 1080p-equivalent, %W/s)
  * scale                   -> %/s (push-in > 0, pull-out < 0)
  * in-plane rotation       -> deg/s (roll)
  * grid motion             -> mean on-screen displacement of a 9x5 grid (zoom-aware speed)

Then per shot:
  * move vocabulary         -> static / truck / pedestal / pan / tilt / push-in / pull-out / roll / orbit
  * easing                  -> progress curve fitted against linear + power1-3 in/out/inOut + sine
  * never-stops check       -> frames whose (smoothed) motion is below a stop threshold
  * enters/exits moving     -> is the shot cut while the camera still moves?
  * pull-out detection      -> scale measured directly between frames 0.5 s apart
  * perspective drift       -> first->last homography keystone (pan/tilt/orbit vs truck/pedestal)
  * shake                   -> high-frequency jitter of the translation
  * UI micro-animation      -> residual after motion compensation = things moving INSIDE the UI

Sign convention: velocities are CONTENT motion on screen. The camera moves the
opposite way (content sliding left = camera trucking right).

usage: camera_track.py video.mp4 --shots shots.json [-o camera.json] [--method lk|orb]
"""
import argparse
import collections
import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import dump, iter_frames, load, med, pct, probe, r  # noqa: E402

DIAG_1080 = math.hypot(1920, 1080)

EASES = {
    "linear": lambda x: x,
    "power1.in": lambda x: x ** 2, "power1.out": lambda x: 1 - (1 - x) ** 2,
    "power2.in": lambda x: x ** 3, "power2.out": lambda x: 1 - (1 - x) ** 3,
    "power3.in": lambda x: x ** 4, "power3.out": lambda x: 1 - (1 - x) ** 4,
    "power1.inOut": lambda x: np.where(x < .5, 2 * x ** 2, 1 - (-2 * x + 2) ** 2 / 2),
    "power2.inOut": lambda x: np.where(x < .5, 4 * x ** 3, 1 - (-2 * x + 2) ** 3 / 2),
    "power3.inOut": lambda x: np.where(x < .5, 8 * x ** 4, 1 - (-2 * x + 2) ** 4 / 2),
    "sine.inOut": lambda x: -(np.cos(np.pi * x) - 1) / 2,
}
# GSAP names; CSS equivalents for the brief
CSS = {"linear": "linear", "power1.in": "cubic-bezier(.55,.085,.68,.53)", "power1.out": "cubic-bezier(.25,.46,.45,.94)",
       "power2.in": "cubic-bezier(.55,.055,.675,.19)", "power2.out": "cubic-bezier(.215,.61,.355,1)",
       "power3.in": "cubic-bezier(.895,.03,.685,.22)", "power3.out": "cubic-bezier(.165,.84,.44,1)",
       "power1.inOut": "cubic-bezier(.455,.03,.515,.955)", "power2.inOut": "cubic-bezier(.645,.045,.355,1)",
       "power3.inOut": "cubic-bezier(.77,0,.175,1)", "sine.inOut": "cubic-bezier(.445,.05,.55,.95)"}


class Estimator:
    def __init__(self, method="lk"):
        self.method = method
        if method == "orb":
            self.orb = cv2.ORB_create(3000)
            self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def pair(self, a, b):
        """Similarity a->b: returns (M 2x3, inliers, candidates) or (None, 0, 0)."""
        if self.method == "orb":
            k1, d1 = self.orb.detectAndCompute(a, None)
            k2, d2 = self.orb.detectAndCompute(b, None)
            if d1 is None or d2 is None:
                return None, 0, 0
            m = self.bf.match(d1, d2)
            if len(m) < 12:
                return None, 0, len(m)
            p0 = np.float32([k1[x.queryIdx].pt for x in m])
            p1 = np.float32([k2[x.trainIdx].pt for x in m])
        else:
            p0 = cv2.goodFeaturesToTrack(a, 800, 0.005, 8, blockSize=7)
            if p0 is None or len(p0) < 12:
                return None, 0, 0
            p1, st, _ = cv2.calcOpticalFlowPyrLK(a, b, p0, None, winSize=(31, 31), maxLevel=4)
            pb, st2, _ = cv2.calcOpticalFlowPyrLK(b, a, p1, None, winSize=(31, 31), maxLevel=4)
            ok = (st.ravel() == 1) & (st2.ravel() == 1) & (np.linalg.norm((p0 - pb).reshape(-1, 2), axis=1) < 0.5)
            p0, p1 = p0[ok].reshape(-1, 2), p1[ok].reshape(-1, 2)
            if len(p0) < 12:
                return None, 0, len(p0)
        M, inl = cv2.estimateAffinePartial2D(p0, p1, method=cv2.RANSAC, ransacReprojThreshold=1.0,
                                             maxIters=4000, confidence=0.999, refineIters=20)
        if M is None:
            return None, 0, len(p0)
        return M, int(inl.sum()), len(p0)


def homography(a, b):
    orb = cv2.ORB_create(4000)
    k1, d1 = orb.detectAndCompute(a, None)
    k2, d2 = orb.detectAndCompute(b, None)
    if d1 is None or d2 is None:
        return None
    m = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d1, d2)
    if len(m) < 30:
        return None
    p0 = np.float32([k1[x.queryIdx].pt for x in m])
    p1 = np.float32([k2[x.trainIdx].pt for x in m])
    Hm, inl = cv2.findHomography(p0, p1, cv2.RANSAC, 2.0)
    if Hm is None or inl.sum() < 25:
        return None
    return Hm / Hm[2, 2]


def keystone(Hm, w, h):
    """Corner disagreement between H and its best affine approximation, as a fraction of the diagonal."""
    if Hm is None:
        return None
    pts = np.float32([[0, 0], [w, 0], [w, h], [0, h], [w / 2, h / 2]]).reshape(-1, 1, 2)
    ph = cv2.perspectiveTransform(pts, Hm).reshape(-1, 2)
    A, _ = cv2.estimateAffine2D(pts.reshape(-1, 2), ph)
    pa = (A @ np.c_[pts.reshape(-1, 2), np.ones(5)].T).T
    return float(np.max(np.linalg.norm(ph - pa, axis=1)) / math.hypot(w, h))


def fit_ease(motion):
    m = np.clip(np.asarray(motion, float), 0, None)
    if m.size < 6 or m.sum() <= 0:
        return None
    prog = np.r_[0, np.cumsum(m)] / m.sum()
    x = np.linspace(0, 1, prog.size)
    scores = {k: float(np.sqrt(np.mean((f(x) - prog) ** 2))) for k, f in EASES.items()}
    best = min(scores, key=scores.get)
    thirds = np.array_split(m, 3)
    t = [float(np.mean(s)) for s in thirds]
    return {"best": best, "css": CSS[best], "rmse": r(scores[best], 4), "linear_rmse": r(scores["linear"], 4),
            "progress_at": {"25%": r(np.interp(.25, x, prog), 3), "50%": r(np.interp(.5, x, prog), 3),
                            "75%": r(np.interp(.75, x, prog), 3)},
            "speed_thirds_rel": [r(v / (np.mean(m) + 1e-9), 2) for v in t]}


def classify(s, stop_thr, persp_thr=0.01):
    comps = []
    sp = s["center_speed_px_s_1080p"] or 0
    vx, vy = s["vx_px_s"] or 0, s["vy_px_s"] or 0
    ks = s.get("perspective_drift") or 0
    persp = ks > persp_thr
    if sp >= stop_thr:
        if abs(vx) >= 0.25 * (s["center_speed_px_s"] or 1e-9):
            comps.append(("pan-" if persp else "truck-") + ("right" if vx < 0 else "left"))
        if abs(vy) >= 0.25 * (s["center_speed_px_s"] or 1e-9):
            comps.append(("tilt-" if persp else "pedestal-") + ("up" if vy > 0 else "down"))
    if s["scale_pct_s"] is not None and s["scale_pct_s"] > 0.25:
        comps.append("push-in")
    elif s["scale_pct_s"] is not None and s["scale_pct_s"] < -0.25:
        comps.append("pull-out")
    if s["rotation_deg_s"] is not None and abs(s["rotation_deg_s"]) > 0.5:
        comps.append("roll-" + ("cw" if s["rotation_deg_s"] > 0 else "ccw"))
    if persp and sp < stop_thr:
        comps.append("orbit")
    if not comps:
        return "static" if (s["motion_px_s_1080p"]["median"] or 0) < stop_thr else "drift"
    return "+".join(comps)


def track(path, shots_doc, method="lk", track_w=960, stop_thr=2.0, window_s=0.5):
    info = probe(path)
    W, H, fps = info["width"], info["height"], info["fps"]
    tw = min(W, track_w)
    f = W / tw  # native px per tracking px
    th = int(round(H / f))
    norm = DIAG_1080 / math.hypot(W, H)  # native px -> 1080p-equivalent px
    gx, gy = np.meshgrid(np.linspace(.05, .95, 9) * tw, np.linspace(.05, .95, 5) * th)
    grid = np.c_[gx.ravel(), gy.ravel(), np.ones(gx.size)]
    cen = np.array([tw / 2, th / 2, 1.0])
    est = Estimator(method)
    shots = shots_doc["shots"]
    starts = {s["start_frame"]: s for s in shots}
    win = max(2, int(round(window_s * fps)))
    per = {s["index"]: [] for s in shots}
    firstlast = {}
    persp_samples = {s["index"]: [] for s in shots}
    half = max(1, int(round(fps / 2)))
    ui_frames = []
    buf = collections.deque(maxlen=win + 1)
    windows = {s["index"]: [] for s in shots}
    prev = None
    cur_shot = None
    for i, g in iter_frames(path, width=tw):
        if i in starts:
            cur_shot = starts[i]
            prev = None
            buf.clear()
            firstlast[cur_shot["index"]] = [g, g]
        if cur_shot is None:
            continue
        firstlast[cur_shot["index"]][1] = g
        if (i - cur_shot["start_frame"]) % half == 0:
            persp_samples[cur_shot["index"]].append(g)
        if prev is not None:
            M, inl, cand = est.pair(prev, g)
            row = {"frame": i, "inliers": inl, "cand": cand}
            if M is not None and inl >= 10:
                a, b = M[0, 0], M[1, 0]
                sc = math.hypot(a, b)
                d = (M @ cen) - cen[:2]
                gm = np.linalg.norm((grid @ M.T) - grid[:, :2], axis=1).mean()
                row.update(dx=d[0] * f, dy=d[1] * f, lns=math.log(sc), rot=math.degrees(math.atan2(b, a)),
                           grid=gm * f)
                # residual after compensation -> UI micro-animation
                warped = cv2.warpAffine(prev, M, (tw, th), flags=cv2.INTER_LINEAR)
                valid = cv2.warpAffine(np.full_like(prev, 255), M, (tw, th), flags=cv2.INTER_NEAREST)
                valid = cv2.erode(valid, np.ones((9, 9), np.uint8))
                diff = cv2.absdiff(cv2.GaussianBlur(warped, (5, 5), 0), cv2.GaussianBlur(g, (5, 5), 0))
                ch = ((diff > 28) & (valid > 0)).astype(np.uint8)
                ch = cv2.morphologyEx(ch, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
                frac = float(ch.mean())
                row["residual"] = frac
                if frac > 0.0008:
                    ys, xs = np.nonzero(ch)
                    ui_frames.append({"frame": i, "shot": cur_shot["index"], "area_pct": frac * 100,
                                      "x": float(xs.mean() / tw), "y": float(ys.mean() / th)})
            per[cur_shot["index"]].append(row)
        # windowed scale (direct estimate across 0.5 s, robust to per-frame noise)
        buf.append((i, g))
        if len(buf) == win + 1 and (i - cur_shot["start_frame"]) % 3 == 0:
            M, inl, _ = est.pair(buf[0][1], g)
            if M is not None and inl >= 15:
                d = (M @ cen) - cen[:2]
                windows[cur_shot["index"]].append({"t": r((buf[0][0] + i) / 2 / fps, 3),
                                                   "scale_pct": (math.hypot(M[0, 0], M[1, 0]) - 1) * 100,
                                                   "dx": d[0] * f, "dy": d[1] * f})
        prev = g

    # group UI residual frames into events
    events = []
    for u in ui_frames:
        if events and u["frame"] - events[-1]["end_frame"] <= 1 and u["shot"] == events[-1]["shot"]:
            e = events[-1]
            e["end_frame"] = u["frame"]
            e["peak_area_pct"] = max(e["peak_area_pct"], u["area_pct"])
        else:
            events.append({"frame": u["frame"], "end_frame": u["frame"], "shot": u["shot"],
                           "peak_area_pct": u["area_pct"], "x": u["x"], "y": u["y"]})
    for e in events:
        e["time_s"] = r(e["frame"] / fps, 3)
        e["dur_s"] = r((e["end_frame"] - e["frame"] + 1) / fps, 3)
        e["peak_area_pct"] = r(e["peak_area_pct"], 3)
        e["x"], e["y"] = r(e["x"], 2), r(e["y"], 2)

    out = []
    for s in shots:
        rows = [x for x in per[s["index"]] if "dx" in x]
        res = {"index": s["index"], "start_s": s["start_s"], "dur_s": s["dur_s"], "tracked_pairs": len(rows),
               "pairs": max(0, s["frames"] - 1)}
        if len(rows) < 3:
            res.update(move="untracked", note="too few trackable frames (textureless, very short, or heavy blur)")
            out.append(res)
            continue
        dx = np.array([x["dx"] for x in rows]) * fps
        dy = np.array([x["dy"] for x in rows]) * fps
        sp = np.hypot(dx, dy)
        lns = np.array([x["lns"] for x in rows])
        rot = np.array([x["rot"] for x in rows]) * fps
        gm = np.array([x["grid"] for x in rows]) * fps * norm
        gms = np.convolve(np.pad(gm, 1, mode="edge"), np.ones(3) / 3, mode="valid") if gm.size >= 3 else gm
        wl = windows[s["index"]]
        span = win / fps
        if len(wl) >= 3:  # direct 0.5 s estimates: unbiased, high SNR (per-frame fits under-read slow zooms)
            vx = med([x["dx"] for x in wl]) / span
            vy = med([x["dy"] for x in wl]) / span
            speed = med([math.hypot(x["dx"], x["dy"]) for x in wl]) / span
            rate = ((1 + med([x["scale_pct"] for x in wl]) / 100) ** (1 / span) - 1) * 100
            rate_src = "window"
        else:
            vx, vy = med(dx), med(dy)
            speed = float(np.hypot(np.sum(dx), np.sum(dy)) / len(rows))
            rate = (math.exp(med(lns) * fps) - 1) * 100
            rate_src = "per-frame"
        jit = float(np.std(np.diff(dx)) + np.std(np.diff(dy))) / fps if len(rows) > 3 else 0.0
        w = [x["scale_pct"] for x in windows[s["index"]]]
        # perspective drift: median keystone over 1 s spans (robust to UI content changing mid-shot)
        ps = persp_samples[s["index"]]
        kv = []
        for k in range(len(ps) - 2):
            kk = keystone(homography(ps[k], ps[k + 2]), ps[k].shape[1], ps[k].shape[0])
            if kk is not None:
                kv.append(kk)
        if not kv and s["frames"] > 2:
            kk = keystone(homography(*firstlast[s["index"]]), tw, th)
            kv = [kk / max(s["dur_s"], 1e-3)] if kk is not None else []
        ks = float(np.median(kv)) if kv else None
        stopped = int((gms < stop_thr).sum())
        settle = float(gms.min() / (np.median(gms) + 1e-9))
        edge = min(3, len(gms))
        tot_scale = ((1 + rate / 100) ** ((s["frames"] - 1) / fps) - 1) * 100
        evt = [e["time_s"] for e in events if e["shot"] == s["index"]]
        neg_all = [x for x in windows[s["index"]] if x["scale_pct"] < -0.3]
        neg = [x for x in neg_all if not any(abs(x["t"] - t) <= span / 2 + 1 / fps for t in evt)]
        reflow = [x for x in neg_all if x not in neg]
        res.update({
            "vx_px_s": r(vx, 1), "vy_px_s": r(vy, 1),
            "center_speed_px_s": r(speed, 1),
            "center_speed_px_s_1080p": r(speed * norm, 1),
            "speed_pctW_s": r(speed / W * 100, 2),
            "speed_frame_median_px_s": r(med(sp), 1),
            "rate_source": rate_src,
            "speed_cv": r(np.std(sp) / (np.mean(sp) + 1e-9), 3) if np.mean(sp) > stop_thr else None,
            "travel_px": [r(np.sum(dx) / fps, 1), r(np.sum(dy) / fps, 1)],
            "mean_speed_px_s_1080p": r(math.hypot(np.sum(dx), np.sum(dy)) / fps / ((s["frames"] - 1) / fps) * norm, 1),
            "scale_pct_s": r(rate, 3),
            "scale_total_pct": r(tot_scale, 2),
            "rotation_deg_s": r(med(rot), 3),
            "perspective_drift": r(ks, 4),  # keystone per 1 s, fraction of the diagonal
            "motion_px_s_1080p": {"median": r(med(gm), 1), "p5": r(pct(gms, 5), 1), "min": r(float(gms.min()), 1),
                                  "max": r(float(gms.max()), 1)},
            "never_stops": bool(stopped == 0 and settle >= 0.25),
            "min_to_median_motion": r(settle, 3),
            "frames_below_stop": stopped,
            "stop_threshold_px_s_1080p": stop_thr,
            "enters_moving": bool(np.mean(gms[:edge]) >= stop_thr),
            "exits_moving": bool(np.mean(gms[-edge:]) >= stop_thr),
            "shake_px": r(jit, 3),
            "window_scale_pct_per_0p5s": {"min": r(min(w), 3) if w else None, "median": r(med(w), 3) if w else None,
                                          "max": r(max(w), 3) if w else None},
            "pull_out": {"detected": bool(tot_scale < -0.5 or len(neg) >= 3),
                         "negative_windows": len(neg), "at_s": [x["t"] for x in neg[:12]],
                         "reflow_suspect_at_s": [x["t"] for x in reflow[:12]]},
            "ease": fit_ease(gm) if np.median(gm) >= stop_thr else None,
            "tracking": {"median_inliers": int(np.median([x["inliers"] for x in rows])),
                         "median_candidates": int(np.median([x["cand"] for x in rows]))},
            "ui_events": [e["time_s"] for e in events if e["shot"] == s["index"]],
        })
        res["move"] = classify(res, stop_thr)
        out.append(res)

    moving = [s for s in out if s.get("move") not in ("static", "untracked", None)]
    sp = [s["center_speed_px_s_1080p"] for s in moving if s.get("center_speed_px_s_1080p", 0) >= stop_thr]
    pushes = [s["scale_pct_s"] for s in moving if (s.get("scale_pct_s") or 0) > 0.25]
    summary = {
        "method": method, "tracking_width": tw, "units": "content motion on screen; camera moves opposite",
        "shots_moving": len(moving), "shots_static": sum(1 for s in out if s.get("move") == "static"),
        "speed_px_s_1080p": {"min": r(min(sp), 1), "median": r(med(sp), 1), "max": r(max(sp), 1)} if sp else None,
        "speed_pctW_s": {"min": r(min(sp) / 19.2, 2), "max": r(max(sp) / 19.2, 2)} if sp else None,
        "push_in_pct_s": {"min": r(min(pushes), 2), "max": r(max(pushes), 2)} if pushes else None,
        "camera_never_stops": all(s.get("never_stops") for s in moving) and len(moving) == len(out),
        "any_pull_out": any(s.get("pull_out", {}).get("detected") for s in out),
        "cut_while_moving": all(s.get("exits_moving") for s in moving[:-1]) if len(moving) > 1 else None,
        "ease_labels": sorted({s["ease"]["best"] for s in out if s.get("ease")}),
        "max_speed_cv": r(max([s["speed_cv"] for s in out if s.get("speed_cv") is not None] or [0]), 3),
        "ui_event_count": len(events),
    }
    return {"summary": summary, "shots": out, "ui_events": events}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--shots", required=True, help="shots.json from cuts.py")
    ap.add_argument("-o", "--out")
    ap.add_argument("--method", default="lk", choices=["lk", "orb"])
    ap.add_argument("--track-width", type=int, default=960)
    ap.add_argument("--stop", type=float, default=2.0, help="stop threshold, 1080p-equivalent px/s")
    a = ap.parse_args(argv)
    res = track(a.video, load(a.shots), a.method, a.track_width, a.stop)
    if a.out:
        dump(res, a.out)
    for s in res["shots"]:
        print(f'shot {s["index"]:>2} {s["dur_s"]:>5}s  {s.get("move"):<34} speed {s.get("center_speed_px_s")} px/s  '
              f'scale {s.get("scale_pct_s")} %/s  ease {(s.get("ease") or {}).get("best")}  never_stops {s.get("never_stops")}')
    print(json.dumps(res["summary"], indent=1))


if __name__ == "__main__":
    main()
