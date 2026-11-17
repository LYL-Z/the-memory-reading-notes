import glob, os, re, collections

ROOT = "D:/The Memory/tmp/reading-notes-review"
fs = []
for v in range(1, 7):
    fs += [(f"V{v}", p) for p in sorted(glob.glob(f"{ROOT}/manuscript/volume-0{v}/*.md"))]
fs += [("V7", p) for p in sorted(glob.glob(f"{ROOT}/work/m09/volume-07/*.md"))]

pats = {
    "但": r"但", "可是": r"可是", "不过": r"不过", "却": r"却", "然而": r"然而",
    "并不是": r"并不是", "并非": r"并非", "不是": r"不是", "并不": r"并不",
    "值得": r"值得", "真正": r"真正", "其实": r"其实", "意义上": r"意义上",
}
agg = collections.defaultdict(collections.Counter)
chars = collections.Counter()
for v, p in fs:
    t = open(p, encoding="utf-8").read()
    chars[v] += len(t)
    for k, pat in pats.items():
        agg[v][k] += len(re.findall(pat, t))
print("vol\tchars\t" + "\t".join(pats))
for v in [f"V{i}" for i in range(1, 8)]:
    n = chars[v]
    row = [f"{agg[v][k]*10000/n:.1f}" for k in pats]
    print(f"{v}\t{n}\t" + "\t".join(row) + "   (每万字)")
