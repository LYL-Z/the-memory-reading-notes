# r2｜00 基线、执行环境与授权边界（最终交付版）

项目：《时间的复数人称》DeepSeek V4.1-Flash **r2 独立全量深读**
版本：2026-11-12 · Read-First / Audit-Ready / No-Manuscript-Write
执行主体：r2 会话（自中断点续作，Doubao→本会话）；主控独立复核并交付
状态：**P0—P5 交付完成；正式修稿未启动**

> **与根目录共享活文档的关系（重要）**
> 根目录 `../00_baseline_and_scope.md` 是 r1／r2 两轮共享的活文档（其 §12.4 C 明文规定「不另复制」）。本文件**不是**对它的复制，而是 r2 最终交付物清单中的「基线快照与执行边界」：记录本轮交付时点实时核验到的 commit、产物目录、覆盖范围与不可宣称项。两轮共享活文档继续原位追加，本文件与之并存、不覆盖、不改写。

---

## 一、结论先行（本轮交付时点实测）

1. 三个源全部真实可读，且已核验到 commit 级：创作仓 PR #53 head `2307305837932f6196ce300fc67f26ed8db3ac11`、事实库 master `ef33c98d63b88283e840f5414db154eb9118c4e4`、r2 独立工作目录 `D:\The Memory\AI-Review-Onboarding\DeepSeek-V4.1-Flash\`。不存在「本地不可访问」或「只能读 main」。
2. 现行正文 = **第一部 18 章（R50 冻结，main 与 PR 链逐文件一致）+ 第二部 24 章（main 只有旧版 001–005；PR #51 提供 001–018 的 R7 候审版；PR #52 追加 019；PR #53 追加 020–024）**，共 42 章。`main` 的「第二部只有 5 章」是假象，不能作阅读基线。
3. 官方字数（本轮在 `_work/pr53` 实跑 `python scripts/hanzi_count.py`）：**V1 = 136,693；V2 = 135,374；合计 272,067**。r2 卡片的正则 `[\u4e00-\u9fff]` 口径为 V1 136,763／V2 135,473／合计 272,236，差 169 字，来自标题、标点与计数规则差异；**两种口径不得混用**，本文件与 03/04 号交付物引用官方口径时显式标注。
4. r2 冷读回执 = 44 个文件（V1 18 卡 + `v1a/wrap.md`；V2 24 卡 + `v2b/wrap.md`），全部 `full_read` 至 EOF，每卡含逐字锚点与物理行号。
5. **本轮对 44 张卡中的 42 张章节卡做了机器逐字回查**：521 条锚点，**512 条 EXACT PASS（98.27%），9 条 MISS**。9 条全部为卡片侧引文加工（合并两行、省略号跳接、改标点、漏字、改前缀），**不是正文版本漂移**；逐条诊断与正文逐字原文见 `anchor_verification.csv`。本轮**不虚报「0 失配」**，也不改写前序卡片，只登记可恢复的订正账。
6. r2 正式交付物写入 `r2/` 子目录（依共享活文档 §12.4 C，避免覆盖 r1 同名文件，保留作者两轮比较权）。**源仓库、事实库、既有 PR／分支、小说正文零改动**。

---

## 二、实时核验值（2026-11-12，本轮交付前重跑）

| 项 | 实测值 | 取得方式 |
|---|---|---|
| 创作仓 `main` | `bad5b23483fd21c8f65423ff3747c095e06c0759` | `git -C _work/reading-notes rev-parse origin/main` |
| 创作仓 PR #51 head | `017ef32da134c0292906e0d4ebcb843e7f50a627` | worktree `_work/pr51` |
| 创作仓 PR #52 head | `6b6d90c582c06edfaaf4941d7c5824ee9086fd3c` | worktree `_work/pr52` |
| 创作仓 **PR #53 head（阅读基线）** | `2307305837932f6196ce300fc67f26ed8db3ac11`（2026-11-12 01:51:41 -0800） | worktree `_work/pr53`，`git rev-parse HEAD` |
| 创作仓 PR #53 树文件数 | **443** | `git ls-tree -r -l` |
| 其中正文 md | **42** | 同上，`manuscript/volume-0{1,2}/` |
| 创作仓 `reading-notes` 工作分支 | `deepseek/phase1-2-candidate-20261112`，HEAD `a2e329b0710cc42b7d57a73de2098911abc5a331` | `git rev-parse HEAD` |
| 该分支已 tracked 的 deepseek 文件 | **300** | `git ls-tree -r --name-only HEAD | grep '^deepseek'` |
| 事实库 master | `ef33c98d63b88283e840f5414db154eb9118c4e4`（2026-11-08 01:41:44 -0800） | `git -C D:\The Memory\The Memory rev-parse HEAD` |
| 事实库工作区 | **clean（0 dirty）** | `git status --short` |
| 事实库文件／Markdown | **2,297 / 892** | `os.walk`（排除 .git） |
| 事实库 `私人资料/` Markdown | **47**（仅目录级登记，零正文读取、零哈希计算） | 同上 |
| r2 工作区文件 | 见 `00_repo_manifest.csv` 源 C 段 | `os.walk` |
| 外部 URL 登记 | **23** 条，分 FULL_TEXT / PARTIAL_VIEW / METADATA_ONLY / BLOCKED / SEARCH_CACHE | 见 `09_external_research_MLA.md` |

