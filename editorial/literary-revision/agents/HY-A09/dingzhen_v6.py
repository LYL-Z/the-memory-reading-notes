#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V6 顶针率实测脚本（HY-A09 自写，可复算）

口径（与 team-lead 的 R2 实测口径对齐，允许 ±0.5pt 误差）：
1) 去掉标题行；以 。！？!?… 切句；去掉所有非汉字字符得到纯汉字串。
2) 只保留长度 >= 3 汉字的句子（过短句不参与，避免「嗯。」这类对白污染分母）。
3) 相邻两句 i / i+1 记一次「顶针连接」，当且仅当 prev[-2:] == next[:2]。
4) 连接率 = 连接数 / 相邻句对数（n-1）。
5) 另报：参与顶针的句数占比、最长连续链、正文汉字数、
   段落汉字长度分布（>400 字段落数、最长段）。

用法：
    python dingzhen_v6.py <file.md> [<file.md> ...]
    python dingzhen_v6.py --json <file.md>
"""
import json
import os
import re
import sys

HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


def strip_headings(text):
    """只取候选稿的正文：标题行去掉；遇到独立成行的 --- 即截断（其后为交稿附录）。"""
    lines = text.split("\n")
    body = []
    for l in lines:
        if l.strip() == "---":
            break
        body.append(l)
    return "\n".join(l for l in body if not l.startswith("#"))


def clean(s):
    return "".join(HAN.findall(s))


def split_sents(text):
    parts = re.split(r"[。！？!?…]+", strip_headings(text))
    return [c for c in (clean(p) for p in parts) if len(c) >= 3]


def paragraphs(text):
    out = []
    for block in re.split(r"\n\s*\n", strip_headings(text)):
        n = len(clean(block))
        if n:
            out.append(n)
    return out


def hanzi(text):
    return len(HAN.findall(strip_headings(text)))


def chain_len(flags):
    best = cur = 0
    for f in flags:
        cur = cur + 1 if f else 0
        best = max(best, cur)
    return best


def analyze(path):
    text = open(path, encoding="utf-8").read()
    sents = split_sents(text)
    n = len(sents)
    flags = [
        sents[i][-2:] == sents[i + 1][:2] for i in range(n - 1)
    ]
    cnt = sum(flags)
    pairs = max(n - 1, 1)
    involved = set()
    for i, f in enumerate(flags):
        if f:
            involved.update((i, i + 1))
    paras = paragraphs(text)
    return dict(
        path=path,
        hanzi=hanzi(text),
        sents=n,
        links=cnt,
        rate=round(cnt / pairs * 100, 1),
        inv_rate=round(len(involved) / max(n, 1) * 100, 1),
        longest=chain_len(flags),
        paras=len(paras),
        over400=sum(1 for p in paras if p > 400),
        max_para=max(paras) if paras else 0,
    )


def main(argv):
    as_json = "--json" in argv
    files = [a for a in argv if not a.startswith("--")]
    rows = [analyze(p) for p in files]
    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    header = "file\thanzi\tsents\tlinks\trate%\tinvolved%\tlongest\tparas\tover400\tmax_para"
    print(header)
    for r in rows:
        print(
            "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                os.path.basename(os.path.dirname(r["path"])) + "/" + os.path.basename(r["path"]),
                r["hanzi"], r["sents"], r["links"], r["rate"], r["inv_rate"],
                r["longest"], r["paras"], r["over400"], r["max_para"],
            )
        )


if __name__ == "__main__":
    main(sys.argv[1:])
