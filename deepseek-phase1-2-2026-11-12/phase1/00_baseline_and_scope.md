# 00 基线、执行环境与授权边界

项目：《时间的复数人称》DeepSeek V4.1-Flash 独立全量深读
版本：2026-11-12 · Read-First / Audit-Ready / No-Manuscript-Write
执行主体：DeepSeek V4.1-Flash（DeepSeek Harness 会话，Team Lead + 阅读/研究分队）
状态：P0 已完成；P1–P5 已完成（正文全覆盖，仓库/事实库/外部研究为 PARTIAL，见第十二节）。

## 一、结论先行

1. 三个源都真实可访问，且已分别核验到 commit 级：创作仓库工作树（PR #53 head 23073058）、事实库（master ef33c98）、本地目录（即事实库工作副本，工作区干净）。不存在"本地不可访问"或"只能读 main"的情况。
2. 现行正文的真实版本结构是：**第一部 18 章（R50 冻结，main 与 PR 链完全一致）+ 第二部 24 章（main 只有旧版 001–005；PR #51 提供 001–018 的 R7 候审版；PR #52 追加 019；PR #53 追加 020–024，更新时间为 2026-11-12 01:51 -0800）**。因此"第二部只有 5 章"是 main 的假象，不能作为阅读基线。
3. 三个源之外的工作目录已建立：`D:\The Memory\AI-Review-Onboarding\DeepSeek-V4.1-Flash\`。所有产物只写在这里；源仓库零修改（本轮核验时两库工作区均为 clean）。
4. 事实库共 2297 个文件、892 个 Markdown；其中 47 个 Markdown 位于被 .gitignore 排除的 `私人资料/`，属**仅本地、不可公开引用**层。本报告与全部产物不摘录私密原文。
5. 本阶段可核验的硬事实：42 章正文合计 272,236 个汉字（按正则统计，含正文与标题；官方口径第一部 136,693，统计差异见第六节）。42 章全文字节级 SHA256 已逐章记录，可用于任何后续版本对照。

## 二、执行宿主与工具可用性（P0-1）

| 项目 | 实测结果 | 证据 |
|---|---|---|
| 宿主 | Windows，DeepSeek Harness（DSH）会话，工作目录 `D:\The Memory` | 运行环境 |
| 文件系统 | 可读可写；三源路径均真实存在 | `Test-Path` = True |
| Git | 可用；本地事实库 `D:\The Memory\The Memory` 为 git 仓库 | `git rev-parse` 成功 |
| GitHub CLI | 已登录 LYL-Z（token scopes: gist, read:org, repo, workflow） | `gh auth status` |
| 网络 | 可直连 GitHub API（HTTP 200）；未使用失效代理 | `Invoke-WebRequest api.github.com/rate_limit` |
| 浏览器/抓取 | `web_fetch` / `web_search` / 浏览器工具可用（外部研究条目须逐条实际抓取） | 见 09 文件 |
| 本地创作仓副本 | 未发现完整的独立 clone；`D:\The Memory\tmp\reading-notes-*` 为历史轮次的局部工作副本，不作为基线 | 目录检查 |

未使用任何"假装执行"的替代：不能抓取的页面在 09 中标注 BLOCKED。

## 三、三个源的定义与核验值（P0-2）

### A. 创作仓库（主基线）

- 远端：https://github.com/LYL-Z/the-memory-reading-notes （public；default branch `main`；pushed_at 2026-11-12T09:51:41Z）。
- 本地只读工作副本：`D:\The Memory\AI-Review-Onboarding\_work\reading-notes`（clone 于 2026-11-12，另建 4 个 detached worktree 用于版本对照）。
- `main` = **bad5b23483fd21c8f65423ff3747c095e06c0759**（2026-11-08 00:38:34 -0800，"Merge PR #22: Volume II chapters 01–05 final editorial phase"）。
- 最新候选基线 = **PR #53 head 2307305837932f6196ce300fc67f26ed8db3ac11**（2026-11-12 01:51:41 -0800，"state: mark five volume II finale chapters complete, preserve history and author gate for volume III"）。
- 工作树 443 个文件（含 42 章正文、315 个 editorial 文档、outline/state/evidence/work/tools/.cursor 等）。

### B. 事实库（原始 Obsidian）

- 远端：https://github.com/LYL-Z/the-memory （default branch `master`；**只读**）。
- 本地工作副本：`D:\The Memory\The Memory`。
- 本地 HEAD = **ef33c98d63b88283e840f5414db154eb9118c4e4** = 远端 `master` SHA（2026-11-12 核验一致）。
- 工作区 clean（`git status --short` 无输出）。
- 文件 2297 个（不含 .git），Markdown 892 个；tracked 文件 890 个；`私人资料/` 被 .gitignore 排除（本地 47 个 Markdown + 图片，仅本地）。
- 冲突核验：本地与远端同 SHA，不存在"本地未同步"问题；但**本地有远端没有的私密层文件**，这是设计使然，不是版本差异。

### C. 本地工作目录

- 任务书要求核验的 `D:\The Memory\The Memory` 就是事实库的本地工作副本（同一 git 仓库），不是第四种材料。
- 外层 `D:\The Memory` 下另有历史轮次目录（`审稿交付\`、`小说连载稿\`、`tmp\reading-notes-*`、`NovelStudio_Grok47\` 等）。任务书明确：历史连载稿与旧工程不得当作现稿，也不得模仿其文风；本报告只在版本沿革意义上登记，不作为文学判断依据（旧稿阅读状态：登记，未纳入现稿冷读）。

## 四、版本矩阵：PR 链与正文覆盖

| 分支 / PR | Head commit | 时间（本地时区） | base | 覆盖第二部章节 | 状态 |
|---|---|---|---|---|---|
| `main` | bad5b234 | 2026-11-08 00:38 | — | 001–005（旧版） | CANON-MAIN（旧） |
| PR #51 `chatgpt/volume02-18chapter-literary-overhaul-r1-20261111` | 017ef32d | 2026-11-11 20:01 | hy4/ch18-independent-review-20261111 (0fc6ebe2) | 001–018（R7） | DRAFT-REVIEW |
| PR #52 `chatgpt/volume02-ch19-right-front-r1-20261111` | 6b6d90c5 | 2026-11-11 20:32 | 017ef32d | 001–019 | DRAFT-REVIEW |
| PR #53 `chatgpt/volume02-ch20-24-finale-r1-20261112` | 23073058 | 2026-11-12 01:51 | 6b6d90c5 | 001–024 | DRAFT-REVIEW（最新） |
| PR #50 及以前 | — | ≤2026-11-11 | — | 第18章及以前的历史审稿 | HISTORICAL |

已核验的版本事实：

1. **第一部 001–018 在 main、PR #51、PR #53 中逐文件 SHA256 完全一致**，即 R50 冻结版没有被后续 PR 改动。
2. 第二部 001–005 在 main 与 PR #51 中**不同**（SHA 不同）；main 是 2026-11-08 已合并的旧版，PR 链是后续 R7 精修版。阅读基线采用 PR #53（含 PR #51 的 001–018），main 版本仅用于版本对照。
3. 第二部 006–018 不存在于 main；019 只存在于 PR #52/#53；020–024 只存在于 PR #53。
4. 因此本任务的"现行正文"= 第一部 18 章（冻结）+ 第二部 24 章（候审链），共 42 章。不能把 main 的 5 章当作第二部全貌。

## 五、章节清单与状态（42 章，PR #53 树）

统计口径：行数 = 文件物理行数；汉字数 = 正则 [\u4e00-\u9fff] 计数（含章节标题与文件内注释性文字，故略高于"官方正文汉字"）；SHA256 为文件级。

| 卷 | 章 | 标题 | 行数 | 汉字 | SHA256 前 12 | 状态 |
|---|---|---|---|---|---|---|
| 一 | 001 | 左边的位置 | 315 | 7,742 | 77eb43053e4a | CANON-FROZEN |
| 一 | 002 | 晚饭后的桌子 | 311 | 10,581 | 6cdaee589131 | CANON-FROZEN |
| 一 | 003 | 525 | 261 | 11,050 | e870681513c7 | CANON-FROZEN |
| 一 | 004 | 月考之后 | 281 | 11,919 | 03a6058a7bb4 | CANON-FROZEN |
| 一 | 005 | 盒饭 | 195 | 6,170 | e64b21c15cd0 | CANON-FROZEN |
| 一 | 006 | 一只福袋 | 221 | 7,259 | a3762679f0b8 | CANON-FROZEN |
| 一 | 007 | 答案放在桌上 | 243 | 8,181 | 3d62f193bea7 | CANON-FROZEN |
| 一 | 008 | 两周 | 301 | 7,086 | 5948dc134d6d | CANON-FROZEN |
| 一 | 009 | 讲台两侧 | 297 | 7,864 | 01f12c443b51 | CANON-FROZEN |
| 一 | 010 | 那个零 | 227 | 5,052 | 8f10b36605f2 | CANON-FROZEN |
| 一 | 011 | 竞赛班门口 | 335 | 9,190 | d06ed7facd8c | CANON-FROZEN |
| 一 | 012 | 橘子洲 | 223 | 6,323 | 9bf12e79ea6c | CANON-FROZEN |
| 一 | 013 | 婚礼进行曲 | 269 | 6,758 | eeca3ea8f671 | CANON-FROZEN |
| 一 | 014 | 勇敢一点 | 375 | 7,374 | bd7bf5664de0 | CANON-FROZEN |
| 一 | 015 | 陈喜在门口 | 281 | 6,334 | e5bc960b118e | CANON-FROZEN |
| 一 | 016 | 小红帽 | 241 | 5,407 | 2b66d186f5fd | CANON-FROZEN |
| 一 | 017 | 竹林杯 | 127 | 5,542 | f5fdd4107584 | CANON-FROZEN |
| 一 | 018 | 历史课 | 315 | 6,931 | 7ecb7e20e437 | CANON-FROZEN |
| 二 | 001 | 一个人的客厅 | 171 | 6,360 | d912666e61c7 | DRAFT-REVIEW |
| 二 | 002 | 二班 | 139 | 4,918 | f4d784866185 | DRAFT-REVIEW |
| 二 | 003 | 后门 | 153 | 5,751 | 1fe7ac9576c7 | DRAFT-REVIEW |
| 二 | 004 | 三餐 | 149 | 6,377 | 6284b5891508 | DRAFT-REVIEW |
| 二 | 005 | 借来的床 | 171 | 6,513 | 9416a35cef4d | DRAFT-REVIEW |
| 二 | 006 | 轮到谁说话 | 99 | 4,190 | e7573277b4b9 | DRAFT-REVIEW |
| 二 | 007 | 没做完的作业 | 110 | 3,665 | 854ff99fabbc | DRAFT-REVIEW |
| 二 | 008 | 一百三零五 | 229 | 8,892 | aaec96645976 | DRAFT-REVIEW |
| 二 | 009 | 父亲讲过的 | 221 | 7,406 | faa341d96023 | DRAFT-REVIEW |
| 二 | 010 | 考过以后 | 153 | 4,763 | c7730afc5b6d | DRAFT-REVIEW |
| 二 | 011 | 两处地点 | 123 | 4,563 | a957d514bf34 | DRAFT-REVIEW |
| 二 | 012 | 打过去的球 | 157 | 5,671 | 01c8fa0c70aa | DRAFT-REVIEW |
| 二 | 013 | 再找一遍 | 179 | 6,172 | 2aa9444eea34 | DRAFT-REVIEW |
| 二 | 014 | 母亲那边 | 233 | 7,722 | b894770fac09 | DRAFT-REVIEW |
| 二 | 015 | 食堂里 | 93 | 4,000 | d53c2289650f | DRAFT-REVIEW |
| 二 | 016 | 过年的路 | 121 | 5,221 | e7c01af372d2 | DRAFT-REVIEW |
| 二 | 017 | 垃圾桶 | 165 | 6,295 | 70133c9a524f | DRAFT-REVIEW |
| 二 | 018 | 老师怎么写我 | 317 | 7,500 | 8c5bee4b81e8 | DRAFT-REVIEW |
| 二 | 019 | 右前方 | 253 | 6,665 | a80b0b6825a4 | DRAFT-REVIEW（PR #52） |
| 二 | 020 | 后来都拿起手机 | 166 | 4,710 | 6eff5682283a | DRAFT（PR #53 新增） |
| 二 | 021 | 四二五 | 163 | 4,414 | 96f9346b0fd2 | DRAFT（PR #53 新增） |
| 二 | 022 | 小林子 | 163 | 4,506 | f88b46c877d8 | DRAFT（PR #53 新增） |
| 二 | 023 | 有人听我讲 | 188 | 4,823 | 50c05cbf860b | DRAFT（PR #53 新增） |
| 二 | 024 | 名单之外 | 183 | 4,376 | a6c08f02f1c9 | DRAFT（PR #53 新增） |

合计：42 章，272,236 汉字（原始统计）。第一部 136,763；第二部 135,473。

## 六、字数口径差异（须在引用时说明）

- 仓库官方口径：第一部 R50 = **136,693 个官方汉字**（README / state 记录，使用 `scripts/hanzi_count.py`）。
- 本表正则口径：第一部 136,763。差值 70，来自标题、frontmatter 或标点规则差异，不影响章节级判断。
- 第二部官方口径散落在各轮记录（例如 001–005 = 32,956；PR #51 声称章节数见 state；PR #53 记录 020–024 完成）。任何引用必须注明口径来源，不能把两种统计混用。

## 七、事实库结构与私密边界

- 顶层目录（按 Markdown 数量）：高中 235、文化与审美 106、百万长文写作 82、背景资料 61、大学 51、私人资料 47、写作体系 44、长篇创作 34、问卷回收 31、初中 31、项目管理 30、家庭 30、正式成文 15、小学 13、根目录 10、其他（Excalidraw/人物关系/隐私/公开脱敏资料等）若干。
- 索引入口：`00-知识库首页.md`、`知识库架构总览.md`、`知识库总索引.md`、`LLM检索逻辑指南.md`、`时间线索引.md`、`主题线索引.md`、`人物标准库.md`、`人物总索引.md`、`人物出场索引.md`。
- 写作体系（创作规范）与"现行作品规范"必须区分：写作体系是知识库中的规划，现行规范在创作仓库 `AGENTS.md`、`editorial/style-and-influences/`、`editorial/clocks.md`、`editorial/literary-craft-playbook-for-volume-02.md`。
- 历史旧稿（`百万长文写作/`、`长篇创作/`、`正式成文/`、外层 `小说连载稿/`、《19年回忆录》连载文本）：仅登记工程沿革，不作现稿冷读、不模仿其文风（依创作仓库 AGENTS.md 第 2 条）。
- **私密层**：`私人资料/` 被 .gitignore 排除，仅存本地。本任务不读其正文、不摘录、不引用、不进入公开报告。若某字段只能由私密层确认，报告写"受限，未核"。

## 八、输出目录与文件计划

所有产物位于 `D:\The Memory\AI-Review-Onboarding\DeepSeek-V4.1-Flash\`（三源之外）：

```
00_baseline_and_scope.md       本文件（P0）
00_repo_manifest.csv           三源文件清单（路径/类别/大小/SHA256/来源）
01_reading_ledger.csv          文件级阅读台账（full_read/partial/metadata_only/visual_inspected/skipped/blocked）
02_canon_and_authority_matrix.md   现行/历史/冲突/待裁决
03_volume01_continuous_read.md     第一部 18 章连续冷读
04_volume02_continuous_read.md     第二部 24 章连续冷读
05_character_evidence_atlas.md     人物证据图
06_dual_timeline_and_reader_knowledge.md  双时钟与读者知情
07_cross_volume_structure_and_echoes.md   跨卷结构与回响
08_style_voice_and_ai-pattern_diagnostics.md  声口与 AI 模式诊断
09_external_research_MLA.md        外部研究（MLA）
10_unresolved_questions_and_conflicts.md  未解问题与冲突
11_independent_understanding_report.md    独立理解报告
12_future_review_plan_NO_EDIT.md   下一轮审稿路径（不修改）
checksums.sha256                   全部产物校验
cards/                             逐章/逐人物证据卡（中间产物，可恢复）
sections/                          报告分段草稿
```

## 九、覆盖策略与已知限制（P0/P1 诚实声明）

1. **正文**：42 章全部逐字读到 EOF（分块 + 逐章卡片 + 引文回查）。这是本任务的第一优先级，不以摘要替代。
2. **创作仓库 443 文件**：全部登记清单与哈希；结构/规范/交接/审稿史类文档优先全读，其余按目录抽样并标注。315 个 editorial 文件不可能在本轮全部逐字读完，覆盖率与未读清单在 01 台账逐文件给出，不用"100%"掩盖。
3. **事实库 892 Markdown**：按"索引—人物—时间线—写作规范—作者订正—相关学段"优先读核心 200 份左右；其余登记为 metadata_only。私密层 47 份不读正文。全库 100% 逐字阅读在本轮不现实，报告只声称实际做到的覆盖。
4. **外部研究**：每一条必须有实际抓取的 URL、作者、标题、日期、验证级别；无法抓取的标注 BLOCKED，不编造引语。
5. **不可宣称**：本报告不是"真人冷读"，不是"出版级终审"，不宣称"世界级已达成"。旧 AI 审稿报告只作为待核对象，不作为事实来源。

## 十、与任务书 P0 要求的逐项对照

| 任务书 P0 要求 | 本文件对应 | 结果 |
|---|---|---|
| 列明宿主、CLI、文件与浏览工具是否可用 | 第二节 | PASS |
| 记录两仓默认分支 SHA | 第三节 | PASS（main bad5b234 / master ef33c98） |
| 候审 PR 的 base/head、继承关系、覆盖范围 | 第四、五节 | PASS（#51→#52→#53 链） |
| 篇章状态分类 | 第五节 | PASS（18 CANON-FROZEN + 24 DRAFT-REVIEW/DRAFT） |
| 不把 main/PR/工作稿混成"完整定稿" | 第四、六节 | PASS |
| 生成 00_baseline_and_scope.md、00_repo_manifest.csv、敏感规则 | 本文件 + 清单 + 第七节 | PASS |
| 输出路径在三源之外 | 第八节 | PASS |

## 十一、变更记录

- 2026-11-12 02:0x：建立本文件；核验三源；创建只读工作副本与四个版本对照 worktree；启动逐章冷读。
- 后续每次读取/修正在此追加，不覆盖历史。

---

## 十二、r2 会话衔接记录（2026-11-12 追加，执行者：Doubao，按 DeepSeek 位启动提示词进入）

依本文件第十一节"后续每次读取/修正在此追加，不覆盖历史"。r2 为用户重新发起的独立执行会话，输入为《双模型独立深读与文学审稿准备任务书》（D 盘根目录 19078 字节版本）与 DeepSeek V4.1-Flash 独立启动提示词；执行者为本会话模型（Doubao），产物仍写入本命名空间，供作者统一比较。

### 12.1 r1 前序运行盘点（2026-11-12 02:06–02:11，中断）
- r1 产物：本文件主体（一至十一节）、00_repo_manifest.csv（590KB）、cards/ 下 40/42 张章节卡（v1a 001–007、v1b 010–018、v2a 001–012、v2b 013–024；**缺 V1-008、V1-009**）、cards/fact 4 张规范卡、cards/fact/cast 18 张人物卡、cards/research/sources.csv、sections/ 三份草稿（03_intro、03_cross、lead_notes）。
- r1 未完成：01_reading_ledger.csv、02–12 全部交付文件、checksums.sha256、锚点机器核验。
- r1 卡片性质认定：同一 DeepSeek 侧命名空间的前序中间产物。按任务书"一次阅读回执只对应实际读取的版本与内容，不可沿用别人的阅读回执"，r2 不把 r1 卡片当自己的回执；每章 r2 卡完成后才作交叉对照（"读后查证"层），分歧登记进 10 号文件。

### 12.2 r2 独立复核结果（与 r1 逐项对照，全部实测）
| 项 | r1 记录 | r2 独立复核 | 一致性 |
|---|---|---|---|
| 创作仓 main HEAD | bad5b234 | bad5b23483fd21c8f65423ff3747c095e06c0759（_work\reading-notes，git rev-parse） | 一致 |
| PR #51 head | 017ef32d | 017ef32da134c0292906e0d4ebcb843e7f50a627（_work\pr51 worktree） | 一致 |
| PR #52 head | 6b6d90c5 | 6b6d90c582c06edfaaf4941d7c5824ee9086fd3c（_work\pr52 worktree） | 一致 |
| PR #53 head | 23073058 | 2307305837932f6196ce300fc67f26ed8db3ac11（_work\pr53；=origin/chatgpt/volume02-ch20-24-finale-r1-20261112，2026-11-12 01:51:41 -0800，当前全库最新 commit） | 一致 |
| 事实库 HEAD | ef33c98 | ef33c98d63b88283e840f5414db154eb9118c4e4 = origin/master；工作区 clean（0 dirty） | 一致 |
| pr53 树文件数（除 .git） | 443 | 443 | 一致 |
| 正文汉字（正则 [\u4e00-\u9fff]） | V1 136,763 / V2 135,473 / 合计 272,236 | 同口径重算：逐项一致 | 一致 |
| 章节文件 | 42 个 md | 42 个 md，清单逐一核对（volume-01 18 + volume-02 24） | 一致 |
| SHA256 抽查 | 见第五节 | V1-001=77eb43053e4a、V1-018=7ecb7e20e437、V2-001=d912666e61c7、V2-024=a6c08f02f1c9，四处全部一致 | 一致 |

r2 工具环境：Windows + PowerShell（会话 PATH 受限，git 用绝对路径 D:\Git\cmd\git.exe；gh 位于 C:\Program Files\GitHub CLI\gh.exe，外部研究阶段实测）；Read/Write/Edit/Grep/Glob 可用。远端实时性：pr53 head 即远端最新分支头，克隆于今日；如外部研究阶段发现远端更新，将在此追加。

### 12.3 r2 执行计划与卡片分层
- cards/r2/{v1a,v1b,v2a,v2b,fact,research}/：本会话逐章冷读卡片，每章 3–5 条逐字锚点（含行号），收尾统一用 Select-String -SimpleMatch 机器核验。r1 卡片原位保留不动。
- 冷读顺序：V1 001→018，V2 001→024（文件序即阅读序）。读章前不读 editorial 历史审稿与其他模型产物；规范与状态类（AGENTS.md、README.md、state 头部）已在基线阶段读取完毕。
- 预置信息声明（诚实记录）：state/next_actions.md 头部含 017–024 章的内容摘要与结构说明（操作状态记录，属基线必读），V1 与 V2-001–016 仅有轮次级修改记录。受此影响的观察在卡片中单独标注 [预置]。
- 版本口径：官方汉字数（scripts/hanzi_count.py）与本文件正则口径差异按第六节说明引用。


## 十二、最终覆盖与交付状态（2026-11-12 收尾实测）

| 项目 | 实测 | 判定 |
|---|---|---|
| 正文全读 | 42/42 章（第一部 18＋第二部 24），逐章到 EOF | PASS |
| 章节逐字锚点 | 375 条，主控脚本 grep，0 失配 | PASS |
| 事实/审稿引文 | 约 185 条（事实卡 109＋创作档案 76），脚本复核 | PASS |
| 创作仓库 | 443 文件全部登记；全读约 60（42 章＋18 份结构/规则/审稿） | PARTIAL |
| editorial 档案 | 315 个中 40 个全读（12.7%），其余按目录登记 | PARTIAL |
| 事实库 | 2297 文件 / 892 Markdown；62 个 Markdown 全读（7.0%）＋22 张人物卡 | PARTIAL |
| 私密层 | 47 个 Markdown、图片若干：目录级登记，零正文读取 | 合规 |
| 外部研究 | 38 条 URL：可读正文 22（58%），全文级 14，BLOCKED/作废 16 | PARTIAL |
| 交付文件 | 00—12 共 14 个顶层文件＋cards/sections＋checksums.sha256（162 个文件校验） | 完成 |

**不可宣称**：三源 100% 通读；真人冷读；出版级终审；世界级文学已达成；PR 已合并或作者已验收。

**本轮唯一允许的完成表述**：以 PR #53 head 为基线，第一部 18 章与第二部 24 章已逐章全读并留下可复核锚点；事实库与创作档案按优先范围读到"能支撑人物、时间、权威判断"的程度；外部研究完成可核来源 22 条、BLOCKED 如实登记。

### 12.4 r2 冷读完成与 r1 交付物实测更正（2026-11-12 r2 会话追加，执行者：Doubao）

**A. r2 冷读完成宣告**：P1 冷读全部完成——V1 18/18 卡（`cards/r2/v1a/001-018.md`＋`wrap.md`）＋V2 24/24 卡（`cards/r2/v2a/001-012.md`、`cards/r2/v2b/013-024.md`＋`wrap.md`），共 44 个文件，全部 full_read 至 EOF，每卡含逐字锚点（物理行号）。冷读禁令（editorial/历史审稿/r1 卡）自本节起解除，转入交叉阶段（任务 #4–#7）。

**B. r1 运行状态更正（实测推翻 12.1）**：12.1 曾记录"r1 未完成：01_reading_ledger.csv、02–12 全部交付文件、checksums.sha256、锚点机器核验"。本节实测（Get-ChildItem 时间戳）：上述文件**已全部存在**，产出时间 2026-11-12 02:12:49–02:21:13（02_canon 02:12:49 → 01_reading_ledger.csv 02:16:49 → 03/04_continuous_read 02:18:21 → 09_external_research 02:19:59 → checksums.sha256 02:21:13），恰在 12.1 所述"02:06–02:11 中断"之后。结论：**r1 在中断后已恢复运行并补完全部交付物**（含 375 条锚点核验，见其"收尾实测"表）；12.1 的"未完成"论断写于 r1 恢复之前，当时为真，现已过时，以本节实测为准。r1 的 13 项交付物（00-12＋checksums）现完整保留于本命名空间根目录，r2 一律不读不引不覆盖（其内容属 r1 回执；r2 交叉阶段只对照 r1 章节卡与 sections/lead_notes，交付物层面仅作存在性与时间戳登记）。

**C. r2 交付物路径决定**：任务书 P5 指定 13 项交付物路径为 `DeepSeek-V4.1-Flash\` 根目录，与 r1 已产出文件同名。为避免覆盖 r1 产物（12.3"r1 卡片原位保留不动"原则的同源义务）并保留作者对两轮运行的比较权，r2 的 13 项交付物改写入 **`DeepSeek-V4.1-Flash\r2\` 子目录**（仍在三源之外、源仓库之外，符合任务书"输出路径必须在三个源之外"）。00_baseline_and_scope.md 为两轮共享的活文档，继续原位追加，不另复制。
