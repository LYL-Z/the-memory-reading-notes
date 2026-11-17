# -*- coding: utf-8 -*-
"""QA 引文核验器 v3：建立两仓 .md 索引（一次 os.walk），解析 `path:line` 引用。
输出四类：OK / AMBIG(同名多份) / MISSING(查无此文件) / RANGE(行号越界)。
用法: python qa/citecheck.py [映射文件...]"""
import re, os, sys, glob
FACT = r"D:/The Memory/The Memory"; WRITE = r"D:/The Memory/tmp/reading-notes-review"
CITE = re.compile(r'`([^`\n]*?\.md):(\d+(?:[-,–]\d+)*)`')
IDX = {}; BYBASE = {}
def build():
    for root in (FACT, WRITE):
        for dp, dn, fs in os.walk(root):
            if '.git' in dp or '私人资料' in dp or 'lover-best' in dp: continue
            for fn in fs:
                if not fn.endswith('.md'): continue
                p = os.path.join(dp, fn).replace('\\', '/')
                rel = os.path.relpath(p, root).replace('\\', '/')
                IDX[(root, rel)] = p; BYBASE.setdefault(fn, []).append(p)
def resolve(p, mapping):
    p = p.replace('\\', '/').strip()
    if '...' in p or '…' in p: return ('BAD', None)
    for root in (FACT, WRITE):
        if (root, p) in IDX: return ('OK', IDX[(root, p)])
    base = os.path.basename(p)
    m = re.match(r'^(\d{3})\.md$', base); mv = re.search(r'V(\d{2})-(\d{3})', os.path.basename(mapping))
    if m and mv and m.group(1) == mv.group(2):
        v = int(mv.group(1)); c = f"{WRITE}/manuscript/volume-0{v}/{base}" if v <= 6 else f"{WRITE}/work/m09/volume-07/{base}"
        if os.path.isfile(c): return ('OK', c)
    h = BYBASE.get(base, [])
    if len(h) == 1: return ('OK', h[0])
    if len(h) > 1: return ('AMBIG', h)
    return ('MISSING', None)
def nums(s):
    out = []
    for part in re.split(r'[,\s]+', s):
        m = re.match(r'(\d+)[-–](\d+)$', part)
        if m: out += list(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit(): out.append(int(part))
    return out
def main(files):
    build()
    T = dict(total=0, ok=0, ambig=0, missing=0, rng=0)
    for f in files:
        loc = dict(total=0, ok=0, ambig=0, missing=0, rng=0); probs = []
        for i, line in enumerate(open(f, encoding='utf-8').read().split('\n'), 1):
            for m in CITE.finditer(line):
                loc['total'] += 1; T['total'] += 1
                st, fp = resolve(m.group(1), f); ns = nums(m.group(2))
                if st == 'MISSING':
                    loc['missing'] += 1; T['missing'] += 1; probs.append(('MISSING', i, m.group(1) + ':' + m.group(2)))
                elif st == 'BAD':
                    loc['ambig'] += 1; T['ambig'] += 1; probs.append(('缩写路径', i, m.group(1)))
                elif st == 'AMBIG':
                    loc['ambig'] += 1; T['ambig'] += 1; probs.append(('同名多份', i, m.group(1)))
                else:
                    loc['ok'] += 1; T['ok'] += 1
                    if ns and max(ns) > len(open(fp, encoding='utf-8').read().split('\n')):
                        loc['rng'] += 1; T['rng'] += 1; probs.append(('行号越界', i, m.group(1) + ':' + m.group(2)))
        if probs:
            print(f"{os.path.basename(f):16s} 引用={loc['total']:4d} 缺失={loc['missing']} 含糊={loc['ambig']} 越界={loc['rng']}")
            for k, i, p in probs[:8]: print(f"    [{k}] 第{i}行 -> {p}")
    print(f"\n总计 引用={T['total']} 可定位={T['ok']} 文件缺失={T['missing']} 含糊={T['ambig']} 行号越界={T['rng']}")
if __name__ == '__main__':
    main(sys.argv[1:] or sorted(f for f in glob.glob('editorial/full-corpus-readiness/bidirectional-mapping/volume-*/*.md') if not os.path.basename(f).startswith('_')))
