#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""顶针链式句计数器（M06 自定义判据，可复算）

判据（写死在这里，避免事后调整）：
1) 以 。！？ 切句（不含分号；省略号按 。 处理），去掉所有标点与空白后得到纯字串。
2) 相邻两句 i, i+1 构成一个「顶针连接」，当且仅当：
   next[0:2] == prev[-2:]  且 prev 长度>=4 且 next 长度>=4   （双字顶针）
   或 next[0:1] == prev[-1:] 且该字不在停用字表（单字顶针，如「疼。疼」）
3) 顶针率 = 顶针连接数 / 相邻句对数；另报「参与顶针的句数 / 总句数」。
4) 连续段：连续 >=3 句都靠顶针相连，记为一个「链」，报最长链长度。
用法：python scripts/dingzhen.py <file> [<file> ...]
"""
import re, sys, os

STOP1 = set("的了是在有和就不也都而很又还这那我你他她它个一上下来去到说")

def clean(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s)

def split_sents(text):
    # 去标题行与 frontmatter
    lines = [l for l in text.split("\n") if not l.startswith("#")]
    body = "\n".join(lines)
    parts = re.split(r"[。！？!?…]+", body)
    out = []
    for p in parts:
        c = clean(p)
        if len(c) >= 2:
            out.append(c)
    return out

def analyze(path):
    text = open(path, encoding="utf-8").read()
    sents = split_sents(text)
    n = len(sents)
    links = []
    for i in range(n - 1):
        a, b = sents[i], sents[i + 1]
        hit = None
        if len(a) >= 4 and len(b) >= 4 and a[-2:] == b[:2]:
            hit = ("2", a[-2:])
        elif a[-1] == b[0] and a[-1] not in STOP1 and len(a) >= 3 and len(b) >= 3:
            hit = ("1", a[-1])
        links.append(hit)
    pairs = max(n - 1, 1)
    cnt = sum(1 for x in links if x)
    # 最长链（连续命中）
    best = cur = 0
    for x in links:
        if x:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    # 参与顶针的句数
    involved = set()
    for i, x in enumerate(links):
        if x:
            involved.add(i); involved.add(i + 1)
    return dict(path=path, sents=n, links=cnt, rate=cnt / pairs * 100,
                involved=len(involved), inv_rate=len(involved) / n * 100, longest=best)

if __name__ == "__main__":
    rows = [analyze(p) for p in sys.argv[1:]]
    print("file\tsents\tlinks\trate%\tinvolved\tinv_rate%\tlongest_chain")
    for r in rows:
        print(f"{os.path.basename(os.path.dirname(r['path']))}/{os.path.basename(r['path'])}\t{r['sents']}\t{r['links']}\t{r['rate']:.1f}\t{r['involved']}\t{r['inv_rate']:.1f}\t{r['longest']}")
