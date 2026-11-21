#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""七部一百三十五章正典验证器（现行文学终修V1.2基线）。

与 verify_six_volume_integrated.py 的关系：后者是六部 115 章的历史验收证据，
按当时基线冻结，不再修改，也不用于当前正典。本脚本是当前正典的唯一验证入口。

基线来自 editorial/literary-finalization/2026-11-21-v1.2-chapter-canon.tsv（保留2026-11-21七卷融合快照不改写），
该表由实际正文生成：每章 git blob SHA1、SHA256、官方汉字数（scripts/hanzi_count.py，
排除标题/frontmatter/代码围栏/HTML 注释）。

用法：
    python scripts/verify_seven_volume_integrated.py            # 全量验证
    python scripts/verify_seven_volume_integrated.py --json     # 机器可读

退出码：0 = PASS，1 = FAIL。任何未执行的检查不会被记为 PASS。
"""
import io
import os
import sys
import json
import hashlib
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import hanzi_count as H  # noqa: E402

CANON = os.path.join(ROOT, "editorial", "literary-finalization",
                     "2026-11-21-v1.2-chapter-canon.tsv")
EXPECTED = {1: 18, 2: 24, 3: 16, 4: 18, 5: 19, 6: 20, 7: 20}
TOTAL_CHAPTERS = 135
TOTAL_HANZI = 853423

# 作者裁定与档案硬事实的定点断言
FUXIONGHUI_BAD = [
    ("manuscript/volume-02/018.md", "他上课的第一句话"),
    ("manuscript/volume-04/003.md", "他说，一个人不懂得问"),
    ("manuscript/volume-04/003.md", "他教政治，却讲起做题"),
    ("manuscript/volume-04/003.md", "他站在讲台上问"),
    ("manuscript/volume-04/004.md", "他说完，教室没有马上安静"),
    ("manuscript/volume-04/017.md", "不等于他当年没有教过"),
]
PROTECTED = [
    ("manuscript/volume-01/018.md", "我喜欢你。"),
    ("manuscript/volume-02/019.md", "这种不高兴归我自己，不能倒算成她早该知道什么。"),
    ("manuscript/volume-06/013.md",
     "还在的门框旁边，我站过，她站过，刘逸凡走掉过。"),
    ("manuscript/volume-07/014.md", "我不知道她怎么想我。这件事从头到尾没有变过。"),
    ("manuscript/volume-07/015.md", "她不必跟我一样记得这趟旅行。"),
]


def blob_sha1(raw):
    # 仓库内 blob 按 LF 规范化；Windows 检出可能带 CRLF，先归一再哈希，
    # 使断言在 Linux CI 与 Windows 工作树上一致。
    raw = raw.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()


def load_canon():
    rows = []
    with io.open(CANON, encoding="utf-8") as fh:
        head = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            if not line.strip():
                continue
            vals = line.rstrip("\n").split("\t")
            rows.append(dict(zip(head, vals)))
    return rows


def read(rel):
    p = os.path.join(ROOT, rel.replace("/", os.sep))
    raw = io.open(p, "rb").read()
    return raw, raw.decode("utf-8").replace("\r\n", "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    checks = []
    fails = []

    def chk(name, ok, detail=""):
        checks.append({"check": name, "result": "PASS" if ok else "FAIL",
                       "detail": detail})
        if not ok:
            fails.append(name + (" :: " + detail if detail else ""))

    if not os.path.isfile(CANON):
        print("FAIL: canon table missing: " + CANON)
        return 1
    rows = load_canon()
    chk("canon_rows_135", len(rows) == TOTAL_CHAPTERS, "rows=%d" % len(rows))

    # 1 目录与章数
    for v, n in EXPECTED.items():
        d = os.path.join(ROOT, "manuscript", "volume-0%d" % v)
        got = sorted(x for x in os.listdir(d) if x.endswith(".md")) if os.path.isdir(d) else []
        want = ["%03d.md" % i for i in range(1, n + 1)]
        chk("volume_%02d_chapter_set" % v, got == want,
            "got=%d want=%d" % (len(got), n))

    # 2 逐章哈希、字数、格式
    total = 0
    seen = set()
    for r in rows:
        rel = r["path"]
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        if rel in seen:
            chk("unique_path_" + rel, False, "duplicate entry")
            continue
        seen.add(rel)
        if not os.path.isfile(p):
            chk("exists_" + rel, False)
            continue
        raw, txt = read(rel)
        tag = r["volume"] + "-" + r["chapter"]
        chk("blob_" + tag, blob_sha1(raw) == r["git_blob_sha1"], "git blob sha1")
        chk("sha256_" + tag,
            hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest() == r["sha256"],
            "sha256")
        c = H.hanzi_count(txt)
        total += c
        chk("hanzi_" + tag, c == int(r["hanzi"]), "got=%d want=%s" % (c, r["hanzi"]))
        lines = txt.split("\n")
        chk("title_" + tag, lines[0].startswith("# ") and len(lines[0]) > 2,
            lines[0][:40])
        chk("nonempty_" + tag, len(txt.strip()) > 200, "chars=%d" % len(txt.strip()))
        chk("no_conflict_" + tag,
            not any(m in txt for m in ("<<<<<<<", ">>>>>>>", "\n=======\n")))
        chk("no_replacement_char_" + tag, "\ufffd" not in txt)
        chk("no_candidate_meta_" + tag,
            not any(m in txt for m in ("CANDIDATE", "候选稿", "底本：", "模型指令",
                                       "【有界推演", "【文学化重构")))

    chk("total_chapters_135", len(seen) == TOTAL_CHAPTERS, "n=%d" % len(seen))
    chk("total_hanzi_%d" % TOTAL_HANZI, total == TOTAL_HANZI, "got=%d" % total)

    # 3 事实定点：符雄辉为女性，不得残留误用男性代词的旧句
    for rel, bad in FUXIONGHUI_BAD:
        _, txt = read(rel)
        chk("fuxionghui_female_" + rel.split("/")[-1] + "_" + bad[:8],
            bad not in txt, bad)

    # 4 刘逸凡（数学课代表）与刘弈帆（物理课代表）是两个人，不得互相顶替
    _, t12 = read("manuscript/volume-06/012.md")
    _, t13 = read("manuscript/volume-06/013.md")
    chk("liuyifan_not_substituted_012",
        t12.count("刘逸凡") == 15 and t12.count("刘弈帆") == 0,
        "逸凡=%d 弈帆=%d" % (t12.count("刘逸凡"), t12.count("刘弈帆")))
    chk("liuyifan_not_substituted_013",
        t13.count("刘逸凡") == 9 and t13.count("刘弈帆") == 0,
        "逸凡=%d 弈帆=%d" % (t13.count("刘逸凡"), t13.count("刘弈帆")))

    # 5 赵问竹线五处保护句
    for rel, s in PROTECTED:
        _, txt = read(rel)
        chk("protected_" + rel.split("/")[-1], s in txt, s[:24])

    # 6 关键事实点
    _, t407 = read("manuscript/volume-04/007.md")
    chk("v4_007_seven_chars", "你老是说我讨嫌" in t407 and "六个字" not in t407)
    _, t313 = read("manuscript/volume-03/013.md")
    chk("v3_013_no_ghost_dialogue", "算我的" not in t313)
    _, t716 = read("manuscript/volume-07/016.md")
    chk("v7_016_singapore_27", "二十七" in t716)

    # 7 历史候选不得混入正典
    for v, name in ((6, "018A.md"), (7, "001A.md")):
        p = os.path.join(ROOT, "manuscript", "volume-0%d" % v, name)
        chk("historical_candidate_excluded_%d_%s" % (v, name), not os.path.exists(p))

    out = {
        "verifier": "verify_seven_volume_integrated.py",
        "baseline": os.path.basename(CANON),
        "chapters": len(seen),
        "official_hanzi": total,
        "checks_run": len(checks),
        "checks_failed": len(fails),
        "result": "PASS" if not fails else "FAIL",
        "failures": fails,
    }
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        for c in checks:
            if c["result"] == "FAIL":
                print("FAIL %s :: %s" % (c["check"], c["detail"]))
        print("checks_run=%d failed=%d chapters=%d official_hanzi=%d -> %s"
              % (len(checks), len(fails), len(seen), total, out["result"]))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())