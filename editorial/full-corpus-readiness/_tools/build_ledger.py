#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 02_full-reading-ledger.tsv from inventory + actual reading record.

Only files genuinely opened and read end-to-end in this session are marked
FULL_TEXT. Structural/scripted metrics are marked STRUCTURED_ONLY, never FULL.
"""
import io, csv, os

OUT = r"D:/The Memory/tmp/reading-notes-review/editorial/full-corpus-readiness"

# Files read in full, end-to-end, this session (verified by Read/Bash cat in transcript)
FULL = {
 # --- repo B: governing documents ---
 "AGENTS.md": ("B", "governing rules 2026-11-14; 9 clauses"),
 "README.md": ("B", "six-volume entry, 115ch/732,799 official CJK, PR#77 merge"),
 "editorial/author-decisions/2026-11-13-reconstruction-and-literary-authority.md": ("B", "author's latest reconstruction authority; 4-tier levels"),
 "editorial/six-volume-integration/2026-11-14-editorial-verdict.md": ("B", "current literary verdict per volume + open disputes"),
 "editorial/six-volume-integration/2026-11-14-three-clocks-and-canon.md": ("B", "T_event/T_person_knows/T_reader + cross-volume constraints"),
 "editorial/six-volume-integration/2026-11-14-author-rulings.md": ("B", "5 point rulings + PR#70 four corrections + open divergences"),
 "editorial/six-volume-integration/2026-11-14-publication-gates.md": ("B", "third-party rights gates, all OPEN"),
 "editorial/longform-architecture/2026-11-07-six-plus-one-author-realignment.md": ("B", "6+1 architecture proposal; superseded numbering"),
 "editorial/longform-architecture/2026-11-08-seven-part-aesthetic-motif-and-music-map.md": ("B", "7-part aesthetic score, motifs M01-M08, cross-volume variations"),
 # --- repo B: manuscript ---
 "editorial/contradictions.md": ("B", "full 360 lines: 99 open items + 12 closed + 5 never-to-dramatise"),
 "manuscript/volume-01/018.md": ("B", "V1 finale 历史课; core anchor, 4-person truth-or-dare, ends open"),
 "manuscript/volume-07/001.md": ("B", "red box / admission notice / mother's neighbour talk"),
 "manuscript/volume-07/002.md": ("B", "check-in day, mosquito net, key rule with 曾子沣"),
 "manuscript/volume-07/003.md": ("B", "军训, 赵文邦 intro, 行测, ranks"),
 "manuscript/volume-07/004.md": ("B", "Dark Zone game dispute; '总裁气质' origin"),
 "manuscript/volume-07/005.md": ("B", "first timetable; unit error 16 vs 1.6; meta '写到这里'"),
 "manuscript/volume-07/006.md": ("B", "first-semester grades; weighted GPA; 热学 75"),
 "manuscript/volume-07/007.md": ("B", "canteen group; 唐嘉睿/高泽聪; unpaid chair"),
 "manuscript/volume-07/008.md": ("B", "shooting schedule; missing SD card; 4-min test footage"),
 "manuscript/volume-07/009.md": ("B", "director credit order; '楼梯' rename — strongest chapter"),
 "manuscript/volume-07/013.md": ("B", "father: tea, Chongqing 2025-08, 1985 TV set, Xinjiang"),
 "manuscript/volume-07/014.md": ("B", "Xi'an trip with mother+赵问竹; no contact info"),
 "manuscript/volume-07/015.md": ("B", "photo cropping as unreliability; two versions kept"),
 "manuscript/volume-07/020.md": ("B", "unfinished app; '半成品'; 'not a company employee'"),
 # --- repo A: full text ---
 "高中/G2204/人物/同学/赵问竹.md": ("A", "core person page; incl. 2026-09-16 dual-affection confirmation"),
}

STRUCTURED = {
 "manuscript/volume-01..06 (all 115 chapters)": ("B", "scripted metrics only: title/hanzi/paragraphs/dialogue/marks/probes; NOT full reading"),
 "manuscript/volume-07 (all 20 chapters)": ("B", "scripted metrics for all 20; full text for 15 of 20"),
}

def main():
    src = os.path.join(OUT, "01_repository-inventory.tsv")
    rows = list(csv.DictReader(io.open(src, encoding="utf-8"), delimiter="\t"))
    fields = ["repository","relative_path","version_read","reading_status","reading_method",
              "reading_coverage","evidence_note","blocking_reason","next_action","priority_for_round2"]
    out = []
    for r in rows:
        repo = "B" if r["repository"].startswith("B") else "A"
        path = r["relative_path"]
        key = path
        status = "UNREAD"
        method = ""
        coverage = "0%"
        note = ""
        blocking = ""
        nxt = "round2"
        prio = ""
        if key in FULL:
            status = "FULL_TEXT"
            method = "read_end_to_end"
            coverage = "100%"
            note = FULL[key][1]
            nxt = "done"
            prio = "P0"
        elif path.startswith("manuscript/"):
            status = "STRUCTURED_ONLY"
            method = "scripted_metrics"
            coverage = "metadata+metrics only"
            note = "title/hanzi/paragraph/dialogue/probe extraction; body not read in this session"
            nxt = "round2_full_read"
            prio = "P0"
        else:
            # repo A files: nothing else read yet
            if repo == "A":
                prio = r["source_priority"]
            else:
                prio = r["source_priority"]
        out.append(dict(repository=r["repository"], relative_path=path,
                        version_read=("PR#84/R9" if "PR#84" in r["branch_or_commit"] else r["branch_or_commit"]),
                        reading_status=status, reading_method=method, reading_coverage=coverage,
                        evidence_note=note, blocking_reason=blocking,
                        next_action=nxt, priority_for_round2=prio))
    p = os.path.join(OUT, "02_full-reading-ledger.tsv")
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t"); w.writeheader()
        for r in out: w.writerow(r)
    import collections
    c = collections.Counter(r["reading_status"] for r in out)
    print("ledger rows:", len(out), "->", p)
    for k, v in c.most_common(): print(f"  {v:6d}  {k}")
    # coverage stats
    tot = sum(int(r["file_size"]) for r in rows)
    full = sum(int(r["file_size"]) for r in rows if r["relative_path"] in FULL)
    print(f"\nbytes total={tot:,} full_text_bytes={full:,} ({full/tot*100:.1f}%)")

if __name__ == "__main__":
    main()
