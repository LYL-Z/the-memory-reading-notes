import glob, os, re, sys

ROOT = "D:/The Memory/tmp/reading-notes-review"
fs = []
for v in range(1, 7):
    fs += [(f"V{v}-{os.path.basename(p)[:3]}", p) for p in sorted(glob.glob(f"{ROOT}/manuscript/volume-0{v}/*.md"))]
fs += [(f"V7-{os.path.basename(p)[:3]}", p) for p in sorted(glob.glob(f"{ROOT}/work/m09/volume-07/*.md"))]

lo, hi = int(sys.argv[1]), int(sys.argv[2])
MARK = re.compile(r"如今|现在|多年后|后来|那年|当时|那年月|大一|大二|今年|去年|二〇二|20\d\d")
for cid, p in fs[lo:hi]:
    L = [x.rstrip("\n") for x in open(p, encoding="utf-8")]
    body = [(i, x.strip()) for i, x in enumerate(L, 1) if x.strip() and not x.startswith("#")]
    print(f"\n##### {cid} {L[0].strip()}  ({len(L)} 行)")
    for i, t in body[:2]:
        print(f"  首{i}: {t[:120]}")
    hits = [(i, t) for i, t in body if MARK.search(t)]
    print(f"  标记 {len(hits)} 段")
    for i, t in hits[:6]:
        print(f"   ~{i}: {t[:100]}")
    if body:
        print(f"  末{body[-1][0]}: {body[-1][1][:100]}")
