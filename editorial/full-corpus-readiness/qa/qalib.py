# -*- coding: utf-8 -*-
"""QA 公共库：两仓索引 + 引用解析（统一口径）"""
import os, re
FACT = r"D:/The Memory/The Memory"; WRITE = r"D:/The Memory/tmp/reading-notes-review"
IDX = {}; BYBASE = {}
def build():
    if IDX: return
    for root in (FACT, WRITE):
        for dp, dn, fs in os.walk(root):
            if '.git' in dp or '私人资料' in dp or 'lover-best' in dp: continue
            for fn in fs:
                if not fn.endswith('.md'): continue
                p = os.path.join(dp, fn).replace('\\', '/')
                rel = os.path.relpath(p, root).replace('\\', '/')
                IDX[(root, rel)] = p; BYBASE.setdefault(fn, []).append(p)
def resolve(p, mapping):
    build()
    p = p.replace('\\', '/').strip()
    if '...' in p or '…' in p: return ('BAD', None)
    mv = re.search(r'V(\d{2})-(\d{3})', os.path.basename(mapping))
    if mv:
        v = int(mv.group(1)); base = os.path.basename(p)
        if re.match(r'^\d{3}\.md$', base) and base[:3] == mv.group(2):
            c = f"{WRITE}/manuscript/volume-0{v}/{base}" if v <= 6 else f"{WRITE}/work/m09/volume-07/{base}"
            if os.path.isfile(c): return ('OK', c)
    for root in (FACT, WRITE):
        if (root, p) in IDX: return ('OK', IDX[(root, p)])
    h = BYBASE.get(os.path.basename(p), [])
    if not h: return ('MISSING', None)
    if len(h) == 1: return ('OK', h[0])
    fact = [x for x in h if x.startswith(FACT)]
    return ('AMBIG', (fact or h)[0])
