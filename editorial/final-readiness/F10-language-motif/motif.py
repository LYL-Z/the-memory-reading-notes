import glob, os, re, collections

ROOT = "D:/The Memory/tmp/reading-notes-review"
fs = []
for v in range(1, 7):
    fs += [(f"V{v}", f"{os.path.basename(p)[:3]}", p) for p in sorted(glob.glob(f"{ROOT}/manuscript/volume-0{v}/*.md"))]
fs += [("V7", f"{os.path.basename(p)[:3]}", p) for p in sorted(glob.glob(f"{ROOT}/work/m09/volume-07/*.md"))]

groups = {
 "茶": ["茶桌","茶几","茶杯","泡茶","喝茶","茶水","茶缸","茶叶","斟"],
 "门": ["门口","门牌","后门","前门","校门","家门","敲门","门缝","铁门","推门","关门","开门"],
 "钥匙": ["钥匙"],
 "灯": ["台灯","路灯","声控","留灯","关灯","开灯","灯管","灯光","灯泡"],
 "桌": ["课桌","饭桌","茶桌","书桌","讲台","桌角","桌面","桌子"],
 "床": ["上下铺","上铺","下铺","床板","床沿","床单","床"],
 "名次": ["名次","排名","分数","总分","一本线","位次","第几名"],
 "名字": ["名字","取名","称呼","叫法","外号","昵称"],
 "楼梯": ["楼梯","楼道","六楼","台阶"],
 "河": ["资江","洢水","河边","江边","河水"],
}
tot = collections.Counter()
per = {k: collections.Counter() for k in groups}
for v, ch, p in fs:
    t = open(p, encoding="utf-8").read()
    for k, ws in groups.items():
        for w in ws:
            n = t.count(w)
            if n:
                tot[(k,w)] += n
                per[k][v] += n
for k, ws in groups.items():
    print(f"\n== {k} 总 {sum(tot[(k,w)] for w in ws)}")
    print("   " + "  ".join(f"{w}:{tot[(k,w)]}" for w in ws if tot[(k,w)]))
    print("   卷分布 " + " ".join(f"{v}:{per[k][v]}" for v in [f'V{i}' for i in range(1,8)]))
