# -*- coding: utf-8 -*-
"""HY4 修订补丁 3：整体复读后修复接缝、重复句与残留地点误置。"""
import io
import os
import sys

BASE = r"D:\The Memory\tmp\hy4-independent-review\manuscript\volume-02"

PATCH = {
    "002": [
        ("又想把缺的那部分靠再看一遍补上。还有些念头",
         "又想把缺的那部分靠再看一遍补上。\r\n\r\n还有些念头"),
    ],
    "005": [
        ("我如今说不准自己选了上铺还是下铺，靠门还是靠窗。也许当时根本没费心记住，因为心里清楚这只是暂住。心里清楚这只是暂住，也就没费心去记。",
         "我如今说不准自己选了上铺还是下铺，靠门还是靠窗。心里清楚这只是暂住，也就没费心去记。"),
        ("我们没有为了525的结束专门聚到一处，也没有谁轮流说一句以后要好好地过。至少我没有记下这种场面。学年结束本来就会换班",
         "我们没有为了525的结束专门聚到一处。学年结束本来就会换班"),
    ],
    "006": [
        ("那次说过什么誓词，谁先伸手，我也讲不准。大哥、二弟、三妹倒留下来了。那几个称呼我们很愿意用",
         "那次说过什么誓词，谁先伸手，我也讲不准。那几个称呼我们很愿意用"),
    ],
    "010": [
        ("这种时候更怕旁边坐着熟人。", "更怕的是旁边坐着熟人。"),
    ],
    "011": [
        ("夏恺宪的妈妈当年提议结拜，后来又送我生日礼物，这两件事隔着好些年。小时候聚会有她替我们张罗，长大以后她还记得我。这两件事隔着好些年，中间的生活我并不知道。",
         "夏恺宪的妈妈当年提议结拜，后来又送我生日礼物，中间隔着好些年。小时候聚会有她替我们张罗，长大以后她还记得我；这些年她怎么过的，我并不知道。"),
        ("记得在她家看的鬼片", "记得一起看过的那部鬼片"),
        ("回来大家又一起做饭。这些都不是我安排的。", "回来大家又一起做饭。"),
    ],
}


def main():
    total, miss = 0, []
    for ch, reps in PATCH.items():
        path = os.path.join(BASE, ch + ".md")
        with io.open(path, "r", encoding="utf-8", newline="") as f:
            text = f.read()
        for i, (old, new) in enumerate(reps, 1):
            n = text.count(old)
            if n != 1:
                miss.append((ch, i, n, old[:36]))
                continue
            text = text.replace(old, new, 1)
            total += 1
        with io.open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    print("APPLIED =", total)
    if miss:
        print("MISSED:")
        for m in miss:
            print("  ", m)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
