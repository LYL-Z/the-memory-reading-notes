#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R5 independent source and word-count check for 20 Volume VII chapters."""
from __future__ import annotations
import csv
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hanzi_count import hanzi_count

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "editorial/volume07/gpt6-r5/r5-chapter-verified.tsv"
R4 = "bb2a2ba52bbdc06bb179582575021f2c289c0ddd"
TOTAL_R4 = 75115
TOTAL_R5 = 80042

def git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.decode(errors='replace')}")
    return p.stdout.decode("utf-8")

def main() -> int:
    issues = []
    with LEDGER.open(encoding="utf-8-sig",newline="") as f:
        rows = list(csv.DictReader(f,delimiter="\t"))
    if len(rows) != 20: issues.append(f"Expected 20 chapters, found {len(rows)}")
    oldsum = newsum = 0
    for i,row in enumerate(rows,1):
        n = f"{i:03d}"
        path = f"manuscript/volume-07/{n}.md"
        if row.get("chapter") != n or row.get("path") != path:
            issues.append(f"Row {i}: bad chapter order/path")
            continue
        try:
            old = hanzi_count(git("show",f"{R4}:{path}"))
            new = hanzi_count((ROOT/path).read_text(encoding="utf-8-sig"))
            oldsha = git("rev-parse",f"{R4}:{path}").strip()
            newsha = git("rev-parse",f"HEAD:{path}").strip()
            oldsum += old; newsum += new
            if old!=int(row["r4_hanzi"]) or new!=int(row["r5_hanzi"]):
                issues.append(f"{n}: chapter count drift from ledger R4={old} R5={new}")
            if oldsha!=row["r4_git_blob_sha"] or newsha!=row["r5_git_blob_sha"]:
                issues.append(f"{n}: selected Git source hash drift")
            if new < old:
                issues.append(f"{n}: R5 below R4 baseline")
            if newsha == oldsha:
                issues.append(f"{n}: no change to chapter")
            print(f"{n}: {old} -> {new} ({new-old:+})")
        except Exception as exc:
            issues.append(f"{n}: {exc}")
    print(f"TOTAL: R4={oldsum} R5={newsum} DELTA={newsum-oldsum:+}")
    if oldsum!=TOTAL_R4 or newsum!=TOTAL_R5:
        issues.append("total count mismatch")
    for issue in issues:
        print(f"FAIL: {issue}",file=sys.stderr)
    if issues: return 1
    print("RESULT: R5_MECHANICAL_INTEGRITY_PASS")
    print("NOTE: Literature, third-person privacy and publication permissions NOT certified.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
