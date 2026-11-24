# 阅读、同步与研究账本

## 1. 基线与工具事实

本轮实际读取的远端基线为：

- `LYL-Z/the-memory-reading-notes`：`main@3f79d2a5f46d30da880f458cff81330d8fd24ce1`，提交时间为 2026-11-24；PR #100、#101 已合并。
- `LYL-Z/the-memory`：`master@ef33c98e438d4b2a9033654945cfed0914635189`。本地 `.git/HEAD` 指向同一提交。
- Claude 历史探索：PR #93，读取其明确指定的 head `ee3bf7dadd11f991e4a8879b1c41ee69b1228c88`；该 PR 在本轮开始时仍为历史 Draft。

本机 GitHub CLI 已登录并可读取两仓。命令行 `git` 不在当前环境中，故使用 GitHub API 与 codeload 获取 main 和 PR93 完整快照，再逐篇读取本地文件。此步骤只代表取得指定提交的完整快照，不冒充本地 Git 同步或推送。

未读取 Claude、Grok 或任何其他模型在本轮新建立的 independent-masterplan 成果。PR #93 与 GPT V1/V2 是作者明确指定的历史资料。

## 2. 根文件与现行制度：全文实读

在创作仓当前 main 上逐篇读取：

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `给ChatGPT.md`
- `editorial/creative-charter/OPERATING-RULES.md`
- `editorial/creative-charter/VOICE-SAMPLES.md`
- `editorial/creative-charter/2026-11-20-literary-freedom-and-mature-themes.md`

在事实源仓逐篇读取：

- 外层 `AGENTS.md`
- `写作体系/写作体系索引.md`
- `写作体系/创作总纲-百万字散文式自传小说.md`
- `写作体系/技法库/叙事结构与语言工具.md`
- `写作体系/风格参考/作家作品参考谱系.md`
- `项目管理/用户订正-2026-09-11-事实优先与有界推演.md`
- `项目管理/用户订正-2026-09-12-第一人称可推断可替想.md`
- `家庭/家庭敏感资料处理规则.md`

制度审计并未声称逐个通读两仓所有 Markdown。交付中的制度意见只针对以上实读文件、指定第八部资料及所读正文，不把“全仓扫描”写成“全仓阅读”。

## 3. 第八部指定资料：全文实读

### 当前 main 的 `editorial/volume08/` 现存文件

完整逐篇读取：

- `2026-11-20-claude-independent-research-supplement.md`
- `2026-11-20-gpt6-r2-proposal.md`
- `2026-11-20-r3-integrated-design.md`
- `claude-2026-11-20/original-research.md`
- `2026-11-24-open-epic/README.md`
- `2026-11-24-open-epic/01-author-direction.md`
- `2026-11-24-open-epic/02-research.md`
- `2026-11-24-open-epic/03-architectures.md`
- `2026-11-24-open-epic/04-story-arcs.md`
- `2026-11-24-open-epic/05-recommended-design.md`
- `2026-11-24-open-epic/06-scene-studies.md`
- `2026-11-24-open-epic/integration-v2/README.md`
- `integration-v2/01-physics-and-opening.md`
- `integration-v2/02-worlds-and-empire.md`
- `integration-v2/03-literary-craft.md`
- `integration-v2/04-characters.md`
- `integration-v2/05-model-workflow.md`
- `integration-v2/06-policy-audit.md`
- `integration-v2/07-sources.md`
- `integration-v2/08-claude-task.md`
- `integration-v2/08-gpt6-v1-evaluation.md`
- `integration-v2/09-opening-study.md`

说明：README 中提及的 R1 目录和两份过程截图转录不在上述 main 快照中，未把它们计入已读。历史文件的引用关系与当前快照存在不完全一致，应以后续仓内核验为准。

### PR #93 的 Claude 历史独立探索

完整逐篇读取：

- `README.md`
- `01-reading-ledger.md`
- `02-the-novel-as-written.md`
- `03-open-exploration.md`
- `05-overall-design.md`
- `06-relation-to-prior-designs.md`
- `07-open-questions-and-author-choices.md`
- 试写复审《00-试写复审》
- 《你下午是不是拍我了》
- 《乌鲁木齐的雪》
- 《房东》
- 《年夜饭》
- 《礼堂》
- 《回礼》
- 《佑霖》

