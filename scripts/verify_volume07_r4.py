# -*- coding: utf-8 -*-
"""Verify Volume VII R4 candidate against the frozen R3 baseline.

Unlike scripts/verify_volume07_candidate.py (which pins the static 37,744 R3
constant), this verifier recomputes both sides from real git objects, so it can
never "pass" while the numbers have drifted.

Usage:
    python scripts/verify_volume07_r4.py                 # HEAD vs frozen R3
    python scripts/verify_volume07_r4.py <r4rev> <r3rev>

Exit code 0 = every chapter present, every chapter >= its own R3 baseline,
volume total inside the commissioned 75,000-90,000 window.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hanzi_count import hanzi_count  # noqa: E402

R3 = "c73734e17ce9336abca60959b1f15a9cf1b7d44d"
CH = [f"manuscript/volume-07/{i:03d}.md" for i in range(1, 21)]
FLOOR, CEIL = 75_000, 90_000


def blob(rev: str, path: str) -> str:
    out = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True)
    if out.returncode != 0:
        raise SystemExit(f"missing {path} at {rev}")
    return out.stdout.decode("utf-8")


def sha(rev: str, path: str) -> str:
    out = subprocess.run(["git", "rev-parse", f"{rev}:{path}"], capture_output=True)
    return out.stdout.decode().strip()


def main() -> int:
    r4 = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    r3 = sys.argv[2] if len(sys.argv) > 2 else R3
    print(f"R4={r4}  R3={r3}")
    print("ch\tR3\tR4\tdelta\tverdict")
    total3 = total4 = 0
    failures = []
    for path in CH:
        n3, n4 = hanzi_count(blob(r3, path)), hanzi_count(blob(r4, path))
        total3 += n3
        total4 += n4
        ok = n4 >= n3
        if not ok:
            failures.append(f"{path}: {n4} < {n3}")
        print(f"{path[-6:-3]}\t{n3}\t{n4}\t{n4 - n3:+d}\t{'OK' if ok else 'BELOW_BASELINE'}")
    print(f"TOTAL\t{total3}\t{total4}\t{total4 - total3:+d}")
    print(f"blob R4 001={sha(r4, CH[0])}")
    print(f"window {FLOOR}-{CEIL}: {'PASS' if FLOOR <= total4 <= CEIL else 'OUT_OF_WINDOW'}")
    if failures:
        print("FAIL\n  " + "\n  ".join(failures))
        return 1
    if not FLOOR <= total4 <= CEIL:
        return 2
    print("PASS: 20/20 chapters at or above their own R3 baseline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
