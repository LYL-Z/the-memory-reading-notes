# 阅读范围、证据与边界

GLM 线（作者指定身份）｜2026-11-25｜分支 `creative/volume08-glm-independent-masterplan`，起点 `main@3f79d2a`

这份账只回答一个问题：我凭什么对这部小说说话。读法分三档：全文精读、局部精读、目录与检索了解。**不把目录扫描、关键词检索当作精读**；凡未亲读处，注明替代依据。

## 0. 仓库状态（开工时核验）

| 仓库 | 路径 | 状态 |
|---|---|---|
| 创作仓 the-memory-reading-notes | `D:\The Memory\the-memory-reading-notes` | `origin/main@3f79d2a`；glm 分支自该提交切出，工作树干净；另有 `ref-pr93` 只读检出（`ee3bf7d`，即 PR #93 分支头），仅供阅读 PR #93 |
| 事实仓 the-memory | `D:\The Memory\The Memory` | `master` 与 `origin/master` 一致；只读，未作任何改动 |

两仓均已 fetch 同步。远程存在 claude、grok、kimi、qwen4、deepseek 各独立分支与多个第八部 PR（#93 OPEN 等）；按任务要求，**各线本轮新成果一律未读**，仅核对了分支名与 PR 编号。PR #100、#101 内容已并入 main（`9c0337a`、`3f79d2a`），属历史设计，全读。

## 1. 本人全文精读（Read 逐字读完）

**入口与制度**：根 `AGENTS.md`（作者宪章 2026-11-20 版）、`CLAUDE.md`、`README.md`；`editorial/creative-charter/OPERATING-RULES.md`（含常驻快速卡）、`VOICE-SAMPLES.md`。

**第八部全部历史设计**：
- `2026-11-24-open-epic/`：`README.md`、`01-author-direction.md`、`02-research.md`、`03-architectures.md`（八架构 A–H）、`04-story-arcs.md`（O01–O40 模块）、`05-recommended-design.md`、`06-scene-studies.md`、`07-claude-task.md`、`CLAUDE.md`（PR #100 内容）。
- `integration-v2/`：`README.md` 与 `01`–`09` 全部九个专题文件（PR #101 内容，即 GPT-6.2 的 V2《万世之我·时域纪元》）。
- `2026-11-20-gpt6-r2-proposal.md`（R2）、`2026-11-20-r3-integrated-design.md`（R3）、`2026-11-20-claude-independent-research-supplement.md`（C01–C40 索引与对照）。
- `claude-2026-11-20/original-research.md`（上轮 Claude 全文 40 条）。
- **PR #93**（`claude-independent-exploration`，经只读检出）：`01-reading-ledger.md`、`02-the-novel-as-written.md`、`05-overall-design.md`（《一个一个来》）、`07-open-questions-and-author-choices.md`、`trial-writing/00-试写复审.md` 及七场试写全文（01 祁然、02 乌鲁木齐的雪、03 房东、04 年夜饭、05 礼堂、06 回礼、07 佑霖）。

**正文（正式正典 135 章）**：
- `manuscript/volume-01/001.md`《左边的位置》全文（正典第一章）。
- `manuscript/volume-07/020.md`《不是公司的员工》全文（第七部收束章，第八部接缝点）。

**事实仓（只读）**：
- `高中/素材/文学化推演/刘佑林与赵问竹的平行宇宙故事线-2026-08-15.md` 全文——四条主宇宙与八条扩展宇宙，作者四个梦的原始整理，含阅读边界声明与 MLA 引用。
- `写作体系/创作总纲-百万字散文式自传小说.md` 全文。
- `写作体系/写作体系索引.md` 全文。
- `高中/G2204/人物/同学/赵问竹.md` 前 120 行（确认层、关系事实、班级时间线、高一回忆与关系边界各节；末尾 74 行为延伸关联，未读完）。

**截图附件**：抽样核读了 2 张（`063545.png`：GPT-6.2《万世之我：时域纪元》八架构总图；`065507.png`：作者关于四模型独立分支的追加指令）。其余 16 张按任务书已完整转录的作者原文处理，未逐张读取；如个别截图含未转录内容，本方案未采用，责任在我。

## 2. 联网检索证据（本方案实际引用）

