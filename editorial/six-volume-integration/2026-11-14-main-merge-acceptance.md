# 六部统一工作稿正式合并main验收｜2026-11-14

> 本文件验证GitHub主线结果；不宣称版权清理、真人独立试读或全球文学水准已经取得成功。

## 实际操作与回执

- 原始main：`12ac7ee9342b93a9cbf091095562b205321237b7`，四部76章507,125。
- 保留备份：`archive/main-pre-six-volume-20261114`，HEAD仍为上述原main。
- 统一候选分支：`integration/six-volume-canon-20261114`，选稿与档案经过逐章机械验收。
- 已合并PR：[77](https://github.com/LYL-Z/the-memory-reading-notes/pull/77)，`merged=true`，`state=closed`，合并时间`2026-11-14T16:37:28Z`。
- 实际main合并提交：`2ba6be83bbde5717b4ef516927a92c090b4df6ce`；合并后GitHub `/git/ref/heads/main` 读回同一个SHA。
- 合并后Git树 `manuscript/volume-01..06` 标准编号章节 **115/115**；双仓源库 `LYL-Z/the-memory/master` HEAD `ef33c98d63b88283e840f5414db154eb9118c4e4` 不变。
- Github Actions: 分支推送成功 [Run 43616513114](https://github.com/LYL-Z/the-memory-reading-notes/actions/runs/43616513114)；PR触发成功 [Run 43616587807](https://github.com/LYL-Z/the-memory-reading-notes/actions/runs/43616587807)；**合并后main成功** [Run 43616624507](https://github.com/LYL-Z/the-memory-reading-notes/actions/runs/43616624507)。

## 当前单一正文字数（官方CJK口径）

| 部 | 章节 | 字数 |
|---|---:|---:|
| Ⅰ《现在有人回头》 | 18 | 138,952 |
| Ⅱ《名单上的人》 | 24 | 172,099 |
| Ⅲ《家里的另一种时间》 | 16 | 140,227 |
| Ⅳ《叫我名字的人》 | 18 | 74,236 |
| Ⅴ《换座之后》 | 19 | 80,985 |
| Ⅵ《未写完的纸》 | 20 | 126,300 |
| **总计** | **115** | **732,799** |

见 `2026-11-14-chapter-canon.tsv` 的115条章级来源SHA（不是只报统计值）。PR#76静态报告的五部606031应修正为现场复算606499，差+468，已留差异说明。

## 本次通过的门槛

- `SELECTED_MANUSCRIPT_TREE` PASS
- `CHAPTER_COUNT_115` PASS
- `OFFICIAL_HANZI_PER_CHAPTER_AND_VOLUME` PASS
- `SOURCE_GIT_BLOB_PROVENANCE` PASS
- `GITHUB_MAIN_MERGE` PASS
- `POST_MERGE_CI` PASS
- `SOURCE_VAULT_READ_ONLY` PASS

## 未被本次技术整合假称通过的门槛

- **完整六部连续文学冷读和人类盲读**：OPEN；陌生真人0人。
- **真实人物著作/隐私/公开名称权益**：OPEN。宋俊豪化名/实名、母亲家庭段落、朱学良及其他具名角色需个别处理。含私人答复的PR#70逐字原文没有在本次main重复复制。
- **文学结构/声口**：OPEN。第六部R4五章重复情节是明示保留的工作缺陷；第4/5部密度与跨卷重复仍需进一步判读。世界级文学是追求，不是本次GitHub合并的证明。

**结论**：`MAIN_TECHNICAL_INTEGRATION_ACCEPTED`；`LITERARY_FROZEN=false`；`PUBLICATION_READY=false`。
