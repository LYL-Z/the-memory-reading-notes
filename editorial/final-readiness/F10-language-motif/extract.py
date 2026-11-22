import glob, os, re

ROOT = "D:/The Memory/tmp/reading-notes-review"
fs = []
for v in range(1, 7):
    fs += [(f"V{v}-{os.path.basename(p)[:3]}", p) for p in sorted(glob.glob(f"{ROOT}/manuscript/volume-0{v}/*.md"))]
fs += [(f"V7-{os.path.basename(p)[:3]}", p) for p in sorted(glob.glob(f"{ROOT}/work/m09/volume-07/*.md"))]

out = []
for cid, p in fs:
    L = [x.rstrip("\n") for x in open(p, encoding="utf-8")]
    title = L[0].strip("# ").strip() if L else ""
    paras = [x.strip() for x in L if x.strip() and not x.startswith("#")]
    out.append(f"\n### {cid} 《{title}》 段数{len(paras)}")
    for t in paras[:2]:
        out.append(f"  首: {t}")
    for t in paras[-3:]:
        out.append(f"  末: {t}")
    if paras:
        last = paras[-1]
        out.append(f"  末段长度: {len(last)}")
open(f"{ROOT}/editorial/final-readiness/F10-language-motif/chap-edges.txt", "w", encoding="utf-8").write("\n".join(out))
print(len(fs), "chapters;", len("\n".join(out)), "chars")
