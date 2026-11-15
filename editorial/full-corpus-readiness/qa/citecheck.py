# -*- coding: utf-8 -*-
"""QA 引文核验器：从映射档案里抽出 `path:line` 引用，检查文件是否存在、引文是否落在该行附近。
用法: python qa/citecheck.py <映射文件> [...]
"""
import re, os, sys, glob

FACT = r"D:/The Memory/The Memory"
WRITE = r"D:/The Memory/tmp/reading-notes-review"

# 匹配形如  `xxx/yyy.md:12` 或 `xxx.md:12-30` 或 `xxx.md:12,34`
CITE = re.compile(r'`([^`\n]*?\.md):(\d+(?:[-,–]\d+)*)`')

def resolve(p):
    p = p.strip()
    for root in (FACT, WRITE):
        f = os.path.join(root, p)
        if os.path.isfile(f):
            return f, root
    # 容错：只给文件名，全库搜
    base = os.path.basename(p)
    hits = glob.glob(FACT + "/**/" + base, recursive=True) + glob.glob(WRITE + "/**/" + base, recursive=True)
    hits = [h for h in hits if "私人资料" not in h and "lover-best" not in h]
    if len(hits) == 1:
        return hits[0], os.path.dirname(hits[0])
    return None, None

def nums(spec):
    out = []
    for part in re.split(r'[,\s]+', spec):
        if not part: continue
        m = re.match(r'(\d+)[-–](\d+)$', part)
        if m: out.extend(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit(): out.append(int(part))
    return out

def check(mdpath):
    txt = open(mdpath, encoding='utf-8').read()
    lines = txt.split('\n')
    total = missing = out_of_range = 0
    problems = []
    for i, line in enumerate(lines, 1):
        for m in CITE.finditer(line):
            path, spec = m.group(1), m.group(2)
            total += 1
            f, root = resolve(path)
            if not f:
                missing += 1
                problems.append(("FILE", i, path, "文件不存在/不唯一"))
                continue
            body = open(f, encoding='utf-8').read().split('\n')
            ns = nums(spec)
            if ns and max(ns) > len(body):
                out_of_range += 1
                problems.append(("RANGE", i, f"{path}:{spec}", f"行号越界（文件共 {len(body)} 行）"))
    return total, missing, out_of_range, problems

if __name__ == '__main__':
    files = sys.argv[1:] or sorted(glob.glob('editorial/full-corpus-readiness/bidirectional-mapping/volume-*/*.md'))
    grand = [0, 0, 0]
    for f in files:
        t, m, o, probs = check(f)
        grand[0] += t; grand[1] += m; grand[2] += o
        flag = "" if not probs else f"  ← {len(probs)} 处问题"
        print(f"{os.path.basename(f):14s} 引用={t:4d} 文件缺失={m:3d} 行号越界={o:3d}{flag}")
        for kind, ln, p, why in probs[:12]:
            print(f"    [{kind}] 映射第{ln}行 -> {p}  ({why})")
    print(f"\n合计 引用={grand[0]} 文件缺失={grand[1]} 行号越界={grand[2]}")
