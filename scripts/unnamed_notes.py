# -*- coding: utf-8 -*-
"""List life markdown not named in fact cards or close-read receipts."""
import json
from pathlib import Path

root = Path(r"D:\The Memory\The Memory")
studio = Path(r"D:\The Memory\NovelStudio_Grok47")
mentioned = set()
for line in (studio / "private_index" / "read_receipts.jsonl").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    row = json.loads(line)
    rel = row.get("relative_path") or ""
    if rel:
        mentioned.add(rel.replace("\\", "/"))

blob = []
for path in (studio / "editorial" / "fact_cards").glob("*.md"):
    blob.append(path.read_text(encoding="utf-8"))
text = "\n".join(blob)

life = []
for line in (studio / "private_index" / "inventory.jsonl").read_text(encoding="utf-8").splitlines():
    row = json.loads(line)
    if row.get("kind") != "md":
        continue
    rel = row["relative_path"]
    top = rel.split("/", 1)[0]
    if top.startswith(".") or top in {"scripts", "tmp"}:
        continue
    life.append((row.get("origin_class"), row.get("hanzi") or 0, rel))

unread = []
for origin, hanzi, rel in life:
    name = Path(rel).name
    if rel in mentioned or name in text or rel in text:
        continue
    unread.append((origin, hanzi, rel))

out = studio / "editorial" / "仍未点名的笔记.txt"
lines = [f"{origin}\t{hanzi}\t{rel}" for origin, hanzi, rel in unread]
out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
print("life", len(life), "unnamed", len(unread))
from collections import Counter
c = Counter(rel.split("/", 1)[0] for _, _, rel in unread)
for k, v in c.most_common():
    print(f"{v}\t{k}")
