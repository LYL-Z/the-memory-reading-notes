# -*- coding: utf-8 -*-
"""HY4 补丁6：补祖母「我出生前屋子已立好」与父亲幺儿排行，不重演 II-004 工序清单。"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH16 = os.path.join(ROOT, "manuscript", "volume-02", "016.md")


def read(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write(p, t):
    t = t.replace("\r\n", "\n").replace("\n", "\r\n")
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)


REPS = [
    # 1 补「屋子在我出生前已立好」——不列 004:57 已写过的拆/请/买/看/做饭/养护
    (
        "等我回城了，菜还得种，猪还得喂。\r\n\r\n",
        "等我回城了，菜还得种，猪还得喂。\r\n\r\n"
        "那间屋子也不是一直就在那里。父亲说过一个年份，比我出生早四年；"
        "那一年他还没把我带回家，屋已经先立起来了，是奶奶一个人在乡下张罗的。"
        "我小时候进去过许多回，只当墙和屋檐本来就有，从没想过它也有一个盖成的日子。"
        "屋子的年份和人的年份挨在一起，我却是隔了许多年才把这两件事排到一处。\r\n\r\n",
    ),
    # 2 补父亲排行，强化「次序不是我排的」
    (
        "大人们在我出生前就有自己的排行、婚姻和来往；我一出生，张口便能把这一切叫成我的亲戚。",
        "大人们在我出生前就有自己的排行、婚姻和来往：父亲是幺儿，上头两个姐姐，"
        "一个去了很远的地方，一个留在益阳。我一出生，张口便能把这一切叫成我的亲戚。",
    ),
]


def main():
    t = read(CH16)
    miss = []
    for old, new in REPS:
        n = t.count(old)
        if n != 1:
            miss.append((old[:46], n))
            continue
        t = t.replace(old, new, 1)
    write(CH16, t)
    print("016.md: applied %d/%d" % (len(REPS) - len(miss), len(REPS)))
    for m in miss:
        print("  MISS count=%d : %s" % (m[1], m[0]))
    sys.exit(1 if miss else 0)


if __name__ == "__main__":
    main()
