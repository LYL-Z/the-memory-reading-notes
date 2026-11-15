# -*- coding: utf-8 -*-
"""QA 引文核验器 v2：抽出 `path:line` 引用，并检验紧随其后的「…」引文是否真的在该文件里。
用法: python qa/quotecheck.py [映射文件...]
"""
import re, os, sys, glob

FACT = r"D:/The Memory/The Memory"
WRITE = r"D:/The Memory/tmp/reading-notes-review"
CITE = re.compile(r'`([^`\n]*?\.md):(\d+(?:[-,–]\d+)*)`')
QUOTE = re.compile(r'[「“]([^」”]{4,90})[」”]')

def norm(s):
    return re.sub(r'[\s　]', '', s)

def resolve(p, mapping):
    p = p.strip()
    if '...' in p or '…' in p:
        return None
    for root in (FACT, WRITE):
        f = os.path.join(root, p)
        if os.path.isfile(f):
            return f
    base = os.path.basename(p)
    # 章号简写：001.md → 本卷正文
    m = re.match(r'^(\d{3})\.md$', base)
    mv = re.search(r'V(\d{2})-(\d{3})', os.path.basename(mapping))
    if m and mv and m.group(1) == mv.group(2):
        vol = int(mv.group(1))
        cand = f"{WRITE}/manuscript/volume-0{vol}/{base}" if vol <= 6 else f"{WRITE}/work/m09/volume-07/{base}"
        if os.path.isfile(cand): return cand
    hits = [h for h in glob.glob(FACT + "/**/" + base, recursive=True) + glob.glob(WRITE + "/**/" + base, recursive=True)
            if "私人资料" not in h and "lover-best" not in h]
    return hits[0] if len(hits) == 1 else None

def segs(q):
    parts = re.split(r'[…\.]{1,6}', q)
    return [norm(x) for x in parts if len(norm(x)) >= 4]

def main(files):
    tot = bad = missfile = 0
    for f in files:
        text = open(f, encoding='utf-8').read()
        lines = text.split('\n')
        for i, line in enumerate(lines, 1):
            for m in CITE.finditer(line):
                tot += 1
                path = m.group(1)
                fp = resolve(path, f)
                if not fp:
                    missfile += 1
                    continue
                body = norm(open(fp, encoding='utf-8').read())
                after = line[m.end():m.end() + 260]
                for q in QUOTE.findall(after):
                    ss = segs(q)
                    if not ss: continue
                    if any(s not in body for s in ss):
                        bad += 1
                        short = next(s for s in ss if s not in body)
                        print(f"[引文不在文件] {os.path.basename(f)}:{i}")
                        print(f"    引用 {path}:{m.group(2)}")
                        print(f"    原句 「{q}」")
                        print(f"    缺   「{short[:40]}」")
    print(f"\n共检引用 {tot}；无法定位文件 {missfile}；引文未命中 {bad}")

if __name__ == '__main__':
    fs = sys.argv[1:] or sorted(glob.glob('editorial/full-corpus-readiness/bidirectional-mapping/volume-*/*.md'))
    main(fs)
