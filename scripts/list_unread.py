# -*- coding: utf-8 -*-
import json
from pathlib import Path

studio = Path(r"D:\The Memory\NovelStudio_Grok47")
close = set()
for line in (studio / "private_index" / "read_receipts.jsonl").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    row = json.loads(line)
    cov = row.get("coverage") or ""
    if cov.startswith("close-read") or "fact-card" in cov:
        close.add(row.get("relative_path"))

want = []
for line in (studio / "private_index" / "inventory.jsonl").read_text(encoding="utf-8").splitlines():
    row = json.loads(line)
    if row.get("kind") != "md" or row.get("origin_class") == "AI_DRAFT":
        continue
    rel = row["relative_path"]
    top = rel.split("/", 1)[0]
    if top.startswith(".") or top in {"scripts", "tmp", "写作体系"}:
        continue
    if rel in close:
        continue
    if any(rel.startswith(p) for p in (
        "背景资料/", "问卷回收/", "私人资料/", "文化与审美/",
        "高中/2025届/人物/", "高中/G2204/人物/", "大学/",
    )):
        want.append((row.get("hanzi") or 0, rel))

want.sort(reverse=True)
out = studio / "editorial" / "unread_priority.txt"
out.write_text("\n".join(f"{n}\t{rel}" for n, rel in want) + "\n", encoding="utf-8")
print("listed", len(want))
for n, rel in want[:40]:
    print(f"{n}\t{rel}")
