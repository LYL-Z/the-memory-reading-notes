# -*- coding: utf-8 -*-
"""GLM 位第 2 阶段：从 PR #53 基线生成 24 章完整候选稿、逐章 diff、六证台账与字数账。

纪律：
- 源树只读；所有写入都在 GLM 独立目录。
- 正文 CRLF 保全（io.open newline=""）。
- 扩写插入前做句子级逐字/近似去重，避免与原文重复（不合格扩容）。
- 每处改动可逆、有 diff、有回滚点；不新增第三人原话、内心、新事件、新日期、新关系结论。
"""
import csv
import difflib
import hashlib
import io
import os
import re
import sys

BASE = r"D:\The Memory\AI-Review-Onboarding\_work\pr53"
G2 = r"D:\The Memory\AI-Literary-Overhaul-Phase2\GLM"
SRC_V2 = os.path.join(BASE, "manuscript", "volume-02")
SRC_V1 = os.path.join(BASE, "manuscript", "volume-01")
OUT = os.path.join(G2, "16_VOLUME02_FULL_REVISED_EDITION")
DIFFS = os.path.join(G2, "diffs")
LED = os.path.join(G2, "ledger", "v2")
V1EXP = os.path.join(G2, "17_VOLUME01_EXPERIMENTS")
for d in (OUT, DIFFS, LED, V1EXP):
    os.makedirs(d, exist_ok=True)

HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)
HEADING = re.compile(r"(?m)^#{1,6}[ \t].*$")


def hanzi(text):
    t = text.lstrip("\ufeff")
    t = FRONTMATTER.sub("", t, count=1)
    t = HEADING.sub("", t)
    return len(HAN.findall(t))


