import glob, os, re, statistics, collections, json

ROOT = "D:/The Memory/tmp/reading-notes-review"
vols = []
for v in range(1, 7):
    vols.append((f"V{v}", sorted(glob.glob(f"{ROOT}/manuscript/volume-0{v}/*.md"))))
vols.append(("V7", sorted(glob.glob(f"{ROOT}/work/m09/volume-07/*.md"))))

res = {}
for name, files in vols:
    paras, sents, chaps = [], [], []
    for p in files:
        L = [x.strip() for x in open(p, encoding="utf-8") if x.strip() and not x.startswith("#")]
        chaps.append(L)
        paras += L
        for t in L:
            sents += [s for s in re.split(r"[。！？…]+", t) if s.strip()]
    plen = [len(x) for x in paras]
    slen = [len(x) for x in sents]
    ends = [len(c[-1]) for c in chaps]
    res[name] = dict(
        chapters=len(files), paras=len(paras), chars=sum(plen),
        para_mean=round(statistics.mean(plen), 1), para_median=statistics.median(plen),
        short_ratio=round(sum(1 for x in plen if x <= 15) / len(plen), 3),
        sent_mean=round(statistics.mean(slen), 1), sent_median=statistics.median(slen),
        end_mean=round(statistics.mean(ends), 1), end_short=sum(1 for e in ends if e <= 30),
        chap_mean=round(sum(plen) / len(files)),
    )
print(json.dumps(res, ensure_ascii=False, indent=1))
