# HY4 独立审稿与实改｜第二部第15—16章（叠加于 PR #41）

**性质**：独立 Draft PR，基于 **PR #41 的 head** `7d0efef6204cb1476ed589b5d63f3e1a566dd50c`（其 base 为 PR #40 分支 `0de0e00`）。不合并 main、不关闭他人 PR、不改写历史、不覆盖 ChatGPT 原稿。第一部 R50 与第二部 001—014 逐字未改，事实仓只读。

## 实时核验（实测）

| 项 | 值 |
|---|---|
| PR #40 | `OPEN/Draft/CLEAN`，head `0de0e00b0e63f7d32b465fbdff67696ede73cfb5`，base `hy4/volume02-ch15-independent-review-20261109`（`9fc6719`） |
| PR #41 | `OPEN/Draft/CLEAN`，head `7d0efef6204cb1476ed589b5d63f3e1a566dd50c`，base **PR #40 分支** |
| 父版官方字数 | 015 = 2,698；016 = 2,046；001—016 = 78,288 |
| 本版官方字数 | **015 = 2,850（+152）；016 = 3,296（+1,250）；001—016 = 79,690（+1,402）** |

## 裁决

- **第15章**：`R2 主体保留 + 四处局部精修`。承认 PR #40 的五处改动是真实净增益，一处不回滚；补删两处残留编辑语，并补两件事实仓有据、全卷未调用的王麒皓独立行动（竹林杯望风；2023-11-11 十六岁生日宴在场）。
- **第16章**：`实际重写`，不 `KEEP_R1`。删可识别的开篇与末句（依据：隐私／重新识别、第三人动机归因、本章自身结构；**不含任何旧稿后卷归属判断**），以相册动作与具体留白替代；把知识库中全卷零命中的姑母／表亲／祖母／父亲人生调度进正文，正面回答「本章是否只在借照片解释自己」。

## 交付文件

- `manuscript/volume-02/015.md`、`016.md`（完整正文）
- `editorial/volume02/reviews/hy4-ch15-ch16-stage1-cold-read.md`（先于任何本轮自评落盘，commit `f9b8fc3`）
- `editorial/volume02/reviews/hy4-ch15-ch16-final-review-and-verdict.md`（十维度严审、事实证据表、与 ChatGPT 六条分歧、015 17 组＋016 24 组 A/B、五问、体量方案）
- `_hy4_ch15_ch16_delivery/015-PR40-original.md`、`016-PR41-original.md`（父版逐字备份）
- `_hy4_ch15_ch16_delivery/015-016-full-diff.patch`（完整机器可读 diff）
- `_hy4_ch15_ch16_delivery/apply_revisions*.py`（可复现改稿脚本）
- `state/progress.json`、`state/next_actions.md`（真实 HEAD／base 记录）

## 隐私红线（已扫描）

015＋016 正文经敏感词表与第三人实名／学校／单位／账号昵称词表扫描，均零命中（词表不在公开文件复述）。2013 三者不假定同帧；2017 十義桥明写不是过年；2023 正月未声称原件核验；嫉妒／势利全部写作第一人称主观。

**P0 状态：`P0_BLOCKED_AWAIT_AUTHOR_AUTHORIZATION`** —— 正文已撤出，但 PR #41／#42 的公开历史提交、PR 累积 diff 的删除行、以及本 PR 曾附带的旧稿全文与完整 diff 附件，无法仅靠普通提交清除。本轮已删除当前树中的两份敏感附件并脱敏报告／state；详细残留清单与可恢复清理方案见 `hy4-pr42-p0-risk-register-and-remediation.md`。**不叠加第 17 章。**

## 校验

`hanzi_count.py` 79,690 ✓｜`git diff --check` PASS ✓｜`python -m json.tool state/progress.json` PASS ✓｜`verify_volume01_round50_final_chatgpt.py` 见提交记录。

**未执行**：仓库 CI、真人独立冷读、王麒皓本人试读、母亲本人试读、亲属权益审阅。工具 PASS 不代表文学质量或出版验收通过。

## 仍待作者裁决

1. 某一年春节，某位亲属自己做过的一件具体小事（谁提议／在哪／做了什么／哪句可核的话）。
2. 该记录的处置授权：去名后是否仍可识别相关长辈；公开历史残留如何处置（是否授权历史重写／GitHub Support 介入）。
3. 王麒皓一件高二／高三由他自己决定的小事。
