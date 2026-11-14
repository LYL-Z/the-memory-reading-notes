# 《时间的复数人称》

> **已合并main｜六部统一正文入口｜2026-11-14。** 这是一部依据真实生活、人物回忆与独立文学重构创作的非线性自传体长篇小说。整合的是**工作主线正文**，不意味着出版许可、文学定稿、世界级水准认证或已完成真正陌生读者盲读。此前“四部76章”的README、旧R50/R7阶段说明已移入历史档案，**不再是当前项目状态**。

**正式合并已核验**：[PR #77](https://github.com/LYL-Z/the-memory-reading-notes/pull/77) · 合并SHA `2ba6be83bbde5717b4ef516927a92c090b4df6ce` · [主支GitHub Actions机械验收通过](https://github.com/LYL-Z/the-memory-reading-notes/actions/runs/43616624507)。这仅证明所选版本与字数、来源和目录可重现，不等于文学/传播权利审查通过。

## 现行六部：115章，732,799官方汉字

| 卷 | 书名 | 章节 | `scripts/hanzi_count.py` 同口径汉字 |
|---|---|---:|---:|
| Ⅰ | [现在有人回头](manuscript/volume-01/) | 18 | 138,952 |
| Ⅱ | [名单上的人](manuscript/volume-02/) | 24 | 172,099 |
| Ⅲ | [家里的另一种时间](manuscript/volume-03/) | 16 | 140,227 |
| Ⅳ | [叫我名字的人](manuscript/volume-04/) | 18 | 74,236 |
| Ⅴ | [换座之后](manuscript/volume-05/) | 19 | 80,985 |
| Ⅵ | [未写完的纸](manuscript/volume-06/) | 20 | 126,300 |
| **总计** | | **115** | **732,799** |

**精确到单章的来源与哈希**：[章级选稿总账](editorial/six-volume-integration/2026-11-14-chapter-canon.tsv) · [逐章计数](editorial/six-volume-integration/2026-11-14-verified-counts.md)。可在检出的仓库根目录执行：

```bash
python scripts/verify_six_volume_integrated.py
```

核验逻辑会检查 **115章、六卷统计、所选候选Git blob SHA、章节序号、冲突标记**，不对文学效果作机械评分。

### 各AI候选稿如何选进主线？

- **第一至五部**：采用相互承接的 PR [#73](https://github.com/LYL-Z/the-memory-reading-notes/pull/73) → [#74](https://github.com/LYL-Z/the-memory-reading-notes/pull/74) → [#75](https://github.com/LYL-Z/the-memory-reading-notes/pull/75) → [#76](https://github.com/LYL-Z/the-memory-reading-notes/pull/76) 的最终HEAD。第一至四部素材和文字由 Grok Phase1/#67 为本轮候选基础，第五部由#63及GPT-6 #68叠入，之后依据#71独立对抗审稿进行了回退、去同质化及作者事实订正。
- **第六部**：以 Grok [#69](https://github.com/LYL-Z/the-memory-reading-notes/pull/69) 的R4完整20章为底，章节 **010/016/020** 改用 GPT-6 [#72](https://github.com/LYL-Z/the-memory-reading-notes/pull/72) R5.2已过原章篇幅下限的文学修订。其余5章的R5删重试版因为低于作者篇幅闸门，并**未**覆盖R4。文学缺陷继续列为待改进项。
- 历史稿**不混合叠字**；同一章节保留一个当前读者正文，另一个有价值的实验留在原Draft/历史账。完整 **PR #1—#76取舍总账**：[列表](editorial/six-volume-integration/2026-11-14-branch-disposition.tsv) · [说明](editorial/six-volume-integration/2026-11-14-branch-disposition.md)。

**必须订正**：PR#76 报告把前五部写成606,031，但本次以确切HEAD取回95章逐篇重计为**606,499**（差+468）。统一新账使用实测值，不复制旧报告数字。

## 先读哪些设计与标准

1. [当前文学编辑结论与缺陷](editorial/six-volume-integration/2026-11-14-editorial-verdict.md)；[非线性三钟与读者知情](editorial/six-volume-integration/2026-11-14-three-clocks-and-canon.md)。
2. [作者最新文学重构授权](editorial/author-decisions/2026-11-13-reconstruction-and-literary-authority.md)：普通对话、空间、动作和不同日子的复合可以艺术重构；已确认事实和真实人物重大私密事件不可因此被推翻。
3. [六部当前发表与隐私风险](editorial/six-volume-integration/2026-11-14-publication-gates.md)；[作者新裁定与仍未解决的分歧](editorial/six-volume-integration/2026-11-14-author-rulings.md)。
4. [Grok Phase0 阅读档案](research/grok-onboarding/)（**历史76章基线**，并非115章的最新阅读证明）；[五部独立对抗审稿](editorial/five-volume-r3-independent-20261114/)；[第五部历史审稿](editorial/volume05/)；[第六部历史审稿](editorial/volume06/)。
5. [最新机器进度](state/progress.json)、[后续任务](state/next_actions.md)及[本轮选稿台账](editorial/six-volume-integration/2026-11-14-chapter-canon.tsv)。

## 艺术判断

核心不是给六卷铺同样的“事情发生—我后来明白”结构，而是让同一人处在**自己当时的经验、不同他人的记忆、回望者的选择性叙述、读者后得到的信息**之间，显现不一致但可信的多个面向。

可以借鉴诺兰的读者信息调度、石黑一雄和普鲁斯特记忆联想的时间组织、其他作家的情感节制与关系发展；不能强制每章倒叙，也不应复制当代个人创作者可辨认的标志性口吻。Michael 大麦哥的旧研究只当作一般叙事技法的参考，不是影音史料核验通过证书。小说不是论文：**不频繁插入“问卷里写道”、精确日历及证据条款**；但后台必须能分辨已确认事实、回忆、文学重构和假设世界。

本项目尚有跨卷模板句与人物声口趋同风险，第四、第五部相对较薄，第六部仍有重复性加厚段落；真实第三方的署名、私密问卷及家庭过目权尚需逐项处理。**真人陌生读者完整独立冷读：0**。这些状态不能被“已经更新main”覆盖。

## 双仓边界及归档

事实源为 [the-memory](https://github.com/LYL-Z/the-memory)，`master@ef33c98d63b88283e840f5414db154eb9118c4e4`，**永久只读**；创作仓本身负责正文、叙事设计和版本账。两仓均很大，列出所有文件不等于全部全文读完；当次读取范围必须附阅读凭据。

旧README全文保存在 [历史README](editorial/archive/README-pre-integration-20261114.md)，旧项目状态保存在 [历史状态](state/archive/progress-pre-integration-20261114.json)、[旧行动表](state/archive/next-actions-pre-integration-20261114.md)，不可再作为现稿依据。拟议中的七部、八部结构依然是设计候选，不因本次六部上主线而自动变成事实、正式卷名或未来创作指令。
