#!/usr/bin/env python3
"""compare: gate a render against a reference analysis (the "did we copy the technique?" loop).

Both inputs are analysis.json files from `sharingan analyze`. Prints a markdown
table and exits 1 if any hard gate fails, so an agent can loop
render -> analyze -> compare -> fix ONE axis -> re-render.

usage: compare.py ref/analysis.json render/analysis.json [--tol 0.15] [-o report.md]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from brief import derive  # noqa: E402
from common import load  # noqa: E402


def compare(ref, cand, tol=0.15):
    R, C = derive(ref), derive(cand)
    rows = []

    def gate(name, ok, want, got, hard=True):
        rows.append((name, "PASS" if ok else ("FAIL" if hard else "WARN"), want, got))

    rs, cs = ref["source"], cand["source"]
    gate("aspect", abs(rs["aspect"] - cs["aspect"]) < 0.02, rs["aspect"], cs["aspect"])
    gate("fps", abs(rs["fps"] - cs["fps"]) < 0.5, rs["fps"], cs["fps"], hard=False)
    lo, hi = min(R["durs"]) * (1 - tol), max(R["durs"]) * (1 + tol)
    gate("shot durations", all(lo <= x <= hi for x in C["durs"]), f"{lo:.2f}–{hi:.2f} s", f"{min(C['durs']):.2f}–{max(C['durs']):.2f} s")
    ra, ca = ref["edit"]["stats"]["asl_s"], cand["edit"]["stats"]["asl_s"]
    gate("ASL", abs(ca - ra) <= max(0.5, ra * 0.25), f"{ra} s ±25%", f"{ca} s", hard=False)
    if R["sp"]:
        lo, hi = min(R["sp"]) * (1 - tol), max(R["sp"]) * (1 + tol)
        bad = [s for s in C["sp"] if not lo <= s <= hi]
        gate("camera speed (1080p)", not bad and bool(C["sp"]), f"{lo:.1f}–{hi:.1f} px/s",
             f"{min(C['sp']):.1f}–{max(C['sp']):.1f} px/s" if C["sp"] else "no translating shots")
    if R["never"]:
        gate("camera never stops", bool(C["never"]), "every frame moves", "yes" if C["never"] else
             "no: shots " + ", ".join(str(s["index"]) for s in C["shots"] if not s.get("never_stops")))
    if not R["pulls"]:
        gate("no pull-out", not C["pulls"], "none", ", ".join(f"shot {s['index']}" for s in C["pulls"]) or "none")
    if R["push"]:
        mx = max(R["push"]) * (1 + tol)
        gate("push-in rate", all(p <= mx for p in C["push"]), f"≤ {mx:.2f} %/s", f"{max(C['push']):.2f} %/s" if C["push"] else "none", hard=False)
    if set(R["eases"]) == {"linear"}:
        gate("linear camera", set(C["eases"]) <= {"linear"}, "linear only", ", ".join(sorted(C["eases"])) or "n/a")
    if R["cvs"] and C["cvs"]:
        gate("constant velocity (cv)", max(C["cvs"]) <= max(R["cvs"]) + 0.1, f"≤ {max(R['cvs']) + 0.1:.2f}", f"{max(C['cvs']):.2f}", hard=False)
    if R["cut_moving"]:
        gate("cut while moving", bool(C["cut_moving"]), "yes", "yes" if C["cut_moving"] else "no")
    ra_, ca_ = ref.get("audio") or {}, cand.get("audio") or {}
    if ra_.get("class"):
        gate("audio class", ra_.get("class") == ca_.get("class"), ra_.get("class"), ca_.get("class"), hard=False)
    rv, cv = (ra_.get("cuts") or {}).get("verdict"), (ca_.get("cuts") or {}).get("verdict")
    if rv:
        gate("cut/audio sync", rv == cv, rv, cv, hard=False)
    fails = sum(1 for r in rows if r[1] == "FAIL")
    md = ["| gate | result | reference | render |", "|---|---|---|---|"]
    md += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows]
    md.append(f"\n**{len(rows) - fails}/{len(rows)} gates passed** ({fails} hard failures).")
    return "\n".join(md), fails


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("reference")
    ap.add_argument("render")
    ap.add_argument("--tol", type=float, default=0.15)
    ap.add_argument("-o", "--out")
    a = ap.parse_args(argv)
    md, fails = compare(load(a.reference), load(a.render), a.tol)
    if a.out:
        Path(a.out).write_text(md + "\n")
    print(md)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
