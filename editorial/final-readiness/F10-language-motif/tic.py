import glob, os, re, collections

ROOT = "D:/The Memory/tmp/reading-notes-review"
fs = []
for v in range(1, 7):
    fs += [(f"V{v}", f"{os.path.basename(p)[:3]}", p) for p in sorted(glob.glob(f"{ROOT}/manuscript/volume-0{v}/*.md"))]
fs += [("V7", f"{os.path.basename(p)[:3]}", p) for p in sorted(glob.glob(f"{ROOT}/work/m09/volume-07/*.md"))]

pats = {
    "我立刻": r"我(立刻|立即|马上)",
    "忽然高兴/兴奋": r"我(忽然|突然|一下子|一下)(很高兴|兴奋|来了精神|高兴起来|坐直)",
    "设问为什么": r"为什么[^。！？]{0,20}[？?]",
    "因为自答": r"因为[^。！？]{4,40}。",
    "讲成/写成/写进": r"(讲成|写成|写进|不肯写|没有写|不写|补成|补出|补写)",
    "这一段/这一章/这一节": r"(这一段|这一章|这一节|这本书|这篇|这个句子|这一句)",
    "不值得": r"不值得",
    "只是": r"只是",
    "并没有": r"并没有",
    "他没有说话/我也没有": r"(他|她|我)(没有说话|没有回答|没有问|没有回头|没有接)",
    "两个短句并置": r"[^。！？]{4,12}。[^。！？]{4,12}。",
}
for k, pat in pats.items():
    per = collections.Counter()
    for v, ch, p in fs:
        t = open(p, encoding="utf-8").read()
        n = len(re.findall(pat, t))
        if n:
            per[v] += n
    print(f"{k}\t{sum(per.values())}\t" + "\t".join(f"{v}:{per[v]}" for v in [f'V{i}' for i in range(1,8)]))
