# -*- coding: utf-8 -*-
"""HY4 补丁7：最后两处文字接缝——避开 II-004:9 的称呼重演、修双分号。"""
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
    (
        "母亲那本相册里还有一个相册，叫“我的侄子”。",
        "母亲那些相册里有一个，叫“我的侄子”。",
    ),
    (
        "奶奶在乡下还有别的叫法，我一直只叫她奶奶，从没问过哪一个是先有的。一个人在好几处被叫着，我小时候一点也不觉得奇怪；轮到自己被九班的人喊“主席”，倒想了很久。",
        "一个人有几处叫法，我小时候一点也不觉得奇怪。大人在这一处叫她这个，在另一处叫她那个，我只学会其中一个就够了。轮到自己被九班的人喊“主席”，倒想了很久。",
    ),
    (
        "记得的是照片外头总得有人腾出手来；至于按完以后谁先走，我没有问过。",
        "记得的是照片外头总得有人腾出手来。至于按完以后谁先走，我没有问过。",
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
