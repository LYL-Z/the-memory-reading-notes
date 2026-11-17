#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 02_full-reading-ledger.tsv from inventory + read-records (evidence-derived).

FULL_TEXT is NO LONGER a hand-written declaration: it is derived from
read-records/read-records.tsv. A file with no read-record cannot be FULL_TEXT.
"""
import io, csv, os

OUT = r"D:/The Memory/tmp/reading-notes-review/editorial/full-corpus-readiness"

def load_records():
    p = os.path.join(OUT, "read-records", "read-records.tsv")
    if not os.path.exists(p):
        return {}
    recs = {}
    for r in csv.DictReader(io.open(p, encoding="utf-8"), delimiter="\t"):
        recs[r["file"]] = r
    return recs

def main():
    src = os.path.join(OUT, "01_repository-inventory.tsv")
    rows = list(csv.DictReader(io.open(src, encoding="utf-8"), delimiter="\t"))
    recs = load_records()
    fields = ["repository","relative_path","version_read","reading_status","reading_method",
              "reading_coverage","evidence_note","blocking_reason","next_action","priority_for_round2","read_record"]
    out = []
    for r in rows:
        path = r["relative_path"]
        status, method, coverage, note, nxt, rec = "UNREAD", "", "0%", "", "round2", ""
        if path in recs:
            rec = recs[path]
            status = "FULL_TEXT"
            method = rec["tool"]
            coverage = rec["read_range"]
            note = rec["note"]
            nxt = "done"
        elif path.startswith("manuscript/"):
            status = "STRUCTURED_ONLY"
            method = "scripted_metrics"
            coverage = "metadata+metrics only"
            note = "title/hanzi/paragraph/dialogue/probe extraction; body not read"
            nxt = "full_read_required"
        out.append(dict(repository=r["repository"], relative_path=path,
                        version_read=rec["version"] if rec else r["branch_or_commit"],
                        reading_status=status, reading_method=method, reading_coverage=coverage,
                        evidence_note=note, blocking_reason="", next_action=nxt,
                        priority_for_round2=r["source_priority"], read_record=rec["artifact"] if rec else ""))
    p = os.path.join(OUT, "02_full-reading-ledger.tsv")
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t"); w.writeheader()
        for r in out: w.writerow(r)
    import collections
    c = collections.Counter(r["reading_status"] for r in out)
    print("ledger rows:", len(out), "->", p)
    for k, v in c.most_common(): print(f"  {v:6d}  {k}")
    print("derived from read-records:", len(recs))

if __name__ == "__main__":
    main()
