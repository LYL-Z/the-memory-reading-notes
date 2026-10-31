# -*- coding: utf-8 -*-
import hashlib
import sqlite3
from pathlib import Path

studio = Path(r"D:\The Memory\NovelStudio_Grok47")
db = sqlite3.connect(studio / "private_index" / "vault.db")
print("--- indexed text by top ---")
rows = db.execute(
    """
    select case when instr(relative_path, '/')=0 then '(root)'
                else substr(relative_path, 1, instr(relative_path, '/')-1) end as top,
           origin_class, count(*), sum(hanzi)
    from files
    where kind in ('md','txt') and parse_status='已提取'
    group by 1, 2
    order by 3 desc
    """
).fetchall()
for r in rows:
    print(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}")
print("--- ai by top ---")
for r in db.execute(
    """
    select case when instr(relative_path, '/')=0 then '(root)'
                else substr(relative_path, 1, instr(relative_path, '/')-1) end,
           count(*), sum(hanzi), sum(size)
    from files where origin_class='AI_DRAFT' group by 1
    """
):
    print(r)

ext_root = Path(r"D:\The Memory")
targets = []
serial = ext_root / "小说连载稿"
if serial.exists():
    targets.extend(p for p in serial.rglob("*") if p.is_file())
extra = ext_root / "刘佑林的19年回忆录_连载稿.txt"
if extra.exists():
    targets.append(extra)
lines = []
for p in targets:
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    rel = p.relative_to(ext_root).as_posix()
    lines.append(f"{digest}\t{p.stat().st_size}\t{rel}")
out = studio / "editorial" / "external_legacy_hashes.txt"
out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
print("external_files", len(lines), "bytes", sum(p.stat().st_size for p in targets))
