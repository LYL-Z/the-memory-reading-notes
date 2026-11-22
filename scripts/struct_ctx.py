import sys, re
ROOT = "D:/The Memory/tmp/reading-notes-review"

def path(cid):
    v, c = cid.split("-")
    if v == "V7":
        return f"{ROOT}/work/m09/volume-07/{c}.md"
    return f"{ROOT}/manuscript/volume-0{v[1]}/{c}.md"

def show(cid, ln, before=2, after=3):
    p = path(cid)
    L = open(p, encoding="utf-8").read().split("\n")
    a = max(1, ln - before); b = min(len(L), ln + after)
    print(f"--- {cid}:{ln} ---")
    for i in range(a, b + 1):
        mark = ">>" if i == ln else "  "
        print(f"{mark}{i}: {L[i-1]}")

for arg in sys.argv[1:]:
    cid, ln = arg.split(":")
    show(cid, int(ln))
