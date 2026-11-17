import os, re, glob, collections

ROOT = "D:/The Memory/tmp/reading-notes-review"
files = []
for v in range(1, 7):
    for p in sorted(glob.glob(f"{ROOT}/manuscript/volume-0{v}/*.md")):
        files.append((f"V{v}-{os.path.basename(p)[:3]}", p))
for p in sorted(glob.glob(f"{ROOT}/work/m09/volume-07/*.md")):
    files.append((f"V7-{os.path.basename(p)[:3]}", p))

lines = []
for cid, p in files:
    with open(p, encoding="utf-8") as f:
        for i, ln in enumerate(f, 1):
            t = ln.strip()
            if not t or t.startswith("#"):
                continue
            lines.append([cid, i, t, re.sub(r"[^\u4e00-\u9fff]", "", t)])

N = 14
idx = collections.defaultdict(list)
for k, rec in enumerate(lines):
    s = rec[3]
    for j in range(0, len(s) - N + 1):
        idx[s[j:j+N]].append(k)

def lcp(a, i, b, j, cap=200):
    n = 0
    while i + n < len(a) and j + n < len(b) and a[i+n] == b[j+n] and n < cap:
        n += 1
    return n

pairs = set()
for k, rec in enumerate(lines):
    s = rec[3]
    if len(s) < N:
        continue
    best = {}
    for j in range(0, len(s) - N + 1):
        for k2 in idx[s[j:j+N]]:
            if k2 == k:
                continue
            a, b = k, k2
            s2 = lines[k2][3]
            # 向左
            x, y = j, lines[k2][3].find(s[j:j+N])
            if y < 0:
                continue
            while x > 0 and y > 0 and s[x-1] == s2[y-1]:
                x -= 1; y -= 1
            L = lcp(s, x, s2, y)
            if L >= 14:
                key = (k, k2)
                if key not in best or L > best[key][1]:
                    best[key] = (x, L, y)
    for (a, b), (x, L, y) in best.items():
        sub = lines[a][3][x:x+L]
        pairs.add((L, a, b, x, y, sub))

res = sorted(pairs, key=lambda r: (-r[0], r[1]))
print(f"# 重复段 {len(res)} 条 (N={N}, 双向)")
for L, a, b, x, y, sub in res:
    print(f"{L}\t{lines[a][0]}:{lines[a][1]}\t{lines[b][0]}:{lines[b][1]}\t{sub}")
