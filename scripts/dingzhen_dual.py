#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""顶针双判据 × 双指标 计数器（R6 裁决版）

作者裁决（2026-11-17）：保留两个不同指标，不得混在同一张表直接比较：
  - 顶针连接率 = 符合判据的相邻句对数 / 有效相邻句对数        【跨卷比较主指标】
  - 顶针参与句占比 = 参与≥1次顶针连接的句数 / 有效句数        【补充指标】

两套判据（口径不同，结果不可互换）：
  - A10   ：重合 ≥2 字，或 1 字（非停用）；不设最短句长限制
  - DZ    ：重合 ≥2 字且两句均≥4 字，或 1 字（非停用）  —— 即 scripts/dingzhen.py

句子切分：以 。！？ 切分（省略号并入句末），去标点空白后比较。
连续链：≥3 句靠顶针相连记为一条链，报最长链。
"""
import sys, os, re, glob, json

STOP=set("的了着过吗呢吧啊呀哦嗯这那是不在有和就都也很还又再才把被让给对从向往说要做会能可要只更最太真很没别吗吧呢")
def norm(s):
    s=re.sub(r'[^\u4e00-\u9fff]','',s)
    return s
def is_link(prev, nxt, mode):
    if not prev or not nxt: return False
    if mode=='A10':
        if len(prev)>=2 and len(nxt)>=2 and nxt[0:2]==prev[-2:]: return True
        return len(prev)>=1 and len(nxt)>=1 and nxt[0]==prev[-1] and nxt[0] not in STOP
    else:  # DZ
        if len(prev)>=4 and len(nxt)>=4 and nxt[0:2]==prev[-2:]: return True
        return len(prev)>=1 and len(nxt)>=1 and nxt[0]==prev[-1] and nxt[0] not in STOP
def stats(text, mode):
    # 按段落处理：段内切句
    paras=[p for p in re.split(r'\n\s*\n', text) if p.strip()]
    pairs=links=sents=part=0; maxchain=0; chains=0
    for p in paras:
        if p.strip().startswith('#') or p.strip().startswith('|') or p.strip().startswith('>'): continue
        raw=re.split(r'(?<=[。！？])', p)
        ss=[norm(x) for x in raw]
        ss=[x for x in ss if len(x)>=1]
        if len(ss)<2: 
            sents+=len(ss); continue
        sents+=len(ss)
        involved=[False]*len(ss)
        cur=0
        for i in range(len(ss)-1):
            pairs+=1
            if is_link(ss[i], ss[i+1], mode):
                links+=1; involved[i]=True; involved[i+1]=True; cur+=1
            else:
                if cur>=2: chains+=1; maxchain=max(maxchain,cur+1)
                cur=0
        if cur>=2: chains+=1; maxchain=max(maxchain,cur+1)
        part+=sum(involved)
    return dict(pairs=pairs, links=links, conn=links/pairs if pairs else 0,
                sents=sents, part=part, partr=part/sents if sents else 0,
                chains=chains, maxchain=maxchain)
def read(p):
    return open(p,encoding='utf-8',errors='replace').read()
def body_files():
    out=[]
    for v in range(1,7):
        d=f'manuscript/volume-{v:02d}'
        for f in sorted(glob.glob(d+'/*.md')):
            b=os.path.basename(f)
            if re.fullmatch(r'\d{3}\.md',b): out.append((v,b,f))
    for f in sorted(glob.glob('work/m09/volume-07/*.md')):
        b=os.path.basename(f)
        if re.fullmatch(r'\d{3}\.md',b): out.append((7,b,f))
    return out
if __name__=='__main__':
    rows=[]
    for v,b,f in body_files():
        t=read(f)
        a=stats(t,'A10'); d=stats(t,'DZ')
        rows.append(dict(vol=v, ch=b[:3], a10_conn=round(a['conn']*100,1), a10_part=round(a['partr']*100,1),
                         dz_conn=round(d['conn']*100,1), dz_part=round(d['partr']*100,1),
                         dz_maxchain=d['maxchain'], chars=len(norm(t))))
    # 汇总
    import statistics as st
    print(f'{"卷":>3}{"章数":>5}{"A10连接率":>11}{"A10参与句":>11}{"DZ连接率":>10}{"DZ参与句":>10}{"DZ最长链":>9}')
    for v in range(1,8):
        rs=[r for r in rows if r['vol']==v]
        if not rs: continue
        print(f'{v:>3}{len(rs):>5}{st.mean(r["a10_conn"] for r in rs):>11.1f}{st.mean(r["a10_part"] for r in rs):>11.1f}'
              f'{st.mean(r["dz_conn"] for r in rs):>10.1f}{st.mean(r["dz_part"] for r in rs):>10.1f}{max(r["dz_maxchain"] for r in rs):>9}')
    os.makedirs('editorial/final-readiness/F00-stats',exist_ok=True)
    import csv
    with open('editorial/final-readiness/F00-stats/dingzhen-dual.tsv','w',encoding='utf-8',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(rows[0].keys()),delimiter='\t')
        w.writeheader(); [w.writerow(r) for r in rows]
    print(f'\n已写 editorial/final-readiness/F00-stats/dingzhen-dual.tsv（{len(rows)} 章）')
