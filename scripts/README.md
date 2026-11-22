# scripts/ — 可复算工具

本目录存放审计与映射用的可复算脚本。每一份映射报告里的「复算命令」都应能在本目录找到对应代码。

## 语料读取（重要）

`06_seven-volumes-chapter-atlas.tsv` 的 path 列写 `manuscript/volume-07/`，但**第七部实体在 `work/m09/volume-07/`**（该 path 在工作树为空）。
任何只扫 `manuscript/` 的「全书」统计会**静默把 135 章变成 115 章**且不报错。

**全书检索必须两处并跑。** M09 的 `corpus.txt` 是两处合并的全量语料（3.1 MB，不入库）。

## 脚本

| 脚本 | 用途 |
|---|---|
| `hanzi_count.py` | 汉字计数（官方口径，与章表对账） |
| `dingzhen.py` | 顶针链检测（相邻句首尾重合 ≥2 字，或单字非停用；分双字/单字/回声/段内-跨段四层） |
| `struct_cnt.py` | 精确计数（母题词频等） |
| `struct_ctx.py` | 取上下文（引文核验） |
| `struct_digest.py` | 章级摘要统计 |
| `struct_dup.py` | 重复段检测 |
| `struct_dup2.py` | 14 字 n-gram 跨行最长公共子串（重复组主检工具） |
| `struct_table.py` | 生成 135 行章表 |
| `coverage_gap.py` | 覆盖率缺口 |
| `list_read_sizes.py` / `list_unread.py` | 阅读台账对账 |
| `append_round2_receipts.py` | 回执追加 |
| `mark_close_reads.py` | 标记已读 |
| `patch_index.py` | 索引补丁 |
| `fetch_repo_heads.py` | 取仓库 HEAD |

## 引文核验

`../qa/citecheck.py`（引用可定位性）、`../qa/quotecheck.py`（逐字比对）、`../qa/qalib.py`（公共库）。

## 顶针口径（两套，不可混用）

| 判据 | Ⅵ 章均 | `V6-018` |
|---|---:|---:|
| 台账／A10（2–4 字） | 37.5% | **71.3%（参与句占比，非顶针率）** |
| `dingzhen.py`（2 字＋单字非停用） | 31.5% | 43.8%（连接率） |

**两套尺子同章差 28 个百分点。引用时必须标注口径，不得并列。**