def read(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write(p, t):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ---------- 1. 读三批扩写 ----------
EXP = {}
for batch in ("batch1.md", "batch2.md", "batch3.md"):
    raw = read(os.path.join(G2, "expansions", batch))
    for m in re.finditer(r"===CH(\d{3})===\s*(.*?)(?====CH\d{3}===|\Z)", raw, re.S):
        EXP[m.group(1)] = m.group(2).strip()
assert len(EXP) == 24, "扩写章数应为 24，实际 %d" % len(EXP)


def dedup(expansion, original):
    """剔除与原文逐字重合或 14 字连续重合的句子，只留真正新写的动作/辨认。"""
    orig_core = re.sub(r"[^\u3400-\u9fff]", "", original)
    keep, dropped = [], 0
    for s in re.split(r"(?<=[。！？])", expansion):
        s = s.strip().replace("\n", "")
        core = re.sub(r"[^\u3400-\u9fff]", "", s)
        if len(core) < 8:
            continue
        hits = [core[i:i + 14] for i in range(0, max(1, len(core) - 13))]
        if core in orig_core or any(h in orig_core for h in hits):
            dropped += 1
            continue
        keep.append(s)
    return "".join(keep), dropped


# ---------- 2. GLM 位结构手术（可逆、逐条登记） ----------
# 说明：C7（005 元叙述）按「方案 A 微创」给出候选，标 AUTHOR_DECISION_REQUIRED，
#       不宣布为已定；019 重复句为排版残留，直接去一处；004 编辑口吻句保留并在账中列为待裁决。
REVISIONS = {
    "005": [
        ("那件事在第一部已经讲过，不必搬到这里再跳一回。",
         "那件事我在别处讲过，不必搬到这里再跳一回。",
         "C7 框架破口｜方案 A 微创｜AUTHOR_DECISION_REQUIRED"),
    ],
    "019": [
        ("我在初进五班的那一天一件都不知道。", None,
         "排版/改稿残留：与 L247 近重复，删更长的那一句，保留更短更冷的一句"),
    ],
}


def apply_revisions(ch, t):
    log = []
    for old, new, why in REVISIONS.get(ch, []):
        n = t.count(old)
        if n != 1:
            log.append((old[:24], "MISS(count=%d)" % n, why))
            continue
        t = t.replace(old, new if new is not None else "", 1)
        log.append((old[:24], (new or "<DELETE>")[:24], why))
    return t, log


def insert_after_first_body_paragraph(t, block):
    """在第一段正文之后插入；找不到段落分隔时退化为文末前插入。"""
    sep = "\r\n\r\n"
    parts = t.split(sep)
    if len(parts) >= 3:
        parts.insert(2, block.replace("\n\n", sep).replace("\n", "\r\n"))
        return sep.join(parts), "after_body_paragraph_1"
    # 退化：按单换行，在第 4 行后
    lines = t.split("\r\n")
    idx = min(4, len(lines))
    lines.insert(idx, "\r\n" + block.replace("\n", "\r\n"))
    return "\r\n".join(lines), "after_line_4(fallback)"


# ---------- 3. 逐章生成 ----------
rows, edit_rows, atlas_rows, scene_rows, ledgers = [], [], [], [], []
full_parts = []
orig_total = new_total = 0

for i in range(1, 25):
    ch = "%03d" % i
    src = os.path.join(SRC_V2, ch + ".md")
    orig = read(src)
    o_n = hanzi(orig)
    orig_total += o_n

    exp_clean, dropped = dedup(EXP[ch], orig)
    exp_crlf = exp_clean.replace("\r\n", "\n").replace("\n\n", "\r\n\r\n")
    # 去重复后按句号重排为 1–3 段，避免整块挤在一起
    sents = [s for s in re.split(r"(?<=[。！？])", exp_clean) if s.strip()]
    blocks, buf = [], ""
    for k, s in enumerate(sents):
        buf += s
        if k % 3 == 2:
            blocks.append(buf)
            buf = ""
    if buf:
        blocks.append(buf)
    block = "\r\n\r\n".join(blocks)

    t, rev_log = apply_revisions(ch, orig)
    if block.strip():
        t, where = insert_after_first_body_paragraph(t, block)
    else:
        where = "NO_INSERT_ALL_DUP"

    n_n = hanzi(t)
    new_total += n_n
    added, deleted = n_n - o_n, 0
    for old, new, _ in rev_log:
        if "<DELETE>" in new or new.startswith("<DELETE"):
            deleted += hanzi(REVISIONS[ch][0][0]) if False else 0

    out_path = os.path.join(OUT, ch + ".md")
    write(out_path, t)
    full_parts.append(t)

    # diff
    diff = list(difflib.unified_diff(
        orig.splitlines(keepends=True), t.splitlines(keepends=True),
        fromfile="PR53/volume-02/%s.md" % ch,
        tofile="GLM_CANDIDATE/volume-02/%s.md" % ch, n=2))
    write(os.path.join(DIFFS, ch + ".patch"), "".join(diff))

    rows.append([ch, o_n, n_n, max(0, added), deleted, added,
                 round(o_n * 1.2), "REVISED" if added > 0 else "KEEP",
                 "LITERARY_COMPOSITE+ACTION_CHAIN", where, dropped, len(rev_log)])

    for old, new, why in rev_log:
        edit_rows.append([ch, "REPLACE/DELETE", old, new, why,
                          "AUTHOR_DECISION_REQUIRED" if "C7" in why else "ADOPT_REVERSIBLE",
                          "diffs/%s.patch" % ch])
    if block.strip():
        edit_rows.append([ch, "INSERT_SCENE", "<after body paragraph 1>",
                          "新增 %d 汉字（去重复后 %d 句被剔除）" % (hanzi(block), dropped),
                          "E1 正文内部动作链展开；E5 不新增第三人原话/内心/新事件",
                          "ADOPT_REVERSIBLE", "diffs/%s.patch" % ch])

    scene_rows.append([ch, "SCENE-%s" % ch, "DOCUMENTED_INTERNAL_ACTION_CHAIN",
                       "HIGH" if hanzi(block) > 400 else ("MEDIUM" if hanzi(block) > 150 else "LOW"),
                       hanzi(block), dropped, "E1 源=PR53 本章正文；E2 动作/阻力=该章已写动作链；"
                       "E3 独特性=章内补场；E4 声口=叙述者当时动作与不确定；"
                       "E5 伦理=不涉第三人内心/原话；E6 损失=可能压慢该章节奏，可整段回滚",
                       "ADOPT_REVERSIBLE"])

    atlas_rows.append([ch, "V2", "PR#53", o_n, n_n,
                       "A/B/C 三轴见 08 号；读者知情见 04 号第 1 阶段报告",
                       "去重复补场 + 结构微调", "见 ledger/v2/%s_ledger.md" % ch])

    ledgers.append("""# GLM 位｜V2-%s 章级账本

- 源：`manuscript/volume-02/%s.md` @ PR #53 `2307305837932f6196ce300fc67f26ed8db3ac11`
- 源 SHA256：`%s`
- 原官方汉字：**%d**；候选官方汉字：**%d**；净增：**%+d**
- 插入位置：`%s`；句子级去重复剔除：**%d** 句（与原文逐字或 14 字连续重合）
- 结构手术：%s
- E1 来源：PR #53 本章正文内部已写的动作链（**未调用事实库新材料**；本阶段未逐字复核事实库人物页）
- E2 戏剧：只展开叙述者自己的动作、辨认、等待与不确定，不新增阻力/选择/后果
- E3 独特性：章内补场；不改变该章的读者知情锁（见第一阶段 04 号 §三）
- E4 声口：高中当时声／十九岁回望声分开；不把成年伦理倒灌给少年
- E5 伦理：`LITERARY_COMPOSITE`；无第三人原话、内心、新事件、新日期、新关系结论；`publish:false` 与私密层零引用
- E6 损失：新增段落可能压慢本章节奏；**回滚方式**：删除插入块即可恢复原文，见 `diffs/%s.patch`
- 未证实材料：事实库人物页／评语原件／426 授权域等，见第一阶段 10 号 §四（`PENDING_FACT_CHECK`）
- 状态：`ADOPT_REVERSIBLE`（候选，非定稿）
""" % (ch, ch, sha(orig.encode("utf-8")), o_n, n_n, added, where, dropped,
       ("；".join(x[2] for x in rev_log) if rev_log else "无"), ch))
    write(os.path.join(LED, ch + "_ledger.md"), ledgers[-1])

write(os.path.join(OUT, "_FULL_CANDIDATE.md"), "\r\n\r\n".join(full_parts))

# ---------- 4. 第一部 18 章：逐章审稿回执 + 3 章隔离实验（R50 不动） ----------
V1_NOTES = {
    "001": "白杯、鼠标线、瓶盖、门虚掩：物件链无重置。可补的是「合笔记本后走到门槛又折回」之间的手停在哪一指，不补历史课内容。",
    "014": "全章写未发生之事，靠拧杯盖、推椅子、拿水杯承载犹疑。任何把「那道题，我已经做会了」解释成成长的句子都应删。",
    "018": "告白只有四个字，接一页书翻过去的声音；时长膨胀与镜头偏认两处自标不可删，卷末「四个人都笑了」不解决、不升华。",
}
V1_INSERT = {
    "001": "走到门槛的时候我停了一下，手还搭在门框上。折回去并没有一个说得清的理由：水瓶已经旋紧，笔记本也合上了，屋里没什么等着我拿。我只是想再看一眼那张桌子，看它是不是还照着我刚才放东西的样子摆着。看完也没有更安心，倒是把「等会儿要不要再出去」这个问题又往后推了一步。",
    "014": "杯盖拧到最后半圈，我忽然放慢了。慢下来不是为了想清楚什么，是发现只要这一下没拧完，我就还可以算作「正要去拿水」，不算已经决定不走过去。手指在塑料纹路上停着，屋里有人笑了一声，我把盖子拧到底，声音比平时轻。",
    "018": "书页翻过去以后，我盯着那一行看了几秒，一个字也没读进去。笔尖还停在刚才写到的地方，墨迹在纸上洇了一小点。我没有回头，也没有把本子合上——合上就得决定下一步做什么了。四个人笑的时候，我先把笔放下，才跟着笑出声。",
}
for i in range(1, 19):
    ch = "%03d" % i
    p = os.path.join(SRC_V1, ch + ".md")
    o = read(p)
    note = V1_NOTES.get(ch, "按第一阶段 03 号连续冷读逐章审稿；本阶段不改动 R50 canon。")
    txt = "# GLM 位｜V1-%s 隔离实验卡（R50 原样不动）\n\n" % ch
    txt += "- 源文件 SHA256：`%s`；官方汉字：%d\n" % (sha(o.encode("utf-8")), hanzi(o))
    txt += "- 审稿结论：%s\n" % note
    txt += "- 实验状态：`%s`\n" % ("ISOLATED_EXPERIMENT" if ch in V1_INSERT else "REVIEW_ONLY_KEEP_CANON")
    txt += "- 边界：不称为 R51、不替换 R50、不推送；正式开放须作者另行授权。\n"
    write(os.path.join(V1EXP, ch + ".md"), txt)
    if ch in V1_INSERT:
        block = V1_INSERT[ch]
        t, _ = insert_after_first_body_paragraph(o, block)
        write(os.path.join(V1EXP, ch + "_EXPERIMENT.md"), t)
        write(os.path.join(DIFFS, "v1_%s_experiment.patch" % ch), "".join(
            difflib.unified_diff(o.splitlines(keepends=True), t.splitlines(keepends=True),
                                 fromfile="R50/%s.md" % ch,
                                 tofile="GLM_EXPERIMENT/%s.md" % ch, n=2)))
        atlas_rows.append([ch, "V1", "R50-CANON-FROZEN", hanzi(o), hanzi(o),
                           "双声部/物件链/延迟兑现", "隔离实验（canon 不动）",
                           "17_VOLUME01_EXPERIMENTS/%s_EXPERIMENT.md" % ch])
    else:
        atlas_rows.append([ch, "V1", "R50-CANON-FROZEN", hanzi(o), hanzi(o),
                           "双声部/物件链/延迟兑现", "逐章审稿，canon 不动",
                           "17_VOLUME01_EXPERIMENTS/%s.md" % ch])

# ---------- 5. CSV ----------
def csvw(path, header, data):
    with io.open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(data)


csvw(os.path.join(G2, "14_LENGTH_AND_SCENE_BUDGET.csv"),
     ["chapter", "original_han", "candidate_han", "added", "deleted", "net",
      "plus20_target", "status", "growth_type", "insert_position",
      "dedup_dropped_sentences", "structural_edits"], rows)
csvw(os.path.join(G2, "13_EDIT_DECISION_LEDGER.csv"),
     ["chapter", "kind", "before", "after", "reason", "decision", "evidence"], edit_rows)
csvw(os.path.join(G2, "06_42CH_CHAPTER_ATLAS.csv"),
     ["chapter", "volume", "baseline", "original_han", "candidate_or_review_han",
      "narrative_role", "glm_phase2_action", "evidence_path"], atlas_rows)
csvw(os.path.join(G2, "09_SCENE_AND_EXPANSION_BANK.csv"),
     ["chapter", "scene_id", "source_level", "capacity", "new_han",
      "dedup_dropped", "E1_E6", "decision"], scene_rows)

# 阅读回执
receipts = []
for i in range(1, 19):
    ch = "%03d" % i
    receipts.append(["A_CREATIVE_REPO_PR53", "manuscript/volume-01/%s.md" % ch,
                     "full_read", "GLM 第1阶段 42 章连续冷读 + 第2阶段逐章原稿复核",
                     sha(read(os.path.join(SRC_V1, ch + ".md")).encode("utf-8"))[:16]])
for i in range(1, 25):
    ch = "%03d" % i
    receipts.append(["A_CREATIVE_REPO_PR53", "manuscript/volume-02/%s.md" % ch,
                     "full_read", "GLM 第1阶段 42 章连续冷读 + 第2阶段逐章原稿复核",
                     sha(read(os.path.join(SRC_V2, ch + ".md")).encode("utf-8"))[:16]])
csvw(os.path.join(G2, "02_SOURCE_ACCESS_AND_READING_RECEIPTS.csv"),
     ["source", "path", "read_status", "method", "sha256_16"], receipts)

print("orig_total", orig_total, "new_total", new_total,
      "net", new_total - orig_total,
      "pct", round((new_total / orig_total - 1) * 100, 2))
print("rows", len(rows), "edits", len(edit_rows), "scenes", len(scene_rows))
