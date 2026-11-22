# -*- coding: utf-8 -*-
"""QA 引文核验 v3：只检验**紧贴**引用的引文（`x.md:12`（「…」） 或 `x.md:12`「…」），
避免把代理自己的评述句误判成引文。用法: python qa/quotecheck.py [文件...]"""
import re, os, sys, glob
FACT = r"D:/The Memory/The Memory"; WRITE = r"D:/The Memory/tmp/reading-notes-review"
ADJ = re.compile(r'`([^`\n]*?\.md):(\d+(?:[-,–]\d+)*)`[）)]?[：:]?[（(]?[「“]([^」”]{4,90})[」”]')
def norm(s):
    s = re.sub(r'\*\*|__|`', '', s)
    return re.sub(r'[\s　]', '', s)
def resolve(p, mapping):
    p = p.strip()
    if '...' in p or '…' in p: return None
    for r in (FACT, WRITE):
        f = os.path.join(r, p)
        if os.path.isfile(f): return f
    base = os.path.basename(p)
    m = re.match(r'^(\d{3})\.md$', base); mv = re.search(r'V(\d{2})-(\d{3})', os.path.basename(mapping))
    if m and mv and m.group(1) == mv.group(2):
        v = int(mv.group(1))
        c = f"{WRITE}/manuscript/volume-0{v}/{base}" if v <= 6 else f"{WRITE}/work/m09/volume-07/{base}"
        if os.path.isfile(c): return c
    h = [x for x in glob.glob(FACT + "/**/" + base, recursive=True) + glob.glob(WRITE + "/**/" + base, recursive=True)
         if "私人资料" not in x and "lover-best" not in x]
    return h[0] if len(h) == 1 else None
def segs(q):
    return [norm(x) for x in re.split(r'[…\.]{1,6}', q) if len(norm(x)) >= 4]
def main(files):
    tot = hit = bad = 0; rows = []
    for f in files:
        for i, line in enumerate(open(f, encoding='utf-8').read().split('\n'), 1):
            for m in ADJ.finditer(line):
                fp = resolve(m.group(1), f)
                if not fp: continue
                tot += 1
                body = norm(open(fp, encoding='utf-8').read())
                ss = segs(m.group(3))
                if not ss: continue
                miss = [s for s in ss if s not in body]
                if miss:
                    bad += 1
                    rows.append((os.path.basename(f), i, m.group(1) + ':' + m.group(2), m.group(3), miss[0]))
                else:
                    hit += 1
    for r in rows:
        print(f"[未命中] {r[0]}:{r[1]}  {r[2]}\n    原句「{r[3]}」\n    缺  「{r[4][:38]}」")
    print(f"\n紧贴引文合计 {tot}；命中 {hit}；未命中 {bad}（命中率 {hit/max(tot,1)*100:.1f}%）")
if __name__ == '__main__':
    main(sys.argv[1:] or sorted(glob.glob('editorial/full-corpus-readiness/bidirectional-mapping/volume-*/*.md')))
