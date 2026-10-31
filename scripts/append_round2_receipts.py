# -*- coding: utf-8 -*-
import json
from datetime import datetime
from pathlib import Path

p = Path(r"D:\The Memory\NovelStudio_Grok47\private_index\read_receipts.jsonl")
now = datetime.now().astimezone().isoformat(timespec="seconds")
items = [
    ("高中/素材/个人回忆/竹林杯与高一关系变淡-2026-08-28.md", "close-read-full"),
    ("高中/素材/个人回忆/刘佑林口述-选科强基住宿同桌外号-2026-09-12.md", "close-read-full"),
    ("高中/素材/个人回忆/麓山国际作息时间-用户提供-2026-09-12.md", "close-read-full"),
    ("高中/素材/个人回忆/刘佑林关于赵问竹的高中回忆-2026-08-12.md", "close-read-full"),
    ("高中/素材/个人回忆/高二下暑假沪浙之行-2024.md", "close-read-full"),
    ("高中/素材/个人回忆/五一西安之行-母亲与赵问竹-2026.md", "close-read-full"),
    ("高中/素材/个人回忆/新加坡之行-2026.md", "close-read-itinerary-oral-boundary-certificate-note"),
    ("高中/G2204/G2204高一入学、分组与寝室时间线.md", "close-read-full"),
    ("高中/2025届/G2205班-学生职务与小组变动.md", "close-read-full"),
    ("高中/素材/同学回忆/赵问竹关于刘佑林的书面评价.md", "close-read-full"),
    ("高中/素材/同学回忆/阳隽豪关于刘佑林的书面回忆.md", "close-read-full"),
    ("家庭/人物/父亲.md", "close-read-gap-180-269"),
    ("家庭/人物/母亲.md", "close-read-gap-145-273"),
    ("高中/2025届/人物/学生/王麒睿.md", "close-read-lines-120-229"),
    ("项目管理/全库缺口与审计总台账-2026-09-04.md", "close-read-opening-consent-and-2026-09-11-section"),
]
with p.open("a", encoding="utf-8") as f:
    for rel, coverage in items:
        f.write(json.dumps({
            "relative_path": rel,
            "coverage": coverage,
            "processor": "phase1-human-close-read-round2",
            "time": now,
        }, ensure_ascii=False) + "\n")
print(len(items))
