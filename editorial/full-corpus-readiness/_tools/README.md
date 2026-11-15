# _tools：可复算证据

本目录把 `01`／`02`／`06` 与 PR 清单的生成逻辑一并入库，目的是让下一轮可以**重跑并比对**，而不是只能相信已生成的表格。

## 环境要求

- Python 3.9+，仅标准库（`io / os / re / csv / json / subprocess / collections`）
- 两个仓库已在下列位置检出（脚本顶部常量，可改）：

| 常量 | 默认值 | 说明 |
|---|---|---|
| `TM` | `D:/The Memory/The Memory` | 事实源库（只读） |
| `RN` | `D:/The Memory/tmp/reading-notes-review` | 写作仓 |
| `RN_MAIN` | `799a97df…` | 一至六部基线 commit |
| `TM_MAIN` | `ef33c98d…` | 事实库基线 commit |

`RN_V7` / `pr/84` 需先执行：

```bash
cd "D:/The Memory/tmp/reading-notes-review"
git -c http.proxy= -c https.proxy= fetch -q origin refs/pull/84/head:refs/remotes/pr/84
```

## 三个脚本

| 脚本 | 产出 | 说明 |
|---|---|---|
| `build_inventory.py` | `01_repository-inventory.tsv` | `git ls-tree -r` 遍历两仓全部 blob ＋ `os.walk` 遍历被 gitignore 的私密层。**私密层路径与文件名一律写 `REDACTED`**，只保留聚合计数——不要"补全"这一处 |
| `build_ledger.py` | `02_full-reading-ledger.tsv` | 以 `01` 为输入，把「本轮实际全文读过」的文件集合写入 `FULL` 字典。**改这个字典等于改覆盖率声明**，必须与 `12_...final-gate.md` 同步 |
| `build_chapter_atlas.py` | `06_seven-volumes-chapter-atlas.tsv` | 135 章逐章提取标题／字数／段数／对话／句法探针。第七部经 `git show pr/84:...` 读取，不依赖工作树 |

## 复算后应当得到的数字（2026-11-15 基线）

| 项 | 值 |
|---|---:|
| 清单行数 | 1,931 |
| 台账分布 | 25 FULL_TEXT ／ 122 STRUCTURED_ONLY ／ 1,784 UNREAD |
| 七部章数 | 135 |
| 七部正文汉字 | 826,610（一至六部 733,382 ＋ 第七部 93,228，不含 README） |

若复算结果与上表不符，**先怀疑基线 commit 变了**（远程 main 已前进，或 PR#84 被更新/合并），不要先改表。

## PR 状态快照

`2026-11-15-pr-state-snapshot.json` 是 `gh pr list --state all --limit 200` 的原样输出（83 个 PR）。它是"当时状态"的物证，**不是当前状态**。复核请重跑：

```bash
gh pr list --repo LYL-Z/the-memory-reading-notes --state all --limit 200 \
  --json number,state,isDraft,headRefName,baseRefName,headRefOid,title
```

## 不做什么

- 不写入两个仓库的任何内容文件（本工程只读）。
- 不读取受控私密层的正文；清单层也不得输出其文件名。
- 不使用 `editorial/fact_cards/` 的结论当作原始事实。
