#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V6 顶针率实测脚本（HY-A09 自写，可复算）

口径（与 R2 实测一致，误差 ≤0.2pt）：
1) 去标题行；以 。！？!?… 切句；去所有非汉字字符。
2) 只保留长度 >= 3 汉字的句子。
3) 相邻两句 prev[-2:] == next[:2] 记一次顶针连接（只计双字）。
4) 连接率 = 连接数 / (n-1)。
5) 长全链段 = 段落 >200 汉字且段内连接率 >=50%（故障段代理指标）。
6) 候选稿遇独立成行的 --- 即截断，附录不计入。

用法：
    python dingzhen_v6.py <file.md> [...]
    python dingzhen_v6.py --json <file.md>
"""
import json
import os
import re
import sys

HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


def strip_headings(text):
    body = []
    for l in text.split("\n"):
        if l.strip() == "---":
            break
        body.append(l)
    return "\n".join(l for l in body if not l.startswith("#"))


def clean(s):
    return "".join(HAN.findall(s))


def split_sents(text):
    parts = re.split(r"[。！？!?…]+", text)
    return [c for c in (clean(p) for p in parts) if len(c) >= 3]


def paragraphs(text):
    out = []
    for block in re.split(r"\n\s*\n", text):
        n = len(clean(block))
        if n:
            out.append((n, block))
    return out


def chain_len(flags):
    best = cur = 0
    for f in flags:
        cur = cur + 1 if f else 0
        best = max(best, cur)
    return best


def analyze(path):
    text = open(path, encoding="utf-8").read()
    body = strip_headings(text)
    sents = split_sents(body)
    n = len(sents)
    flags = [sents[i][-2:] == sents[i + 1][:2] for i in range(n - 1)]
    cnt = sum(flags)
    paras = paragraphs(body)
    long_chain = 0
    for size, block in paras:
        if size <= 200:
            continue
        s = split_sents(block)
        if len(s) < 4:
            continue
        f = [s[i][-2:] == s[i + 1][:2] for i in range(len(s) - 1)]
        if sum(f) / len(f) >= 0.5:
            long_chain += 1
    return dict(
        path=path,
        hanzi=len(HAN.findall(body)),
        sents=n,
        links=cnt,
        rate=round(cnt / max(n - 1, 1) * 100, 1),
        longest=chain_len(flags),
        paras=len(paras),
        over400=sum(1 for x, _ in paras if x > 400),
        max_para=max((x for x, _ in paras), default=0),
        long_chain_paras=long_chain,
    )


def main(argv):
    files = [a for a in argv if not a.startswith("--")]
    rows = [analyze(p) for p in files]
    if "--json" in argv:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    print("file\thanzi\tsents\tlinks\trate%\tlongest\tparas\tover400\tmax_para\tlong_chain")
    for r in rows:
        print(
            "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                os.path.basename(os.path.dirname(r["path"])) + "/" + os.path.basename(r["path"]),
                r["hanzi"], r["sents"], r["links"], r["rate"], r["longest"],
                r["paras"], r["over400"], r["max_para"], r["long_chain_paras"],
            )
        )


if __name__ == "__main__":
    main(sys.argv[1:])
