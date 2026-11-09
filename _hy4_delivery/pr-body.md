## HY4 独立文学终审与实际修订｜第二部 01—11 章（Draft）

这是**独立第二编辑版本**，供作者与原稿逐段对读。不合并任何已有 PR，不改 main、不改第一部 R50、不改 `LYL-Z/the-memory` 事实源库。

**基线**：PR #29 head `draft/volume02-ch11-two-places-2017-20261108`，SHA `7dba7eddc3d8af900b64d16cf51f657364c65eb6`。原版十一章逐字备份于 `_hy4_delivery/original/`。

### PR #28／#29 分叉只读诊断

- 依赖链 `main → #23 → #24 → #25 → #26 → #27 → #28 → #29`，链式草稿叠加。
- `compare(ch10...ch11)`：`status = diverged`，PR29 相对 PR28 `ahead 31 / behind 8`，`merge-base = 5167840…`。
- PR28 独有 8 个提交全部改动 `manuscript/volume-02/010.md` 及 state／ch10 报告；但两分支 `010.md` 的 blob **完全相同**（`5e6a3e7…`，4,136 汉字），`manuscript/volume-02/` 唯一差异是 PR29 新增的 `011.md`。
- **正文已镜像，提交图仍分叉**。此时合并 PR29 进 PR28 会重新引入 8 个重复提交并与 `state/progress.json`、`state/next_actions.md` 冲突。**不以"文件相同"假称祖先同步，不以 `mergeable` 代替完整审查**。本 PR 不合并、不 rebase 上游、不强推。

### 交付内容

1. `editorial/volume02/reviews/hy4-stage1-first-read-judgments.md` — 未受既有文学评价影响的第一次连续阅读判断（每章八项）。
2. `editorial/volume02/reviews/hy4-independent-ch01-ch11-review.md` — 十一章完整独立文学审稿：十维度逐章、P0/P1/P2、与上一位编辑的七项分歧及原文证据、人物专项与第 11 章七问。
3. `editorial/volume02/reviews/hy4-sentence-ab-proposals.md` — 每章 5—6 处、共 58 处 A/B 优化对照（含 23 处明确「保留原文」）。
4. `manuscript/volume-02/001.md`—`011.md` — HY4 亲自完成的实际修订正文，47 处精确替换。
5. `editorial/volume02/reviews/hy4-revision-diff-and-whole-read.md` — 逐章修改说明、完整 diff 索引、字数增减、十一章整体复读报告。
6. `editorial/volume02/reviews/hy4-facts-and-privacy-audit.md` — 事实来源与隐私边界核查、P0 清单、两仓口径差异、待裁决缺口。
7. `editorial/volume02/reviews/hy4-final-report-to-author.md` — 致作者七部分中文报告。
8. `_hy4_delivery/06-full-diff.patch`、`apply_hy4_revisions*.py` — 可复现补丁与脚本。

### 主要 P0（全部已修）

- 002/003×2/005 四处「十六岁」→「十五岁」（2007-11-05 生，2023 年 8 月实足 15 周岁；006 的 2023-11-11 十六岁生日正确，保留）。既有 ch10 报告第 50 行**早已知悉此错却标注"未越界处理"**。
- 010 家长大会日期表述：原件为 2023-08-19 会议材料，08-29 是其中考试表第二日。
- 011 开场「向睿馨！！！／对不起对不起」改用 moment-94 有原件的公开评论「我要给你打差评，我的名字」，删无原件逐字道歉。
- 011 两处「鬼片在她家」：问卷 Q21/Q23 均答「你家」，与任务书「向家」冲突；不擅自选边，正文改为不钉死地点并列入待裁决。
- 011「她说过……一个人能想起的并不多」：原句全库未找到、近似句属 `publish:false` 层，去掉伪称。
- 006 结拜口径统一为 2017 夏／刘佑林家／夏母提议；饭店保留为另一版记忆，未虚构第二场。

### 字数与待决策

**61,859 → 60,945 汉字，净 −914**（逐章差额之和与总差一致）。按仓库历史增字偏好，此净减**未获作者单独批准**，不包装为质量提高，不回填同义废话；原版可逐句拣选或整卷恢复。

其他待裁决：鬼片地点、错字评论是否另有截图、夏恺宪与赵问竹的独立证词、向睿馨问卷童年细节的公开发表授权、2023 放榜日期与武汉逐站同行。

### 并发基线漂移与冻结处理（如实补录）

工作期间另一会话向 PR #29 分支推送 7 个提交，`011.md` 由 3,750 字改为 3,200 字，并更新任务书与 state；本 PR 初建时因此 `mergeable_state: dirty`（`011.md` 冲突）。**未重写上游、未 rebase、未合并**：新建冻结快照分支 `hy4/baseline-snapshot-20261109-7dba7ed`（指向我开始工作时的 PR29 head `7dba7ed`），把本 PR 的 base 改为该快照，现为 `mergeable: true / clean`，仍是 Draft。原版备份、413 行 diff、字数统计与十一章修订全部相对同一基线，可逐段比较。详见 `hy4-concurrent-baseline-drift-note.md`。

复核并发新版 `011.md` 后确认：**本轮判定的 P0 全部仍在**（「向睿馨！！！／对不起对不起」、三处「在她家看鬼片」、「她说过……一个人能想起的并不多」）。并发精修压缩了篇幅，但没有修事实与隐私边界。若以新版 011 为基线，需要一次新的独立审稿轮次。

### 验收状态（如实）

已运行：三段修订脚本（逐条校验命中）、汉字统计、完整 diff 生成、残留词 grep、十一章按原序整体复读（发现并修复 5 处接缝问题）、第一部 R50 零改动核对。
**未运行／仍为 0**：`scripts/hanzi_count.py`、仓库 CI、真人独立冷读。不标 `FULL_PASS`，不称出版级或文学评级。
