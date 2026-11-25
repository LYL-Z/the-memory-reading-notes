# 《时间的复数人称》

> **七部统一融合正文｜135章｜2026-11-21。** 这是一部依据真实生活、人物回忆与独立文学重构创作的非线性自传体长篇小说。整合的是**工作主线正文**，不意味着出版许可、文学定稿、世界级水准认证或已完成真正陌生读者盲读。此前“六部115章”的README与项目状态已移入历史档案，**不再是当前项目状态**。

## 现行七部：135章，854,867官方汉字（最终收口V1.3）

| 卷 | 书名 | 章节 | 原稿汉字 | 正典汉字 | 净增 |
|---|---|---:|---:|---:|---:|
| Ⅰ | [现在有人回头](manuscript/volume-01/) | 18 | 138,952 | 140,363 | +1,411 |
| Ⅱ | [名单上的人](manuscript/volume-02/) | 24 | 172,099 | 183,706 | +11,607 |
| Ⅲ | [家里的另一种时间](manuscript/volume-03/) | 16 | 140,227 | 158,374 | +18,147 |
| Ⅳ | [叫我名字的人](manuscript/volume-04/) | 18 | 74,236 | 81,560 | +7,324 |
| Ⅴ | [换座之后](manuscript/volume-05/) | 19 | 80,985 | 81,293 | +308 |
| Ⅵ | [未写完的纸](manuscript/volume-06/) | 20 | 126,300 | 114,670 | −11,630 |
| Ⅶ | [远方不是结尾](manuscript/volume-07/) | 20 | 93,102 | 94,901 | +1,799 |
| **总计** | | **135** | **825,901** | **854,867** | **+28,966** |

现行数字按 `scripts/hanzi_count.py` 口径（标题/frontmatter/代码块/注释不计入）列出。**V1.3 最终收口只改动一章**：第五部018《第四把钥匙》恢复 PR #92 融合版（+1,444字）。V1.2 对第六部017—020 的结构性重写**予以保留**——那四章的融合版有 80–83% 的句子是首尾相接的顶针链，同一个考前一天、同一顿饭、同一夜睡眠被复述三到五遍，并给陈思懿、宋俊豪、父母、夏思成塞入大量非人语言的生成长引语；删掉的是机械循环，不是生活。

《第四把钥匙》是唯一的反向裁定：V1.2 把机关抽空后，全章近半变成作者对「我如何讲述」的自我分析，失去了四个人共同经历的一场有紧张、有行动、有各自性格的游戏。融合版有完整的可玩过程（第五把钥匙的用途混淆、「原处」的语义反转、跑回第一间听录音、手心写下的词被汗洇模糊、最后没通关），并在结尾用**放大照片找不到那几把钥匙**这一具体动作拆除不可靠记忆，而不是靠声明。据此恢复。

历史 PR #92 的 867,377 字、V1.1 的 866,731 字、V1.2 的 853,423 字均保留在冻结版本中。文学质量以正文比较判断，不得用删减比例冒充文学评分。

**唯一现行正典是 `manuscript/`。** `editorial/seven-volume-integration/fused/` 是**PR #92冻结的历史融合交付快照**，V1.1以来对第五部010、第七部010及第六部017—020进行了定点文学改写；第五部018在V1.3已恢复为与该快照一致。该快照整体不再与当前正典逐字节相同，仅供追溯，**不是并列的第二个正式版本**。V6-018A《草稿纸》、V7-001A《如果多一张车票》保持在 135 章之外，不纳入正式目录。`manuscript/volume-09/` 属第九部非虚构稿，**不计入七部135章正典与字数**。