以上七场试写均直接读取正文，而非只读 PR 摘要。

## 4. 前七部正文：28 章全文实读，非七部逐字通读

当前 main 的章号与早期 PR93 使用的旧结构不同。本账本按当前 main 记录：

- 第一部：001、015、016、017、018。
- 第二部：001、018、019、020。
- 第三部：001、010、016。
- 第四部：003、009、018。
- 第五部：001、006、013、016、019。
- 第六部：012、013、020。
- 第七部：010、012、014、015、020。

这 28 章覆盖七部，包含：江安宿舍与叙事者追踪；历史课与公开表白；小红帽、竹林杯和考试后的眼睛；手机后盖的“为什么”；高二上半学期与食堂后门；紫金港笔记本与说明卡；轻绳题；生日礼物；二班轶事；西安与返回现实；图书馆数字世界；塞曼效应脚本；阻尼振动；合照与 `manifest.json`；以及“不是公司的员工”。

**未声称逐字读完前七部全部 135 章。** 本方案的连续性理解还参考了第八部设计中的具体原文摘录和下列事实源页，但这些参考不被冒充为其余章节的正文阅读证明。

## 5. 人物与情感材料：普通层全文实读

- `高中/G2204/G2204班人物库.md`
- `高中/G2204/人物/同学/赵问竹.md`
- `高中/素材/个人回忆/刘佑林关于赵问竹的高中回忆-2026-08-12.md`
- `高中/素材/同学回忆/赵问竹关于刘佑林的书面评价.md`
- `高中/素材/文学化推演/刘佑林与赵问竹的平行宇宙故事线-2026-08-15.md`
- `高中/2025届/人物/学生/董佳好.md`
- `家庭/人物/父亲.md`
- `家庭/人物/母亲.md`
- `大学/四川大学/强基班/人物/同学/曾子沣.md`
- `大学/四川大学/强基班/素材/曾子沣自述与对刘佑林的印象.md`

没有读取 `私人资料/` 中的完整聊天、精确个人字段或私密原图。本方案不使用这些材料。

## 6. 用户附件

已逐张读取本轮 18 张图片。内容是 GPT 第八部 V2 任务说明的屏幕记录，其中一张明确指定 Kimi 分支 `creative/volume08-kimi-independent-masterplan`。它们与本任务文字及 V2 文件相互印证，不被当作新增事实源。

## 7. 联网研究范围

实际检索并阅读搜索结果或官方页面摘录，主题包括：

- 《复仇者联盟4》《蚁人》《星际穿越》《信条》《回到未来》《暗黑》的时间机制与叙事规则；
- 狭义／广义相对论相关时间机制、可穿越虫洞、弱能量条件、闭合类时曲线、Deutsch 固定点、后选择模型、时间序保护；
- 量子纠缠不可超光速通信、量子隐形传态、量子参考系、不确定因果序、Page–Wootters、全息原理与多世界解释的证据边界；
- Landauer 原理、记忆与热力学时间箭头；
- 网文升级、序列、信息差、家族、多代、反套路经营、文明建设与平台榜单口径；
- 社会主义公共所有、多中心治理、公民审议、合作社与君主角色；
- Anthropic、OpenAI、xAI 的官方模型、使用政策与内容边界。

来源与证据分级见 `10-sources-mla.md`。未将搜索摘要中的排名、销量或未来模型版本当作稳定事实；未使用短链聚合页作为核心科学结论的唯一依据。

## 8. 本方案的阅读诚实声明

本轮足以形成独立设计，但不等于：

- 前七部所有正文已逐字通读；
- 两个仓库所有 Markdown 已逐字通读；
- 知识库全部人物与全部私密材料已读取；
- 所有参考文献已阅读完整专著或论文全文；
- 现实科学已经验证 MWC 或人类跨时空旅行。

下一阶段若要锁定正式连续正文，仍需补读与当批场景直接相关的未读章节，并建立逐章事实核对，而不能拿本账本替代这一步。
