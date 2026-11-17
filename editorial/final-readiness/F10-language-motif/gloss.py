import glob, os, re, collections

ROOT = "D:/The Memory/tmp/reading-notes-review"
fs = []
for v in range(1, 7):
    fs += [(f"V{v}", f"{os.path.basename(p)[:3]}", p) for p in sorted(glob.glob(f"{ROOT}/manuscript/volume-0{v}/*.md"))]
fs += [("V7", f"{os.path.basename(p)[:3]}", p) for p in sorted(glob.glob(f"{ROOT}/work/m09/volume-07/*.md"))]

# chapter endings
print("== 章末结构 ==")
short_multi = []
for v, ch, p in fs:
    L = [x.strip() for x in open(p, encoding="utf-8") if x.strip() and not x.startswith("#")]
    tail = L[-6:]
    short = [t for t in tail if len(t) <= 30]
    last = L[-1]
    if len(short) >= 3:
        short_multi.append((v, ch, len(short), last[:40]))
print("末6段中>=3段<=30字的章:", len(short_multi))
for x in short_multi:
    print("  ", x)

# abstract gloss sentences
GLOSS = re.compile(r"(这件事|这一次|那一次|有时候|有些时候|多年|后来|其实|也许|大概|至少|生活|日子|时间|记忆|关系|选择|答案|事情|道理|意义|值得|真正)")
print("\n== 每卷『我+抽象判断』句 ==")
cnt = collections.Counter()
tot = collections.Counter()
for v, ch, p in fs:
    t = open(p, encoding="utf-8").read()
    sents = [s for s in re.split(r"[。！？\n]", t) if s.strip()]
    for s in sents:
        if s.startswith(("我", "这", "那", "他", "她")) and GLOSS.search(s) and 12 <= len(s) <= 60:
            cnt[v] += 1
            tot[v] += len(s)
for v in [f"V{i}" for i in range(1, 8)]:
    print(v, cnt[v])

print("\n== 内心直述他人 ==")
for pat in ["她知道", "他知道", "她不想", "他不想", "她需要", "他需要", "她没有力气", "他并不", "她并不"]:
    n = sum(open(p, encoding="utf-8").read().count(pat) for _, _, p in fs)
    print(pat, n)
