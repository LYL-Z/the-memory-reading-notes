# -*- coding: utf-8 -*-
import json
from collections import Counter
from pathlib import Path

studio = Path(r"D:\The Memory\NovelStudio_Grok47")
text = "\n".join(p.read_text(encoding="utf-8") for p in (studio / "editorial").rglob("*.md"))
receipts = (studio / "private_index" / "read_receipts.jsonl").read_text(encoding="utf-8")

rows = []
for line in (studio / "private_index" / "inventory.jsonl").read_text(encoding="utf-8").splitlines():
    row = json.loads(line)
    if row.get("kind") != "md":
        continue
    rel = row["relative_path"]
    top = rel.split("/", 1)[0]
    if top.startswith(".") or top in {"scripts", "tmp"}:
        continue
    hit = rel in text or rel in receipts or rel.replace("/", "\\") in text
    rows.append((hit, row.get("origin_class"), row.get("hanzi") or 0, rel))

unread = [r for r in rows if not r[0]]
print("md", len(rows), "path-cited", len(rows) - len(unread), "not-cited", len(unread))
c = Counter(rel.split("/", 1)[0] for _, _, _, rel in unread)
for k, v in c.most_common():
    print(f"{v}\t{k}")
print("--- sample ---")
for item in unread[:30]:
    print(item[1], item[2], item[3])
Path(studio / "editorial" / "路径未引用的笔记.txt").write_text(
    "\n".join(f"{o}\t{n}\t{rel}" for _, o, n, rel in unread) + "\n",
    encoding="utf-8",
)
