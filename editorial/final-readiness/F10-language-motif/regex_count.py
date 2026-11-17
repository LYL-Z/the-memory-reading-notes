import glob, os, re, collections, sys

ROOT = "D:/The Memory/tmp/reading-notes-review"
fs = []
for v in range(1, 7):
    fs += [(f"V{v}-{os.path.basename(p)[:3]}", p) for p in sorted(glob.glob(f"{ROOT}/manuscript/volume-0{v}/*.md"))]
fs += [(f"V7-{os.path.basename(p)[:3]}", p) for p in sorted(glob.glob(f"{ROOT}/work/m09/volume-07/*.md"))]

pats = {
    "不是A而是B": r"不是[^。！？]{1,24}[，,]?\s*而是",
    "不是A。是B": r"不是[^。！？]{1,20}。\s*是",
    "没有A也没有B": r"没有[^。！？]{1,20}[，,]\s*也没有",
    "既A也B": r"既[^。！？]{1,16}[，,]?\s*也",
    "并不是": r"并不是",
    "并没有": r"并没有",
    "只是": r"只是",
    "不过": r"不过",
    "倒也": r"倒也",
    "仍旧": r"仍旧",
    "仍然": r"仍然",
    "还是": r"还是",
    "忽然": r"忽然",
    "突然": r"突然",
    "我以为": r"我以为",
    "我知道": r"我知道",
    "我想": r"我想",
    "我记得": r"我记得",
    "我记住了": r"我记住了",
    "我没有问": r"我没有问",
    "我没有说话": r"我没有说话",
    "我没有回头": r"我没有回头",
    "我没有再": r"我没有再",
    "我不知道": r"我不知道",
    "那时候": r"那时候|那时，",
    "如今": r"如今",
    "现在": r"现在",
    "当时": r"当时",
    "后来": r"后来",
    "原来": r"原来",
    "其实": r"其实",
    "大概": r"大概",
    "也许": r"也许",
    "至少": r"至少",
    "值得": r"值得",
}
tot = collections.Counter()
per = {k: collections.Counter() for k in pats}
vols = {k: collections.Counter() for k in pats}
for cid, p in fs:
    txt = open(p, encoding="utf-8").read()
    v = cid.split("-")[0]
    for k, pat in pats.items():
        n = len(re.findall(pat, txt))
        if n:
            tot[k] += n
            per[k][cid] = n
            vols[k][v] += n
print("pattern\ttotal\tchapters\t" + "\t".join(f"V{i}" for i in range(1, 8)))
for k in pats:
    print(f"{k}\t{tot[k]}\t{len(per[k])}\t" + "\t".join(str(vols[k][f"V{i}"]) for i in range(1, 8)))
