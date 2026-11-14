#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify the selected 2026-11-14 six-volume manuscript. No network or external packages."""
from __future__ import annotations

import csv
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

from hanzi_count import hanzi_count, prose_body

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editorial/six-volume-integration/2026-11-14-chapter-canon.tsv"
EXPECTED_CHAPTERS = {1: 18, 2: 24, 3: 16, 4: 18, 5: 19, 6: 20}
EXPECTED_HANZI = {1: 138952, 2: 172099, 3: 140227, 4: 74236, 5: 80985, 6: 126300}
EXPECTED_TOTAL = 732799


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def main() -> int:
    problems: list[str] = []
    warnings: list[str] = []
    with MANIFEST.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if len(rows) != 115:
        problems.append(f"manifest has {len(rows)} chapters, expected 115")

    groups: dict[int, list[int]] = defaultdict(list)
    seen: set[str] = set()
    for row in rows:
        try:
            p = row["path"]
            vol = int(row["volume"])
            chapter = row["chapter"]
            expected = int(row["official_hanzi"])
            if p in seen:
                raise ValueError("duplicate manifest path")
            seen.add(p)
            if not re.fullmatch(rf"manuscript/volume-0{vol}/\d{{3}}\.md", p):
                raise ValueError(f"bad source path: {p}")
            if Path(p).stem != chapter:
                raise ValueError("chapter number differs from file stem")
            path = ROOT / p
            binary = path.read_bytes()
            text = binary.decode("utf-8-sig")
            found = hanzi_count(text)
            groups[vol].append(found)
            if found != expected:
                problems.append(f"{p}: expected {expected} CJK, found {found}")
            observed_sha = git_blob_sha(binary)
            if observed_sha != row["git_blob_sha"]:
                problems.append(f"{p}: Git blob changed from selected source; update provenance ledger only after review")
            if not re.search(r"(?m)^# [^\n]+", text):
                problems.append(f"{p}: missing main title")
            if any(x in text for x in ("<<<<<<< ", "=======", ">>>>>>> ")):
                problems.append(f"{p}: possible merge conflict marker")
            if "问卷" in prose_body(text):
                warnings.append(f"{p}: contains 问卷; evaluate context, do not blindly remove")
        except Exception as exc:
            problems.append(f"manifest row failure: {row.get('path', '?')}: {exc}")

    all_files = {
        p.relative_to(ROOT).as_posix()
        for vol in EXPECTED_CHAPTERS
        for p in (ROOT / f"manuscript/volume-0{vol}").glob("[0-9][0-9][0-9].md")
    }
    if all_files != seen:
        problems.append(
            f"manifest/file mismatch: extra={sorted(all_files-seen)} missing={sorted(seen-all_files)}"
        )

    grand = sum(sum(nums) for nums in groups.values())
    for vol, target in EXPECTED_CHAPTERS.items():
        if len(groups[vol]) != target:
            problems.append(f"volume {vol}: {len(groups[vol])} chapters, expected {target}")
        actual = sum(groups[vol])
        if actual != EXPECTED_HANZI[vol]:
            problems.append(f"volume {vol}: {actual} CJK, expected {EXPECTED_HANZI[vol]}")
        print(f"volume-{vol:02}: {len(groups[vol])} chapters, {actual:,} official Hanzi")
    print(f"TOTAL: {grand:,} official Hanzi")
    if grand != EXPECTED_TOTAL:
        problems.append(f"total {grand}, expected {EXPECTED_TOTAL}")
    print(f"word/document warnings: {len(warnings)}")
    for w in warnings[:40]:
        print("WARN:", w)
    for error in problems:
        print("ERROR:", error, file=sys.stderr)
    if problems:
        print("RESULT: FAIL", file=sys.stderr)
        return 1
    print("RESULT: MECHANICAL_INTEGRITY_PASS")
    print("NOTE: This is not a literary cold read, privacy clearance, or publication approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
