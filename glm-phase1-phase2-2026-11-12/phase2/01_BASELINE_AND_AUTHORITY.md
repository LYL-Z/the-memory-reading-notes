# GLM 位｜01 基线、权威与授权（第 2 阶段）

## 一、实时核验（开工与收尾各一次）

| 项 | 值 | 取得方式 |
|---|---|---|
| 创作仓 `main` | `bad5b23483fd21c8f65423ff3747c095e06c0759` | `git -C _work/reading-notes rev-parse origin/main` |
| PR #51 head | `017ef32da134c0292906e0d4ebcb843e7f50a627` | worktree `_work/pr51` |
| PR #52 head | `6b6d90c582c06edfaaf4941d7c5824ee9086fd3c` | worktree `_work/pr52` |
| **PR #53 head（唯一主候审版本）** | `2307305837932f6196ce300fc67f26ed8db3ac11`（2026-11-12 01:51:41 -0800） | worktree `_work/pr53` `git rev-parse HEAD` |
| PR #53 树文件 / 正文 | 443 / 42 章 | `git ls-tree -r -l` |
| 事实库 master | `ef33c98d63b88283e840f5414db154eb9118c4e4`，工作区 clean | `git -C D:\The Memory\The Memory` |
| 事实库文件 / Markdown / 私密层 | 2,297 / 892 / 47 | `os.walk`（私密层零正文读取） |
| 官方汉字 | V1 136,693 / V2 135,374 | `scripts/hanzi_count.py` 实跑 |
| 本地工作副本 | `_work/reading-notes` + 4 个 detached worktree（`main/pr51/pr52/pr53`） | `git worktree list` |

PR 链为 **#51 → #52 → #53 层层继承**，不是三个互不相干的全文副本；`main` 只有第二部旧版 001–005。本阶段只读 PR #53 树，**不拼接不兼容章节**。

## 二、权威阶梯（冲突时取高者）

1. **作者近期明确直接指令**与原始可核事实。
2. 现行工程规范：`AGENTS.md`（旧稿禁读、推测留 `editorial/`、字数只认 `hanzi_count.py`、只走 Draft PR）、`editorial/style-and-influences/2026-11-08-author-voice-anti-template-and-evidence-protocol.md`（三声部、行为优先、反模板、证据六栏）、`editorial/volume02/2026-11-08-b2-first-24chapter-reading-order-v2.md`（现行 24 章排序与读者知情锁）。
3. `editorial/volume02/2026-11-08-24chapter-aesthetic-revelation-and-audio-map.md`（自标 `PROPOSAL_ONLY`）：只作审美参照，**其章号列按旧序，不得覆盖 B2**。
4. `editorial/narrative_design.md`、`authority_conflicts.md`、`reading_coverage.md`：历史工程记录，供沿革理解。
5. 编辑建议／理论框架／AI 自评／废弃目录：只供比较，不能压倒作者订正。
6. 旧稿 `百万长文写作/`、`长篇创作/`、`正式成文/`、外层连载：`AGENTS.md` 明禁，**不读、不仿、不续写**，不得为现稿补造结构或意象。

**已登记的规范冲突**：B2 V2 的前四章映射为 `01 一个人的客厅 / 02 二班 / 03 后门 / 04 三餐`，明文「替代旧阅读排序」；审美施工表第 31–34 行仍按旧序写 `01 二班 / 02 三餐 / 03 后门 / 04 一个人的客厅`。按阶梯取 B2。B2 头部三段历史字数（32,956／33,428／33,577）只覆盖前五章且互相为时间先后，**不得与现行 24 章 135,374 混用**。

## 三、本阶段的授权范围与禁止项

**允许**（任务书 §0、§15）：在**仓库外的隔离目录**创建并写入修订稿、diff、测试与报告；第二部可建隔离候选；第一部可出全面诊断与隔离完整实验版。

**禁止**：改事实源库、改第一部 R50 冻结原稿、改公开既有分支与 PR、改仓库默认分支、改历史记录、改可见性；未经另行授权 push／merge／force／rebase／开公开 PR；公开完整私人材料；把实验版称 R51 或自动替换 R50；把 R50 验证脚本的 PASS 套给结构不同的新稿；把模型模拟读者说成真人试读。

**作者后续指令的覆盖**：作者在本会话明确要求「完成第 1 和第 2 两个阶段后，再全部将你所产生的所有内容公开提交」「全部公开」。该指令即为「另行授权」，但**只覆盖 GLM 位本人两阶段的产出**，不覆盖 DeepSeek 位结果，也不解除私密层／第三人隐私的最小披露义务。因此本阶段收尾后以**普通提交**推送到公开仓库的**新分支**，不 force、不 rebase、不重写历史、不合并 main、不改动既有 PR。

## 四、独立性与交叉接触

GLM 与 DeepSeek 本阶段隔离，不得读取对方本阶段结果、不互求认可、不给合并结论。已发生的元数据层接触与撤销动作，如实登记在 `AI-Review-Onboarding/GLM/GLM_PHASE1_IDENTITY_AND_HANDOFF.md` 与本目录 `00_EXECUTION_SUMMARY.md` §五；**未读取对方候选正文、逐章诊断、A/B 与 diff**，未继承其任何结论。

## 五、第 1 阶段回执的复用边界

`00`–`12`、`cards/`、`sections/`、`anchor_verification.csv` 为 GLM 位第 1 阶段自身回执，可作本阶段 G0／G1 输入。其中 `anchor_verification.csv` 的 **9 条订正账**必须并入事实门槛：V1-010、012、013、015 与 V2-001、013（两处）、023、024 的卡片引文经过加工（合并两行／省略号跳接／改标点／漏字／改前缀），**不得当逐字原文引用**。

不得把第 1 阶段的任何内容当作「已改稿／已扩容／读者已验证」的依据；真人冷读 0，R50 验证器本阶段未运行。
