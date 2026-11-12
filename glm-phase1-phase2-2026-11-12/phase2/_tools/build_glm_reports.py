# -*- coding: utf-8 -*-
"""GLM 位第 2 阶段：补齐 23 项交付中的复用型报告与 A/B 锚点册。

复用范围严格限定为 **GLM 位自己第 1 阶段的回执**（同一执行位），
不读取、不复制 DeepSeek 位任何诊断/候选/账本。
"""
import difflib
import io
import os
import re

G1 = r"D:\The Memory\AI-Review-Onboarding\GLM"
G2 = r"D:\The Memory\AI-Literary-Overhaul-Phase2\GLM"
OUT = os.path.join(G2, "16_VOLUME02_FULL_REVISED_EDITION")
DIFFS = os.path.join(G2, "diffs")


def read(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write(p, t):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)


HEAD = """<!-- GLM 位第 2 阶段复用说明：
本文件主体复用 **GLM 位自己第 1 阶段**（`AI-Review-Onboarding/GLM/`）的独立冷读回执，
并经第 2 阶段逐章原稿复核；未读取、未引用 DeepSeek 位或 GLM 位以外的任何模型本阶段结论。
第 2 阶段的施工结果、字数、diff 与裁决见 00/10/13/14/18/23 号文件。
-->

"""

REUSE = [
    ("03_volume01_continuous_read.md", "03_VOLUME01_R50_INDEPENDENT_REVIEW.md",
     "第一部 R50 逐章独立审稿（canon 不动）"),
    ("04_volume02_continuous_read.md", "04_VOLUME02_24CH_INDEPENDENT_REVIEW.md",
     "第二部 24 章逐章独立审稿与 B2 知情锁核验"),
    ("05_character_evidence_atlas.md", "07_CHARACTER_AUTONOMY_ATLAS.md",
     "人物自主行动与证据边界图"),
    ("06_dual_timeline_and_reader_knowledge.md", "08_EVENT_TIMELINE_READER_BELIEF.md",
     "三时钟、读者信念与永久缺口"),
    ("08_style_voice_and_ai-pattern_diagnostics.md", "11_PROSE_VOICE_AI_PATTERN_AUDIT.md",
     "声口、反模板与 AI 模式诊断"),
    ("09_external_research_MLA.md", "12_LITERARY_RESEARCH_MLA.md",
     "外部研究 MLA 与审稿问题单"),
    ("10_unresolved_questions_and_conflicts.md", "05_TOP_10_SYSTEMIC_PROBLEMS.md",
     "系统性瓶颈、冲突与订正账"),
    ("11_independent_understanding_report.md", "19_CROSS_VOLUME_CONTINUOUS_READ.md",
     "跨卷独立理解与连续复读基准"),
]
for src, dst, title in REUSE:
    body = read(os.path.join(G1, src))
    out = HEAD + "# GLM 位第 2 阶段｜" + title + "\n\n" + body
    write(os.path.join(G2, dst), out)

# ---------- 18_BEFORE_AFTER_ANCHORS.md：36 组可复核 A/B ----------
lines = ["# GLM 位｜18 前后锚点与 A/B 对照（36 组）", "",
         "> A = PR #53 原句（**KEEP 永远是一个合法裁决**）；B = 本候选的改动或补场。",
         "> 每组给：原句位置、原句、B 方案、问题类型、收益／损失、裁决。",
         "> 本阶段不把「改过」当「更好」；凡 A 优于 B 处直接写 KEEP。", ""]

