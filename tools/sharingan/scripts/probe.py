#!/usr/bin/env python3
"""probe: container / stream facts (fps, size, duration, audio).

usage: probe.py video.mp4 [-o probe.json]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import dump, probe  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("-o", "--out")
    a = ap.parse_args(argv)
    p = probe(a.video)
    if a.out:
        dump(p, a.out)
    print(json.dumps(p, indent=2))


if __name__ == "__main__":
    main()
