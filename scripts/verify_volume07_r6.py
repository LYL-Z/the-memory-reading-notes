#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify the R6 draft against its immutable R5 source, not against editable PR labels."""
from __future__ import annotations
import collections
import csv
import re
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hanzi_count import hanzi_count, prose_body
ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "editorial/volume07/gpt6-r6/r6-chapter-verified.tsv"
BASE = "9935ad22714ea15a0828990efd26c4158d0b9e62"
EXPECTED_R5 = 80042
EXPECTED_R6 = 87286
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

def git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + p.stderr.decode(errors="replace"))
    return p.stdout.decode("utf-8")

def main() -> int:
    issues = []
    with LEDGER.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if len(rows) != 20: issues.append(f"Expected exactly 20 rows, found {len(rows)}")
    files = sorted((ROOT / "manuscript/volume-07").glob("[0-9][0-9][0-9].md"))
    if len(files) != 20: issues.append(f"Expected exactly 20 chapter files, found {len(files)}")
    before_total = after_total = 0
    gram_owners = collections.defaultdict(set)
    for i, row in enumerate(rows, 1):
        n = f"{i:03d}"; path = f"manuscript/volume-07/{n}.md"
        if row.get("chapter") != n or row.get("path") != path:
            issues.append(f"row {i} order/path mismatch"); continue
        try:
            old = git("show", f"{BASE}:{path}")
            now = (ROOT / path).read_text(encoding="utf-8-sig")
            old_count = hanzi_count(old); new_count = hanzi_count(now)
            before_total += old_count; after_total += new_count
            old_sha = git("rev-parse", f"{BASE}:{path}").strip()
            new_sha = git("rev-parse", f"HEAD:{path}").strip()
            if old_count != int(row["r5_hanzi"]) or new_count != int(row["r6_hanzi"]):
                issues.append(f"{n} text count != ledger")
            if row["r5_git_blob_sha"] != old_sha or row["r6_git_blob_sha"] != new_sha:
                issues.append(f"{n} Git blob SHA != ledger")
            if int(row["delta"]) != new_count - old_count:
                issues.append(f"{n} delta mismatch")
            if old_sha == new_sha:
                issues.append(f"{n} no actual change")
            if new_count < old_count:
                issues.append(f"{n} shrank below R5")
            han = "".join(HAN.findall(prose_body(now)))
            for k in range(max(0, len(han) - 11)):
                gram_owners[han[k:k + 12]].add(n)
            print(f"{n}: {old_count} -> {new_count} ({new_count-old_count:+})")
        except Exception as exc:
            issues.append(f"{n}: {exc}")
    duplicates = [(g, sorted(cs)) for g, cs in gram_owners.items() if len(cs) >= 2]
    print(f"TOTAL: R5={before_total}; R6={after_total}; change={after_total-before_total:+}")
    print(f"Cross-chapter exact 12-Hanzi duplicates: {len(duplicates)}")
    if before_total != EXPECTED_R5 or after_total != EXPECTED_R6:
        issues.append("volume sum differs from fixed R5/R6 target")
    if duplicates:
        issues.extend(f"repeated 12gram {g} in {','.join(ch)}" for g,ch in duplicates[:12])
    for issue in issues:
        print("FAIL:", issue, file=sys.stderr)
    if issues:
        return 1
    print("R6_CODE_AND_PROVENANCE_PASS")
    print("NOT A LITERARY OR PRIVACY PUBLICATION CERTIFICATION.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
