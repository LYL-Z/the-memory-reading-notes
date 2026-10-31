# -*- coding: utf-8 -*-
import json
from collections import Counter
from pathlib import Path

studio = Path(r"D:\The Memory\NovelStudio_Grok47")
inv = studio / "private_index" / "inventory.jsonl"
receipts = studio / "private_index" / "read_receipts.jsonl"

close = set()
if receipts.exists():
    for line in receipts.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        cov = row.get("coverage") or ""
        if cov.startswith("close-read") or cov.startswith("fact-card"):
            close.add(row.get("relative_path"))

life = []
by_top = Counter()
unread_top = Counter()
for line in inv.read_text(encoding="utf-8").splitlines():
    row = json.loads(line)
    if row.get("kind") != "md":
        continue
    if row.get("origin_class") == "AI_DRAFT":
        continue
    rel = row["relative_path"]
    top = rel.split("/", 1)[0]
    if top.startswith(".") or top in {"scripts", "tmp"}:
        continue
    life.append(rel)
    by_top[top] += 1
    if rel not in close:
        unread_top[top] += 1

print("life_md", len(life))
print("close_paths", len(close))
print("unread", sum(unread_top.values()))
print("--- unread by folder ---")
for k, v in unread_top.most_common():
    print(f"{v}\t{by_top[k]}\t{k}")
