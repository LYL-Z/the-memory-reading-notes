import os, re, glob, sys, collections

ROOT = "D:/The Memory/tmp/reading-notes-review"
files = []
for v in range(1, 7):
    for p in sorted(glob.glob(f"{ROOT}/manuscript/volume-0{v}/*.md")):
        files.append((f"V{v}-{os.path.basename(p)[:3]}", p))
for p in sorted(glob.glob(f"{ROOT}/work/m09/volume-07/*.md")):
    files.append((f"V7-{os.path.basename(p)[:3]}", p))

# 逐行读，记录 (章, 行号, 文本)
lines = []
for cid, p in files:
    with open(p, encoding="utf-8") as f:
        for i, ln in enumerate(f, 1):
            t = ln.strip()
            if not t or t.startswith("#"):
                continue
            lines.append((cid, i, t))

def norm(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s)

# 用 N=14 的汉字 n-gram 建索引，找跨行重复
N = int(sys.argv[1]) if len(sys.argv) > 1 else 14
idx = collections.defaultdict(list)
for k, (cid, i, t) in enumerate(lines):
    s = norm(t)
    for j in range(0, len(s) - N + 1):
        idx[s[j:j+N]].append((k, cid, i, j))

# 合并成重复区间：对每行，找出与另一行相同的最长公共子串（长度>=N）
seen = set()
results = []
for k, (cid, i, t) in enumerate(lines):
    s = norm(t)
    if len(s) < N:
        continue
    best = {}
    for j in range(0, len(s) - N + 1):
        for (k2, cid2, i2, j2) in idx[s[j:j+N]]:
            if k2 <= k:
                continue
            key = (k2,)
            # 扩展
            a, b = j, j2
            while a > 0 and b > 0 and s[a-1] == norm(lines[k2][2])[b-1]:
                a -= 1; b -= 1
            e1, e2 = j + N, j2 + N
            s2 = norm(lines[k2][2])
            while e1 < len(s) and e2 < len(s2) and s[e1] == s2[e2]:
                e1 += 1; e2 += 1
            if e1 - a >= N:
                prev = best.get(k2)
                if prev is None or (e1 - a) > (prev[1] - prev[0]):
                    best[k2] = (a, e1, s[a:e1])
    for k2, (a, e1, sub) in best.items():
        if len(sub) >= N:
            results.append((len(sub), cid, i, cid2, lines[k2][1], sub))

results.sort(reverse=True)
print(f"# N={N}, 重复段 {len(results)} 条")
for r in results:
    print(f"{r[0]}\t{r[1]}:{r[2]}\t{r[3]}:{r[4]}\t{r[5]}")