- 不定因果序实验前沿：北京大学物理学院光量子芯片广义 ICO 验证（2025-10）；arXiv:2508.04643（器件无关因果不等式违反 24σ）；arXiv:2506.16949；arXiv:2506.20516。
- 后选闭合类时曲线：Lloyd 等 P-CTC 理论与光子实验（arXiv:1005.2219）；模拟 CTC 的计量学增益研究。
- 时间晶体 2025：稀有气体核自旋连续时间晶体（相干超数小时）；北大"时间回旋晶体"（Nat. Phys. 2025-10）；Rydberg 多重时间晶体。
- 网文产业与榜单：社科院《2025中国网络文学发展研究报告》（用户 5.26 亿、阅读市场 502.1 亿、IP 市场 3676.1 亿）；光明报系 2025 年度十部影响力作品；中国网络文学双年榜 2024–2025；起点 2025 月票年榜；阅文/番茄作家学院的黄金三章与信息差方法论；阅文 2025 财报与番茄月活对比。
- 平台政策：Anthropic Usage Policy 与 Claude 系统提示（Opus 4.6、Sonnet 4.5 官方文档页）；OpenAI Usage Policies（2025-10-29 生效版）与成年虚构内容相关社区/官方动态；xAI 文档（自定义审核控制、AUP）与 Grok 系统提示仓库。

具体条目、链接与 MLA 著录见 `13-references.md`。

## 3. 未亲读与替代依据（如实申报）

- **前七部其余 133 章**：未逐字读。全书判断依赖三重替代依据——(a) PR #93 `02-the-novel-as-written.md` 对七部的整体分析；(b) `00-试写复审.md` 从七部归纳的病与长处；(c) `VOICE-SAMPLES.md` 五段官方声音样本与八部设计资料中对各部的引用核对。此替代有已知风险：PR #93 自身也声明其子代理笔记存在误读（如"1985 年"事件错位），我未独立复核，凡涉具体章节细节处，本方案只做"接缝级"使用（第七部末章系亲读）。
- `editorial/volume08/claude-2026-11-20/process-screenshots-transcript.md`：未读全文（上轮过程截图转录，非设计本体）。
- PR #93 之 `03-open-exploration.md`、`06-relation-to-prior-designs.md`：未读（15 个模块中读 9 个）。其中 `03` 含十五个原创故事，我未采，如与我的情节库偶有相似，属独立撞车，整合时由 GPT-6.2 裁决先后。
- `editorial/creative-charter/` 其余文件（`2026-11-20-policy-crosswalk.md`、`pilots/`、`PROSE-REPAIR-EXAMPLES.md`、`templates/`）：未读原文，仅经 `OPERATING-RULES.md` 与 integration-v2 `06-policy-audit.md` 的转述了解。
- `editorial/author-decisions/`、`editorial/six-volume-integration/`、`editorial/longform-architecture/`、`outline/` 各卷、`research/grok-onboarding/`（93 文件）、历史 round4x 审稿、`work/`、`state/`、`tools/`、`给ChatGPT.md`：只看目录与个别标题，未读。
- 事实仓 700 余文件中绝大多数未读，包括全部 `隐私/` 目录（**有意不读、不转述**）；人物页仅读赵问竹页（大部）；G2204 人物库、高中回忆全文、父系祖母页、大学人物库、`百万长文写作/` 目录：未读，凡涉其中事实，本方案仅引用 PR #93 阅读账与四个梦原始文件中已核对的部分（出生与名字、称呼史、奶奶、父母、赵问竹事实层、大学与室友、西安行）。
- 高一 G2204 规则要求的 `G2204班人物库.md` 与 `自传叙事规则.md`：未逐字读；其约束经由项目规则与本轮所读文件间接受其影响。凡我方案中触及 G2204 人物处，均沿用"事实层优先、正文可推断替想、人物页不回写"的现行口径，未新增任何人物事实。

## 4. 本轮没有做的事

- 没有读取任何其他模型本轮的独立设计（含本地已存在的 qwen4 工作区文件——我未打开其中任何设计文档，仅注意到其分支存在与身份改名的提交信息）。
- 没有修改前七部、第九部、事实仓、他线分支或 main 上任何文件。
- 没有真人朗读测试与盲评；四场试写只经我自己复读，字数为脚本口径估算，正式采用前应按现行制度以 `verify` 脚本复核。
- 物理公式与实验细节为合理设定的成分，凡属公设均已逐条标注；正式稿若采用，仍需按 `02`、`03` 文件的核对清单过一遍可证伪性表述。
