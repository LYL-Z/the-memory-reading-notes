# 引用核验说明（cards/research）

建立时间：2026-11-12。维护：research-lit。

## 1. 文件构成

| 文件 | 用途 |
| --- | --- |
| `sources.csv` | 全部实际抓取的 URL 台账：author / title / year / url / fetch_status / source_level / note |
| `src-01` … `src-13` | 每源一张研究卡：书目、URL 与 HTTP 结果、逐字摘录、可迁移技法、不可照搬、章节映射与可检验问题 |
| `09_draft.md` | 供主控并入最终报告的草稿：MLA Works Cited、条目→章节→问题、核验台账与 BLOCKED |
| `quote_register.csv` | 逐字引文清单（source_id / url / verification_level / quote / grep_check），可脚本核对 |
| `_sources/` | 2026-11-12 抓取原页的纯文本落盘；`_norm_*.txt` 为去换行版本（单行，便于整句 grep） |

## 2. 引文如何核对

1. 每条 `quote_register.csv` 中的 quote 都是对应 `_sources/` 抓取文本的**连续子串**（`grep_check = PASS`），未改字、未加省略号改写、未拼接。
2. 网页换行为排版产物，故核验使用 `_sources/_norm_*.txt`（把连续空白压成单个空格）。比对时同样做空白归一即可复现。
3. 中文古籍类（鲁迅、萧红）按维基文库页面的**繁体字形**照录，不转简体；引用时若主控要转简体，须另标“转写”。
4. 正文（《时间的复数人称》）引文只在卡片中标注为“（V1-015 首段逐字）”这类形式，取自 `_work/pr53` 每章前 6 行，来源不是外部文献。

## 3. 验证级别（source_level）

- **原文**：整篇可读并落盘（手册条目、访谈、影评、公有领域作品、节目简介）。
- **原文（存档快照）**：原文在存档中读到，现站为 JS 壳（Creative Screenwriting 访谈）。
- **二手转述**：只可引转述者自己的句子（Myers 博客；手册条目内所引 Booth / Genette / Phelan / Olson / Ricoeur）。
- **书目记录**：仅 Crossref / 出版社页信息，正文未取得（Olson、Phelan、Booth、Genette、Ricoeur 原书）。
- **BLOCKED**：正文未取得或不可解码，卡片中一律不引其内容，只登记状态。

## 4. 引号使用约定

卡片与草稿中的中文引号“”主要用于**逐字引文**；另有少量**设例/拟句**（用于说明“这样写会失真”），均在句中明确标为拟句或设例，且不进入 `quote_register.csv`。凡 `quote_register.csv` 未收录者，不得当作已核原文引用。

## 5. 已知问题

- `_sources/_norm_*.txt` 为单行文件，若用带“单行截断”的读取器打开，只能看到前 2000 字；核对请用脚本整读或读 `_sources/` 原始多行文件后再归一。
- 史铁生、芥川正文部分依赖转引或段题，已在对应卡片标明，未冒充通读。
