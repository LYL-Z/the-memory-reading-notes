import os, re, glob, collections, sys

ROOT = "D:/The Memory/tmp/reading-notes-review"
files = []
for v in range(1, 7):
    for p in sorted(glob.glob(f"{ROOT}/manuscript/volume-0{v}/*.md")):
        files.append((f"V{v}-{os.path.basename(p)[:3]}", p))
for p in sorted(glob.glob(f"{ROOT}/work/m09/volume-07/*.md")):
    files.append((f"V7-{os.path.basename(p)[:3]}", p))

words = sys.argv[1:]
tot = collections.Counter()
per = {w: collections.Counter() for w in words}
for cid, p in files:
    txt = open(p, encoding="utf-8").read()
    for w in words:
        n = txt.count(w)
        if n:
            tot[w] += n
            per[w][cid] = n
for w in words:
    print(f"== {w}: 共 {tot[w]} 次, {len(per[w])} 章")
    print("  " + " ".join(f"{c}:{n}" for c, n in sorted(per[w].items(), key=lambda x: -x[1])))
