#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T042: merge T037/T038/T030 deep-read results into read-records.tsv (idempotent)."""
import io, csv, os, collections

BASE = r"D:/The Memory/tmp/reading-notes-review/editorial/full-corpus-readiness"
LEDGER = os.path.join(BASE, "read-records", "read-records.tsv")
INV = os.path.join(BASE, "01_repository-inventory.tsv")
TMP = r"D:/The Memory/tmp/_a02"

FIELDS = ["file","repo","version","read_range","tool","segments","artifact","read_at","note"]

AG = {
 "T037": ("37", "agent-37", "parallel-execution/agents/agent-37/T037-person-cards-2.md"),
 "T038": ("38", "agent-38", "parallel-execution/agents/agent-38/T038-primary-sources.md"),
 "T030": ("30", "agent-30", "parallel-execution/agents/agent-30/T030-person-cards-1.md"),
}

REJECT = {
 "高中/素材/人物资料/赵问竹/赵问竹-影像形态与行为侧写-2026-08-28.md":
   "T037 §0 清单列出 1,660 汉字，但正文 23 张人物卡零引用、零短引、零行号——无任何可核验内容",
 "高中/素材/人物资料/赵问竹/赵问竹-18份影像与成长资料核验-2026-08-11.md":
   "T037 仅字段7表出现 1 条定位项「18 份影像与站位」，无具体影像内容/站位/短引，不足 3 条实质发现",
 "高中/素材/文学化推演/刘佑林与赵问竹的平行宇宙故事线-2026-08-15.md":
   "T037 仅 1 条实质发现（F-2b「年级第四」+ 行151），不足 3 条，建议回读补证",
}

def main():
    inv = {r["relative_path"]: r for r in csv.DictReader(io.open(INV, encoding="utf-8"), delimiter="\t")}
    lines = {p: int(n) for p, n in
             (l.rstrip("\n").split("\t") for l in io.open(os.path.join(TMP, "all.lines.tsv"), encoding="utf-8") if l.strip())}
    hashes = {}
    ps = [l.rstrip("\n") for l in io.open(os.path.join(TMP, "all.txt"), encoding="utf-8") if l.strip()]
    hs = [l.strip() for l in io.open(os.path.join(TMP, "all.hash"), encoding="utf-8") if l.strip()]
    for p, h in zip(ps, hs):
        hashes[p] = h

    # source map: path -> list of task ids that substantively covered it
    src = collections.defaultdict(list)
    for task in ("T037", "T038", "T030"):
        for l in io.open(os.path.join(TMP, "f%s.txt" % task[1:].lstrip("0")), encoding="utf-8"):
            p = l.strip()
            if p and p not in REJECT:
                src[p].append(task)

    old = list(csv.DictReader(io.open(LEDGER, encoding="utf-8"), delimiter="\t"))
    header = io.open(LEDGER, encoding="utf-8").readline().rstrip("\n").split("\t")
    assert header == FIELDS, header
    have = {r["file"]: r for r in old}

    appended_art = []
    new_rows = []
    for p in sorted(src):
        tasks = src[p]
        seg = ";".join(AG[t][1] for t in tasks)
        art = ";".join(AG[t][2] for t in tasks)
        note = "merged-by-A02-from-" + "/".join(tasks)
        if p in have:
            r = have[p]
            add = [AG[t][0] for t in tasks if AG[t][0] not in r["artifact"].split("/")]
            if add:
                r["artifact"] = r["artifact"] + "/" + "/".join(add)
                appended_art.append((p, r["artifact"]))
            continue
        new_rows.append(dict(file=p, repo="A/the-memory",
                             version="master@ef33c98d/" + hashes[p][:12],
                             read_range="all %d lines" % lines[p],
                             tool="subagent-fulltext", segments=seg, artifact=art,
                             read_at="2026-11-15 round2", note=note))

    with io.open(LEDGER, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in old:
            w.writerow({k: r[k] for k in FIELDS})
        for r in new_rows:
            w.writerow(r)

    print("old rows:", len(old))
    print("new rows:", len(new_rows))
    print("total:", len(old) + len(new_rows))
    print("artifact appended on existing:", len(appended_art))
    for p, a in appended_art:
        print("   ", p, "->", a)
    print("rejected:", len(REJECT))
    print("source files unique (passed):", len(src))

if __name__ == "__main__":
    main()
