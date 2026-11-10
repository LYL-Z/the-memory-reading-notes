# -*- coding: utf-8 -*-
"""HY4 补丁4：删去对 II-004:57 的逐项重拍；补两张有据的相册物证。"""
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


OLD_HOUSE = (
    "父亲后来说，那间屋子是二〇〇三年重新盖起来的。拆旧房、请工、买材料、看材料、"
    "给干活的人做饭、留意养护，前后忙了差不多一年，都是她一个人在家里张罗。"
    "那一年我还没有出生。我小时候进去过许多回，只当屋子本来就在那里；"
    "屋檐有多高、墙是哪一年立起来的，跟我一点关系也没有。"
    "她要操心的另有一串事，父亲报得出名目，我一样也没赶上：拆、请、买、看、做饭、养护，"
    "一件接着一件。那不是替谁准备的过年地方，是一间屋子立起来的次序。"
)

NEW_TABLE = (
    "母亲的相册里另有一张，光线很暗，是餐馆里的一桌人，中间还抱着个婴儿。"
    "它不在春节那一组，是二〇一二年九月。我这些年一直往春节那几张后面翻，"
    "想找一张坐满人的饭桌；原来另有一张，只是换了年份，也换了一群人。"
    "我把那张看了两遍，认不出谁是谁，连自己在不在里头都说不准。"
    "它比我记得的任何一顿都更像一顿饭，偏偏不是过年。"
)

REPS = [
    # 1 删去对 004:57「拆旧房、请师傅、买材料、看材料、做饭、养护、约一年」的逐项重拍
    (OLD_HOUSE, NEW_TABLE),
    # 2 补 2013-11 奥林匹克公园：母亲怀抱何沛泽 + 身份待核的条纹衣女孩
    (
        "母亲把他的婴儿照单独收在一处，和我的那些放在不同的地方。到二〇二六年，他该上初中三年级了；这些年我见过他几回，说不准。",
        "母亲把他的婴儿照单独收在一处，和我的那些放在不同的地方。"
        "二〇一三年十一月的奥林匹克公园那一组里，她还抱着一个婴儿，大约就是他；"
        "另一张上，我和一个穿条纹衣的女孩一同爬攀爬架，她的名字至今没有对上。"
        "同一年的相册，有的孩子还被抱着，有的已经能自己爬上去。"
        "到二〇二六年，他该上初中三年级了；这些年我见过他几回，说不准。",
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