**精确到单章的现行来源与哈希**：[V1.3最终正典表](editorial/literary-finalization/2026-11-21-v1.3-chapter-canon.tsv)（[V1.2](editorial/literary-finalization/2026-11-21-v1.2-chapter-canon.tsv)、[V1.1历史正典表](editorial/literary-finalization/2026-11-21-v1.1-chapter-canon.tsv)与[PR #92历史正典表](editorial/seven-volume-integration/2026-11-21-chapter-canon.tsv)均冻结保留）（135行，含 git blob SHA1／SHA256／官方汉字数）· [最终收口报告](editorial/literary-finalization/FINAL-CLOSURE-REPORT.md) · [逐章取舍台账](editorial/seven-volume-integration/135-chapter-selection-ledger.tsv) · [接收回执](editorial/seven-volume-integration/INTEGRATION-RECEIPT.md)。可在检出的仓库根目录执行：

```bash
python scripts/verify_seven_volume_integrated.py
```

核验逻辑检查 **135章、七卷统计、逐章 Git blob SHA1 与 SHA256、官方汉字数、章节序号与章题格式、冲突标记与乱码、候选稿元信息混入**，并对作者裁定的硬事实作定点断言（符雄辉为女性、刘逸凡≠刘弈帆、赵问竹线五处保护句、V4-007 七字、V3-013 无幽灵对白、新加坡二十七人）。V1.2的正式CI结果在新PR中独立核验；V1.1的PR #97及历史PR #92均完成过 **1108项检查、0失败**，不能把先前的PASS用作本轮结果，不得把那次结果冒充本轮的独立测试。不对文学效果作机械评分。

旧六卷验证器 `scripts/verify_six_volume_integrated.py` 与其 2026-11-14 基线**原样保留为历史验收证据**，未改数字迁就新正典；对应工作流已退为手动回放，不再是当前闸门。对当前正文运行它会失败，这是预期行为。

### 三稿如何融合进主线？

- **输入**：原稿 main `607008a`（第一至六部）与 [PR #84](https://github.com/LYL-Z/the-memory-reading-notes/pull/84) `73e8220`（第七部20章）；HY4 文学修订 [PR #86](https://github.com/LYL-Z/the-memory-reading-notes/pull/86) `e1b5d2e`；Qwen 文学修订 [PR #87](https://github.com/LYL-Z/the-memory-reading-notes/pull/87) `e73f77e`。三条线共 135×3 份候选，零缺失。
- **裁决**：逐章比较后取底本，分布为 **原稿 124 章／原稿＋Qwen 8 章／HY4 2 章／PR92 1 章**。三稿融合成功**不等于三份稿都要在正文留痕**——某一章原稿最好，保留原稿就是正确的文学裁决。HY4 在第四、五部的 60–72% 扩写经复核判为动作堆积，基本驳回；Qwen 的 R2 扩充整段舍弃，仅经事实核对的问卷／名录片段压缩并入。
- **不混合叠字**；同一章节只有一个当前读者正文。PR #84／#86／#87 的历史版本全部保留，**不直接合并 #86 或 #87**，只合并完成验收的统一整合 PR [#92](https://github.com/LYL-Z/the-memory-reading-notes/pull/92)。
- 逐章底本、不可替代段落、采纳与舍弃理由见 [七卷决策台账](editorial/seven-volume-integration/logs/) 与 [施工规范](editorial/seven-volume-integration/FUSION-SPEC-2026-11-21.md)。

### 本轮独立核验修复的缺陷

前任总编辑自评 PASS，MainAgent 独立核验实际发现并修复 **两处事实错误、一处内容丢失**：

1. **符雄辉性别**：前任写“性别‘他’保留”，与作者裁定冲突。**符雄辉是女性**，已定点订正 6 处男性代词（V2-018、V4-003×3、V4-004、V4-017），同段指向他人的代词逐一保住，未做机械替换。
2. **刘逸凡被误改为刘弈帆**：前任把 V6-012／013 共 24 处「刘逸凡」替换为「刘弈帆」，理由不实。二人是不同人物——**刘逸凡是数学课代表，刘弈帆是物理课代表**。**已全部回退**，V6-013 顶针保护段逐字复原。
3. **V2-018 取蛋糕收束丢失**：该章对宋俊豪独立生活的大幅扩厚属真增益，予以保留，仅补回原稿取蛋糕那场的收束与“问GPT”细节。

修复后全书 41 个关键人名 × 135 章的原稿↔正典计数审计**零异常**。

## 先读哪些设计与标准

1. [当前文学编辑结论与缺陷](editorial/six-volume-integration/2026-11-14-editorial-verdict.md)；[非线性三钟与读者知情](editorial/six-volume-integration/2026-11-14-three-clocks-and-canon.md)。
2. [作者最新文学重构授权](editorial/author-decisions/2026-11-13-reconstruction-and-literary-authority.md)：普通对话、空间、动作和不同日子的复合可以艺术重构；已确认事实和真实人物重大私密事件不可因此被推翻。
3. [六部当前发表与隐私风险](editorial/six-volume-integration/2026-11-14-publication-gates.md)；[作者新裁定与仍未解决的分歧](editorial/six-volume-integration/2026-11-14-author-rulings.md)。
4. [Grok Phase0 阅读档案](research/grok-onboarding/)（**历史76章基线**，并非115章的最新阅读证明）；[五部独立对抗审稿](editorial/five-volume-r3-independent-20261114/)；[第五部历史审稿](editorial/volume05/)；[第六部历史审稿](editorial/volume06/)。
5. [最新机器进度](state/progress.json)、[后续任务](state/next_actions.md)及[本轮七卷正典表](editorial/seven-volume-integration/2026-11-21-chapter-canon.tsv)。上一轮六部整合的编辑结论与发表闸门仍作历史参考保留。

## 艺术判断

核心不是给六卷铺同样的“事情发生—我后来明白”结构，而是让同一人处在**自己当时的经验、不同他人的记忆、回望者的选择性叙述、读者后得到的信息**之间，显现不一致但可信的多个面向。

可以借鉴诺兰的读者信息调度、石黑一雄和普鲁斯特记忆联想的时间组织、其他作家的情感节制与关系发展；不能强制每章倒叙，也不应复制当代个人创作者可辨认的标志性口吻。Michael 大麦哥的旧研究只当作一般叙事技法的参考，不是影音史料核验通过证书。小说不是论文：**不频繁插入“问卷里写道”、精确日历及证据条款**；但后台必须能分辨已确认事实、回忆、文学重构和假设世界。

本项目尚有跨卷模板句与人物声口趋同风险，第四、第五部相对较薄，第六部仍有重复性加厚段落；真实第三方的署名、私密问卷及家庭过目权尚需逐项处理。**真人陌生读者完整独立冷读：0**。这些状态不能被“已经更新main”覆盖。

## 双仓边界及归档

事实源为 [the-memory](https://github.com/LYL-Z/the-memory)，`master@ef33c98d63b88283e840f5414db154eb9118c4e4`，**永久只读**；创作仓本身负责正文、叙事设计和版本账。两仓均很大，列出所有文件不等于全部全文读完；当次读取范围必须附阅读凭据。

旧README全文保存在 [六部历史README](editorial/archive/README-pre-integration-20261114.md) 与 [七部融合前README](editorial/archive/README-pre-seven-volume-20261121.md)，旧项目状态保存在 [六部历史状态](state/archive/progress-pre-integration-20261114.json)、[七部融合前状态](state/archive/progress-pre-seven-volume-20261121.json)，不可再作为现稿依据。第七部20章原候审稿见 [PR #84](https://github.com/LYL-Z/the-memory-reading-notes/pull/84)，**本轮已并入正典**。第八部仍为独立反事实设计，不计入正文统计。


## 第八部｜当前正式设计 V3.1

[第八部《复数》V3.1正式设计](editorial/volume08/2026-11-25-integrated-v3/v3.1/README.md) · [Claude主创入口](editorial/volume08/2026-11-25-integrated-v3/v3.1/10-claude-brief.md) · [二次审查](editorial/volume08/2026-11-25-integrated-v3/v3.1/00-review.md) · [CTH数学与模拟](editorial/volume08/2026-11-25-integrated-v3/v3.1/02-cth.md)。作者授权PR #110深化并合入main；该设计不是正文冻结。A—H全部采用，无章数、篇幅、世界及小节上限；从硬科幻连续开篇起写，八类人生可独立展开；四梦允许圆满，成年原创爱情、科技财富、现代全球帝国、古代皇家、家庭和文明救世都可充分发展。历史V2、V3和独立PR保留为来源，不是平行执行入口。事实、权利及适用平台边界不变。正文由作者启动Claude后独立分支提交。

## 2026-11-20｜创作规则与第八部（历史演变）

**所有协作AI必须先读 [AGENTS.md](AGENTS.md)** 的文学作者宪章，再按当轮授权工作。作者允许大胆、完整地文学重构普通生活，不应因过度审慎将小说写成事实摘要、人物训诫或空洞的情绪解释；成熟主题、爽感、矛盾与圆满均可有独立文学价值。事实/反事实仍严格分层。

- [第八部 R3 三方案整合](editorial/volume08/2026-11-20-r3-integrated-design.md)：吸收作者转交Grok两方案及GPT-6上轮设计。
- [第八部 GPT-6 上轮方案归档](editorial/volume08/2026-11-20-gpt6-r2-proposal.md)：四核心世界、二十个候选、远未来、多世界结局、开篇试写。
- [Claude独立研究与40条创意补充](editorial/volume08/2026-11-20-claude-independent-research-supplement.md)：原文逐字归档、影视文学机制、40条构思与R2/R3对照，后续架构/试写全文待补。
- **2026-11-24作者新方向：[第八部开放史诗设计工作室](editorial/volume08/2026-11-24-open-epic/README.md)**：八套架构、40个情节模块、文学/网文研究、原创试写与[Claude执行入口](editorial/volume08/2026-11-24-open-epic/07-claude-task.md)。不再设章数、字数上限；R2/R3旧容量仅历史参考。爱情、事业、家庭、架空皇家、古今与文明未来均可扩展，真名非性化使用与成熟题材沿用权益边界。卷名及架构仍待作者选择。PR #93独立候选保留；不覆盖I—VII、IX正文，不回写事实源仓。

### 2026-11-24第二次作者裁定｜八系统全部采用

[开放史诗V2：万世之我·时域纪元](editorial/volume08/2026-11-24-open-epic/integration-v2/README.md)（暂名）：[数学物理开篇](editorial/volume08/2026-11-24-open-epic/integration-v2/01-physics-and-opening.md)、[三类皇家世界](editorial/volume08/2026-11-24-open-epic/integration-v2/02-worlds-and-empire.md)、[爽感与社会人性](editorial/volume08/2026-11-24-open-epic/integration-v2/03-literary-craft.md)、[原创人物](editorial/volume08/2026-11-24-open-epic/integration-v2/04-characters.md)、[三家官方文档及协作](editorial/volume08/2026-11-24-open-epic/integration-v2/05-model-workflow.md)、[制度审查](editorial/volume08/2026-11-24-open-epic/integration-v2/06-policy-audit.md)、[Claude任务](editorial/volume08/2026-11-24-open-epic/integration-v2/08-claude-task.md)。A–H全部采用，不强制每章联动；章节可分任意小节。历史文档保持原貌，旧艺术限额不适用第八部。

## 第九部｜作者的思考（2026-11-21正式立项）

作者在2026-11-21决定新增第九部**《作者的思考》**：收录独立科技、商业及社会观察，不再受前七部小说情节顺序限制。首章为作者于Anthropic上市前写成的原稿，全文入库，另设核查记录和上市后补记候选，不因2026-11-19已上市而覆盖历史原文。

- [第九部入口](manuscript/volume-09/README.md) · [001《Anthropic：安全、资本与万亿估值的危险游戏》](manuscript/volume-09/001-Anthropic-安全资本与万亿估值的危险游戏.md)
- [原文保存](editorial/volume09/2026-11-21-ch01-author-verbatim.md) · [事实核查](editorial/volume09/2026-11-21-ch01-fact-check.md) · [已采纳的上市后附录](manuscript/volume-09/001-Anthropic-安全资本与万亿估值的危险游戏.md#附录上市以后问题还在) · [附录采纳记录](editorial/volume09/2026-11-21-ch01-appendix-acceptance.md)
- 第一至七部当前135章、854,867字的V1.3正典**不变**（867,377为历史PR #92快照）；第八部为V3.1正式设计，正文尚未启动。第九部目前一章，作者原稿中的现实主张不等同于已核实的出版稿。

## 创作入口｜作者宪章与后台制度分离（2026-11-20）

| 何时 | 文件 |
|---|---|
| 常驻：作者身份、声音、野心 | [AGENTS.md 作者宪章](AGENTS.md)（约1455汉字，不堆工程条款） |
| 常驻精简；详细规则按需 | [后台制度](editorial/creative-charter/OPERATING-RULES.md) 的快速卡 |
| 写作时读2–3例 | [声音样本](editorial/creative-charter/VOICE-SAMPLES.md)（五处现行正文逐字节选，作者偏好待确认） |
| 按章提取 | [材料卡](editorial/creative-charter/templates/material-card.md)、[人物卡](editorial/creative-charter/templates/character-card.md) |
| 每章施工 | [章节任务书](editorial/creative-charter/templates/chapter-brief.md)（三案按需，顺畅的故事直接成文） |
| 审稿时 | [病灶对照](editorial/creative-charter/PROSE-REPAIR-EXAMPLES.md)、[交付清单](editorial/pre-delivery-literary-checklist.md) |
| 方法校准 | [第八部施工示例与盲评方案](editorial/creative-charter/pilots/2026-11-20-scene-pilot.md) |

[跨仓冲突清单](editorial/creative-charter/2026-11-20-policy-crosswalk.md)继续登记旧制度的历史适用范围。新的作者宪章与后台制度取代旧根规则的组织形式，不改变历史事实、成熟题材范围、第三人权益与版本保护。Claude Code见[CLAUDE.md](CLAUDE.md)；Cursor技能与本入口同步。