# -*- coding: utf-8 -*-
import json
import sqlite3
from datetime import datetime
from pathlib import Path

studio = Path(r"D:\The Memory\NovelStudio_Grok47")
db = sqlite3.connect(studio / "private_index" / "vault.db")
cur = db.execute(
    """
    update files
    set parse_status='有意排除'
    where relative_path like '写作体系/%'
       or relative_path like '高中/素材/文学化推演/%'
    """
)
db.commit()
print("sql_updated", cur.rowcount)
print("fts_left", db.execute("select count(*) from docs_fts").fetchone()[0])
db.close()

receipts = studio / "private_index" / "read_receipts.jsonl"
now = datetime.now().astimezone().isoformat(timespec="seconds")
items = [
    ("00-知识库首页.md", "close-read-full"),
    ("时间线索引.md", "close-read-full"),
    ("知识库架构总览.md", "close-read-full"),
    ("人物总索引.md", "close-read-full"),
    ("背景资料/维度专页/刘佑林年龄-时代对应.md", "close-read-full"),
    ("小学/小学阶段人物与素材索引.md", "close-read-full"),
    ("初中/初中阶段人物与素材索引.md", "close-read-full"),
    ("高中/高中阶段人物与素材索引.md", "close-read-full"),
    ("大学/大学阶段人物与素材索引.md", "close-read-full"),
    ("家庭/家庭资料索引.md", "close-read-full"),
    ("初中/2022届/素材/升学/2022中考至麓山国际入学时间线-刘佑林回忆.md", "close-read-full"),
    ("项目管理/用户订正-2026-08-28-证据口径与姓名校勘.md", "close-read-full"),
    ("项目管理/用户订正-2026-09-11-事实优先与有界推演.md", "close-read-full"),
    ("项目管理/用户订正-2026-09-11-长篇调用私密层.md", "close-read-full"),
    ("项目管理/用户订正-2026-09-12-书名刘佑林的19年回忆录.md", "close-read-full"),
    ("项目管理/用户订正-2026-09-12-小红帽江安茶西安怕黑.md", "close-read-full"),
    ("项目管理/用户订正-2026-09-12-待补答复按场.md", "close-read-full"),
    ("项目管理/用户订正-2026-09-12-第一人称可推断可替想.md", "close-read-full"),
    ("项目管理/用户订正-2026-09-12-选科强基作息同桌并置.md", "close-read-full"),
    ("高中/G2204/人物/同学/刘佑林.md", "close-read-body"),
    ("高中/G2204/人物/同学/赵问竹.md", "close-read-lines-32-201"),
    ("家庭/人物/父亲.md", "close-read-lines-33-182-and-250-269"),
    ("家庭/人物/母亲.md", "close-read-lines-31-150-and-255-273"),
]
with receipts.open("a", encoding="utf-8") as f:
    for rel, coverage in items:
        f.write(json.dumps({
            "relative_path": rel,
            "coverage": coverage,
            "processor": "phase1-human-close-read",
            "time": now,
            "note": "Semantic reading in the 2026-10-31 session. Not a substitute for the hash receipt.",
        }, ensure_ascii=False) + "\n")
print("receipts", len(items))