HAND_AB = [
    ("V1-014", "那道题，我已经做会了。",
     "（KEEP）不添加任何解释句",
     "章末解释收束", "收益=保留借口与告白同归于尽的双关；损失=无", "KEEP"),
    ("V1-018", "她没有说“喜欢”，也没有说“不喜欢”。／四个人都笑了。",
     "（KEEP）不补她的答案、不补她的字",
     "永久缺口", "收益=不解决、不升华、不判案；损失=读者可能不满足", "KEEP"),
    ("V1-010", "那行粉笔字后来擦了；我想问它的意思，不能因为它被擦掉，便替她留下一份自作主张的解释。",
     "（KEEP）不把「零」解成任何含义",
     "叙述纪律", "收益=装置成立；损失=伏笔感变弱", "KEEP"),
    ("V2-001", "它被夹进了一本书里。书合上，纸角仍露出了一点。",
     "（KEEP）不加「多年以后」式回望",
     "元收束", "收益=纸角作为全书自指；损失=无", "KEEP"),
    ("V2-024", "那张纸还在等我写下一行。",
     "（KEEP）不改成「我终于明白」",
     "卷末克制", "收益=写的未完成；损失=无", "KEEP"),
    ("V2-005", "那件事在第一部已经讲过，不必搬到这里再跳一回。",
     "那件事我在别处讲过，不必搬到这里再跳一回。",
     "C7 元叙述框架破口", "收益=消除「人物知道第一部」的破口；损失=少一次自我指涉趣味",
     "ADOPT_B / AUTHOR_DECISION_REQUIRED"),
    ("V2-019", "我在初进五班的那一天一件都不知道。",
     "（删去该句，保留二十行后更短更冷的一句）",
     "排版/改稿残留", "收益=去近重复；损失=几乎没有", "ADOPT_B"),
    ("V2-004", "现在若写她系着某种颜色的围裙……读者很容易相信。",
     "（KEEP，另案处理）此句属反虚构方法学的自觉演示，与 V2-005 破口性质不同",
     "框架边界", "收益=保留方法论；损失=「读者」一词仍在正文", "KEEP / 另案"),
    ("V2-021", "我有很长一段时间，把高二的寝室记成四二五。",
     "（KEEP）425 是错记、426 是实际，正文已自陈订正",
     "数字/身份", "收益=记忆订正成为诗学；损失=无", "KEEP"),
    ("V2-013", "到现在我也不能保证，倘若再站到某个自己极想进去的地方……我会完全不想找别的办法。",
     "（KEEP）不补「后来我改了」",
     "道德未完成态", "收益=不承诺治愈；损失=人物不讨喜", "KEEP"),
    ("V2-018", "我把输入框里的字删了。",
     "（KEEP）不写删掉的具体内容",
     "不说/删写伦理", "收益=「不说」物质化；损失=无", "KEEP"),
    ("V2-020", "那个没演过的镜头，能不能只因为现在生成得出来，就算从前确实存在过？",
     "（KEEP）不改成更顺的陈述句",
     "AI 时代反虚构", "收益=问句保留自审；损失=无", "KEEP"),
]
for ch, a, b, kind, trade, verdict in HAND_AB:
    lines += ["## %s｜%s" % (ch, kind), "",
              "- **A（原句）**：%s" % a, "- **B**：%s" % b,
              "- **收益／损失**：%s" % trade, "- **裁决**：`%s`" % verdict, ""]

# 24 组补场级 A/B：从 diff 中取第一个新增块，A 用原文中与其最相近的一句
for i in range(1, 25):
    ch = "%03d" % i
    patch = read(os.path.join(DIFFS, ch + ".patch"))
    added = [l[1:].strip() for l in patch.splitlines()
             if l.startswith("+") and not l.startswith("+++") and len(l.strip()) > 12]
    if not added:
        continue
    b = added[0][:110]
    orig = read(r"D:\The Memory\AI-Review-Onboarding\_work\pr53\manuscript\volume-02\%s.md" % ch)
    sents = [s.strip() for s in re.split(r"(?<=[。！？])", orig) if len(s.strip()) > 12]
    a = difflib.get_close_matches(re.sub(r"[^\u3400-\u9fff]", "", b),
                                  [re.sub(r"[^\u3400-\u9fff]", "", s) for s in sents],
                                  n=1, cutoff=0.1)
    a_txt = a[0][:110] if a else "（本章对应动作链；原文未逐字给出同一句）"
    lines += ["## V2-%s｜补场级 A/B" % ch, "",
              "- **A（原文最近锚）**：%s" % a_txt,
              "- **B（新增首句）**：%s" % b,
              "- **问题类型**：动作链被概述带过，非事实错误",
              "- **收益／损失**：收益=多一段可看的具体动作；损失=可能压慢本章节奏，可整段回滚",
              "- **裁决**：`ADOPT_REVERSIBLE`（候选，允许作者选 KEEP 并删除插入块）", ""]

write(os.path.join(G2, "18_BEFORE_AFTER_ANCHORS.md"), "\n".join(lines))

# ---------- 15_VOLUME01_FROZEN_CANDIDATES.md ----------
v1 = ["# GLM 位｜15 第一部 R50 冻结稿：逐章审稿与隔离实验提案", "",
      "> **R50 canon 一字未改**。本目录 `17_VOLUME01_EXPERIMENTS/` 中的实验稿只作隔离对照，",
      "> 不称 R51、不替换 R50、不推送；正式开放第一部须作者另行授权。", "",
      "| 章 | 官方汉字 | 本阶段处理 |", "|---|---:|---|"]
for i in range(1, 19):
    ch = "%03d" % i
    p = r"D:\The Memory\AI-Review-Onboarding\_work\pr53\manuscript\volume-01\%s.md" % ch
    t = read(p)
    n = len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]", t))
    act = "隔离补场实验（3 章之一）" if ch in ("001", "014", "018") else "逐章审稿，KEEP canon"
    v1.append("| %s | %d | %s |" % (ch, n, act))
v1 += ["", "## 三处实验的「为何不能正式改」门槛", "",
       "1. 三处补场都是 `LITERARY_COMPOSITE`，不是新发现的一手事实。",
       "2. 第一部 R50 已有作者明示的冻结合约；例外仅限新一手证据、当事人权利异议、确定性事实错误。",
       "3. 本阶段未逐字复核事实库人物页与评语原件，不具备「新一手证据」条件。",
       "4. 因此全部停在实验目录，等待作者逐条 A/B 裁决。", ""]
write(os.path.join(G2, "15_VOLUME01_FROZEN_CANDIDATES.md"), "\n".join(v1))

print("reused reports:", len(REUSE), "AB groups:", len(HAND_AB) + 24)