> 远端 PR 链已推进至 #51（第二部前 18 章 R7）、#52（019）、#53（020–024 终章）。本轮**只把它们当阅读基线与版本对照**，未对任何 PR 做 head/base 修改、未 force push、未合并 main、未重写历史。

---

## 三、三源定义与隔离

### A. 创作仓（主基线，只读）
- 远端 `https://github.com/LYL-Z/the-memory-reading-notes`（public，default branch `main`）。
- 本地只读副本 `_work/reading-notes`（clone）+ 四个 detached worktree：`_work/main`、`_work/pr51`、`_work/pr52`、`_work/pr53`（`git worktree list` 实测）。
- 现行规范入口（本轮全文读）：`AGENTS.md`、`editorial/authority_conflicts.md`、`editorial/narrative_design.md`、`editorial/reading_coverage.md`、`editorial/volume02/2026-11-08-b2-first-24chapter-reading-order-v2.md`、`editorial/volume02/2026-11-08-24chapter-aesthetic-revelation-and-audio-map.md`、`editorial/style-and-influences/2026-11-08-author-voice-anti-template-and-evidence-protocol.md`。
- `AGENTS.md` 硬约束：不读、不仿、不续写 `百万长文写作/`、`长篇创作/`、`正式成文/`、外层 `小说连载稿/`、`《19年回忆录》`；事实以人物页、用户订正、口述与同时期记录为准；推测留 `editorial/`，不写进读者正文；别人未确认的内心、原话和关系名称不能写成已证事实；字数只认 `scripts/hanzi_count.py`。

### B. 事实库（只读）
- 远端 `https://github.com/LYL-Z/the-memory`（default `master`），本地 `D:\The Memory\The Memory`。
- 本轮**未逐字重读事实库人物页**：r2 卡片「存疑与待核」中列出的待核路径，一律登记为 `PENDING_FACT_CHECK`（见 `01_reading_ledger.csv` 与 10 号文件）。这是 r2 与 r1 覆盖范围的诚实差异，不冒充「已核事实库」。
- 私密层 `私人资料/`：**不读正文、不摘录、不引用、不计算哈希**；`00_repo_manifest.csv` 中该层 SHA256 一律填 `WITHHELD_PRIVATE_LAYER`。

