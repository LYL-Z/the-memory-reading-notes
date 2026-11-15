#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify volume VII draft integrity and chapter provenance; does NOT judge literary quality."""
from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

from hanzi_count import hanzi_count
ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "editorial" / "volume07" / "2026-11-14-r3-chapter-ledger.tsv"
EXPECTED_CHAPTERS = 20
EXPECTED_TOTAL = 37744


def sha_git_blob(payload: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(payload)).encode("ascii") + b"\0" + payload).hexdigest()


def main() -> int:
    with INDEX.open("r", encoding="utf-8-sig", newline="") as fh:
        ledger = list(csv.DictReader(fh, delimiter="\t"))
    errors: list[str] = []
    if len(ledger) != EXPECTED_CHAPTERS:
        errors.append(f"ledger contains {len(ledger)} chapters instead of 20")
    count_total = 0
    seen: set[str] = set()
    for row in ledger:
        n = row["chapter"]
        path = row["path"]
        expected_path = f"manuscript/volume-07/{n}.md"
        if path != expected_path or path in seen:
            errors.append(f"duplicate or wrong path {path}")
            continue
        seen.add(path)
        try:
            payload = (ROOT / path).read_bytes()
            data = payload.decode("utf-8-sig")
            actual = hanzi_count(data)
            count_total += actual
            if actual != int(row["r3_hanzi"]):
                errors.append(f"{n}: {actual} instead of {row['r3_hanzi']} Hanzi")
            if sha_git_blob(payload) != row["r3_git_blob_sha"]:
                errors.append(f"{n}: chosen source SHA changed")
            if not data.startswith("# "):
                errors.append(f"{n}: missing heading")
            if any(k in data for k in ("<<<<<<< ", ">>>>>>> ")):
                errors.append(f"{n}: git conflict marker")
        except (OSError, UnicodeError, ValueError, KeyError) as exc:
            errors.append(f"{n}: {exc}")
    all_chapters = {
        f"manuscript/volume-07/{n:03}.md" for n in range(1, EXPECTED_CHAPTERS + 1)
    }
    if all_chapters != seen:
        errors.append(f"chapter inventory mismatch: {sorted(all_chapters.symmetric_difference(seen))}")
    if count_total != EXPECTED_TOTAL:
        errors.append(f"total {count_total} instead of {EXPECTED_TOTAL}")
    print(f"Volume VII candidate: {len(seen)} chapters, {count_total:,} Hanzi")
    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    print("RESULT:", "FAIL" if errors else "MECHANICAL_INTEGRITY_PASS")
    print("NOTE: Does not certify literary quality or third-party publication rights.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
