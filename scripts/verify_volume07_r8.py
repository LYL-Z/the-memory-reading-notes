# -*- coding: utf-8 -*-
"""Verify Volume VII R8 against the frozen R7 baseline.

R7 pinned its own snapshot verifier (verify_volume07_candidate.py, R3-pinned) and the
R4 verifier (verify_volume07_r4.py, 75k-90k window). Neither is valid here: R8 is
built on R7 (93,041 CJK), so a 90k ceiling would fail a book that is not shorter.

This verifier recomputes both sides from git objects. No static constant can be kept
green while the text drifts.

Checks
  1. 20/20 chapter files present at both revs.
  2. R8 total >= R7 total * MIN_RATIO  (R8 may cut, but not gut)
  3. R8 total <= CEIL                  (no padding back to a word-count goal)
  4. no chapter below its own R7 baseline * CHAPTER_FLOOR
  5. no cross-chapter 12-gram collision

Usage:
    python scripts/verify_volume07_r8.py                 # HEAD vs frozen R7
    python scripts/verify_volume07_r8.py <r8rev> <r7rev>
"""

from __future__ import annotations

import collections
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hanzi_count import hanzi_count  # noqa: E402

R7 = "fac27db5cb5793ec3c87d012caef4264f7784f37"
R7_TOTAL = 93_041
CH = [f"manuscript/volume-07/{i:03d}.md" for i in range(1, 21)]
CEIL = 100_000
MIN_RATIO = 0.90      # volume total may fall to 90% of R7 before it counts as gutted
CHAPTER_FLOOR = 0.80  # a single chapter may not fall below 80% of its own R7 count
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


def show(rev: str, path: str) -> str:
    out = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True)
    if out.returncode != 0:
        raise SystemExit(f"missing {path} at {rev}")
    return out.stdout.decode("utf-8")


def body(text: str) -> str:
    text = re.sub(r"(?m)^#{1,6}[ \t].*$", "", text)
    text = re.sub(r"(?s)<!--.*?-->", "", text)
    return "".join(HAN.findall(text))


def main() -> int:
    r8 = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    r7 = sys.argv[2] if len(sys.argv) > 2 else R7
    print(f"R8={r8}  R7={r7}")
    print("ch\tR7\tR8\tdelta\tverdict")
    t7 = t8 = 0
    fails: list[str] = []
    bodies: dict[str, str] = {}
    for path in CH:
        a, b = show(r7, path), show(r8, path)
        n7, n8 = hanzi_count(a), hanzi_count(b)
        t7 += n7
        t8 += n8
        bodies[path[-6:-3]] = body(b)
        ok = n8 >= n7 * CHAPTER_FLOOR
        if not ok:
            fails.append(f"{path}: {n8} < {CHAPTER_FLOOR:.0%} of {n7}")
        print(f"{path[-6:-3]}\t{n7}\t{n8}\t{n8 - n7:+d}\t{'ok' if ok else 'THIN'}")
    print(f"TOTAL\t{t7}\t{t8}\t{t8 - t7:+d}")
    if t7 != R7_TOTAL:
        print(f"WARN: R7 total recomputed as {t7}, header says {R7_TOTAL}")
    if t8 < t7 * MIN_RATIO:
        fails.append(f"volume {t8} below {MIN_RATIO:.0%} of R7 ({t7})")
    if t8 > CEIL:
        fails.append(f"volume {t8} above ceiling {CEIL}")

    hits = collections.defaultdict(set)
    for ch, s in bodies.items():
        for i in range(len(s) - 12):
            hits[s[i:i + 12]].add(ch)
    dup = {g: v for g, v in hits.items() if len(v) > 1}
    print(f"cross-chapter 12-gram collisions: {len(dup)}")
    for g, v in list(dup.items())[:8]:
        print("  ", sorted(v), g)
    if dup:
        fails.append(f"{len(dup)} duplicated 12-gram fragments across chapters")

    if fails:
        print("FAIL")
        for f in fails:
            print("  -", f)
        return 1
    print("PASS: 20 chapters, volume inside R7-relative bounds, no cross-chapter duplication.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