### C. 独立工作目录（唯一写入区）
- `D:\The Memory\AI-Review-Onboarding\DeepSeek-V4.1-Flash\`，在三源之外、源仓库之外。
- `r2/` 为本轮 13 项正式交付物 + `anchor_verification.csv` + `checksums.sha256`。
- 根目录 r1 命名空间（`00`–`12`、`checksums.sha256`、`cards/`、`sections/`）原位保留，不改写。

---

## 四、版本矩阵与状态标签

| 分支 / PR | Head | 覆盖第二部 | 状态 |
|---|---|---|---|
| `main` | `bad5b234` | 001–005（旧版） | CANON-MAIN（旧） |
| PR #51 | `017ef32d` | 001–018（R7） | DRAFT-REVIEW |
| PR #52 | `6b6d90c5` | 001–019 | DRAFT-REVIEW |
| **PR #53** | `23073058` | **001–024** | **DRAFT-REVIEW（本轮基线）** |

标签口径：第一部 001–018 = `CANON-FROZEN`（冻结不等于完美）；第二部 001–018 = `DRAFT-REVIEW(R7)`；019 = `DRAFT-REVIEW(PR #52)`；020–024 = `DRAFT(PR #53 新增，尚无审稿史)`。历史审稿 = `HISTORICAL`；私密层 = `LOCAL_ONLY`；互相矛盾 = `CONFLICT`；无法判定 = `UNKNOWN`。

---

## 五、覆盖策略与诚实声明

| 项目 | 本轮实测 | 判定 |
|---|---|---|
| 正文全读 | 42/42 章，逐章到 EOF（r2 卡 42 张 + 2 张卷级小结） | PASS |
| 章节逐字锚点机器回查 | 521 条，512 EXACT PASS，9 MISS（全为卡片加工，逐条诊断） | **PARTIAL（不虚报 0 失配）** |
| 创作仓 | 443 文件全部登记路径/字节/SHA256；全文精读 42 章 + 7 份规范 | PARTIAL |
| editorial 其余档案 | 登记为 `metadata_only`，未逐字精读 | PARTIAL |
| 事实库 | 2,297 文件登记；892 份 Markdown 本轮 `metadata_only`；47 份私密层 `not_read` | PARTIAL |
| 外部研究 | 23 条 URL；FULL_TEXT 级 9 条、PARTIAL_VIEW 2 条、METADATA_ONLY 2 条、BLOCKED/404/SEARCH_CACHE 等 10 条 | PARTIAL |
| 真人冷读 | **0** | 未执行 |
| R50 冻结验证器 | **本轮未运行**（r1 曾记录 PASS；不沿用其回执） | 未执行 |
| 源仓库/事实库/PR 改动 | **0** | 合规 |

**不可宣称**：三源 100% 通读；真人冷读；出版级终审；世界级文学已达成；锚点零失配；PR 已合并或作者已验收；事实库人物页已逐字复核。

**本轮唯一允许的完成表述**：以 PR #53 head 为基线，第一部 18 章与第二部 24 章已逐章全读并留下可复核锚点（512/521 逐字通过，9 处卡片加工已登记订正账）；现行规范已全文精读；外部研究由 r2 自己重新抓取并分级登记；事实库与创作档案按优先范围登记到「可支撑后续审稿调用」的程度。

---

## 六、交叉阶段材料来源与纪律

依共享活文档 §12.3／§12.4：r2 不把 r1 卡片当自己的回执，冷读完成后才进入「读后查证」层。

- **r2 结论的一手依据**：42 张 r2 章节卡、2 张卷级小结、本轮对 PR #53 正文的逐字回查、本轮全文精读的 7 份现行规范、本轮自己抓取的 23 条外部 URL。
- **仅作对照、不作依据**：`sections/lead_notes.md`（标注「Lead 独立阅读笔记」）、`sections/03_cross.md`／`04_cross.md`（标注「主控综合」）、`sections/03_intro.md`／`04_intro.md`（r1 连续冷读草稿）、根目录 r1 的 `00`–`12` 交付物。
- **声明过的有限例外**：为补齐外部研究 BLOCKED 项，本轮读取了 r1 `09_external_research_MLA.md` 与 `12_future_review_plan_NO_EDIT.md` 的**来源 URL 与 BLOCKED 清单**，仅作检索起点。r2 的每一条引文、每一条验证级别判定，均来自 r2 自己 2026-11-12 重新抓取的页面；**未引用 r1 的任何理论结论、字数判断或修订建议**。
- 引用 `sections/` 中的词频统计时，一律标注 `CROSS_NOTE_UNVERIFIED_BY_R2`；r2 本轮未重跑全书词频，不把该数字当自己的实测。

---

## 七、隐私与外部使用

- 报告只做最小必要摘录；私密层原文、证件号、手机号、精确门牌一律不进入交付物。
- 交付物中出现的人名均来自**现行正文已公开出现**的写法；不把作品推断写成对现实人物的心理诊断；不根据面部外貌识别个人；不建立真人外貌／神态档案。
- 外部研究只检索公开文学理论、访谈与作品信息，未把任何私密材料粘贴到搜索或网页。
- 已知独立风险（与本项目其他轮次一致，本轮不处理）：公开仓库候审稿的历史提交与 PR 累积 diff 中仍有 `P0_BLOCKED_AWAIT_AUTHOR_AUTHORIZATION` 级残留；层 2（历史重写／GitHub Support）须作者单独授权，本轮未执行，也未改变仓库公开性。

---

## 八、交付物清单（本目录）

`00_baseline_and_scope.md`｜`00_repo_manifest.csv`｜`01_reading_ledger.csv`｜`02_canon_and_authority_matrix.md`｜`03_volume01_continuous_read.md`｜`04_volume02_continuous_read.md`｜`05_character_evidence_atlas.md`｜`06_dual_timeline_and_reader_knowledge.md`｜`07_cross_volume_structure_and_echoes.md`｜`08_style_voice_and_ai-pattern_diagnostics.md`｜`09_external_research_MLA.md`｜`10_unresolved_questions_and_conflicts.md`｜`11_independent_understanding_report.md`｜`12_future_review_plan_NO_EDIT.md`｜`anchor_verification.csv`（附加证据）｜`checksums.sha256`。

---

## 九、变更记录

- 2026-11-12 r2 会话：完成 42 章冷读并落盘 44 卡（见共享活文档 §12.4 A）；因额度中断于「V2 全部 24 章冷读完毕，准备进入 Editorial 规范深读」。
- 2026-11-12 续作会话：实时重核三源与 PR 链；全文精读 7 份现行规范；重新抓取 23 条外部来源；生成三源清单／阅读台账／锚点机器核验；写出 13 项正式交付物；提交独立 GitHub 分支与 Draft PR。**全过程零正文改动、零事实库改动、零 PR 改动、零 force push、零历史重写、零合并 main。**
