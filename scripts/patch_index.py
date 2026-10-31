# -*- coding: utf-8 -*-
import json
import sqlite3
from datetime import datetime
from pathlib import Path

studio = Path(r"D:\The Memory\NovelStudio_Grok47")
db = sqlite3.connect(studio / "private_index" / "vault.db")

root_md = [
    r[0]
    for r in db.execute(
        """
        select relative_path from files
        where instr(relative_path, '/')=0 and extension='.md'
        """
    )
]
print("root_md", root_md)
db.execute(
    """
    update files
    set origin_class='MIXED', origin_hint='vault_root_index'
    where instr(relative_path, '/')=0 and extension='.md'
    """
)

cur = db.execute(
    """
    delete from docs_fts
    where path like '写作体系/%'
       or path like '高中/素材/文学化推演/%'
    """
)
print("fts_removed", cur.rowcount)
db.commit()

inv = studio / "private_index" / "inventory.jsonl"
tmp = studio / "private_index" / "inventory.jsonl.tmp"
changed = 0
with inv.open(encoding="utf-8") as src, tmp.open("w", encoding="utf-8") as dst:
    for line in src:
        row = json.loads(line)
        rel = row["relative_path"]
        if "/" not in rel and rel.endswith(".md"):
            row["origin_class"] = "MIXED"
            row["origin_hint"] = "vault_root_index"
            changed += 1
        if rel.startswith("写作体系/") or rel.startswith("高中/素材/文学化推演/"):
            row["read_receipt"]["coverage"] = "hashed-counted-removed-from-fts"
            row["parse_status"] = "有意排除"
        dst.write(json.dumps(row, ensure_ascii=False) + "\n")
tmp.replace(inv)
print("jsonl_root_retagged", changed)

sizes = db.execute(
    """
    select relative_path, size, hanzi from files
    where relative_path in (
      '高中/G2204/人物/同学/刘佑林.md',
      '家庭/人物/父亲.md',
      '家庭/人物/母亲.md',
      '高中/G2204/人物/同学/赵问竹.md',
      '初中/2022届/素材/升学/2022中考至麓山国际入学时间线-刘佑林回忆.md'
    )
    """
).fetchall()
for row in sizes:
    print("size", row)
db.close()
