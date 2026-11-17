import glob, re, os
ROOT = "D:/The Memory/tmp/reading-notes-review/work/m09/volume-07"
for p in sorted(glob.glob(ROOT + "/*.md")):
    t = open(p, encoding="utf-8").read()
    title = t.split("\n")[0].lstrip("# ")
    dates = re.findall(r"20\d\d年\d{1,2}月(?:\d{1,2}日)?|二〇二[四五]年[一二三四五六七八九十]{1,2}月|大一下|大二上|大一上|大二下|寒假|暑假|国庆|五一", t)
    print(f"{os.path.basename(p)[:3]} {title}")
    print("   ", " | ".join(dict.fromkeys(dates))[:300])
