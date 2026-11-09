# -*- coding: utf-8 -*-
"""HY4 修订补丁 2：CRLF 换行适配 + 补齐第四处年龄错误。"""
import io
import os
import sys

BASE = r"D:\The Memory\tmp\hy4-independent-review\manuscript\volume-02"

PATCH = {
    "002": [
        ("我可以很诚实地说出这层意思，也可以承认，当时的自己没那么诚实。\r\n\r\n", ""),
    ],
    "003": [
        ("我甚至可以列出三条听起来很周全的理由：舍不得同学，想要好班，不想耽误她复习。纸上要是有一道问答题，我多半能把它们答满。可我没有去前面，面前那本书也没因此多翻几页。\r\n\r\n", ""),
        ("留得最清楚的，是那个十六岁男生反反复复的念头", "留得最清楚的，是那个十五岁男生反反复复的念头"),
    ],
    "004": [
        ("我喜欢电影，可那不是我要写的她。\r\n\r\n", ""),
    ],
    "006": [
        ("这念头听起来有点悲伤。我知道自己很会把一件已经过去的事讲成很有意味的样子。\r\n\r\n", ""),
    ],
    "007": [
        ("那么多年以后再写这段暑假，我最不愿意做的事，就是用一本没写完的练习册，把先前那些真的做过的努力一笔勾销。\r\n\r\n", ""),
        ("它们不是两个人。\r\n\r\n", ""),
    ],
    "010": [
        ("一个人最容易和自己争的是：我知道我很能学，为什么眼下偏偏还差这一点？\r\n\r\n", ""),
        ("我没那么大方，能把成绩与友情从头到尾分得干干净净。\r\n\r\n", ""),
    ],
    "011": [
        ("“向睿馨！！！”\r\n\r\n三个感叹号，后面没有别的话。",
         "“我要给你打差评，我的名字。”\r\n\r\n就这一句，后面没有别的话。"),
        ("打完我没发现，倒是被写错的人自己来改。",
         "打完我没发现，倒是她自己看出来了。"),
    ],
}


def main():
    total, miss = 0, []
    for ch, reps in PATCH.items():
        path = os.path.join(BASE, ch + ".md")
        with io.open(path, "r", encoding="utf-8", newline="") as f:
            text = f.read()
        for i, (old, new) in enumerate(reps, 1):
            n = text.count(old)
            if n != 1:
                miss.append((ch, i, n, old[:36]))
                continue
            text = text.replace(old, new, 1)
            total += 1
        with io.open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        print("%s: %d replacements checked" % (ch, len(reps)))
    print("APPLIED =", total)
    if miss:
        print("MISSED:")
        for m in miss:
            print("  ", m)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
