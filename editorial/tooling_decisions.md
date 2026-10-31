# 工具决定

原则：先用已经能跑通的本地工具。不为了「像一个工程」去装云服务。

## 已经在用

| 工具 | 版本 / 位置 | 作用 | 回退 |
|---|---|---|---|
| Python 标准库 | 3.13.13 | 遍历、SHA-256、JSONL | 删除 `scripts/` 不影响原库 |
| SQLite FTS5 | `private_index/vault.db` | 651 篇全文检索 | 删除数据库即可。原笔记不在里面被改写 |
| 路径分类器 | `scripts/vault_audit.py` | 旧稿 / 订正 / 附件 / 技术目录 | 分类是启发式。精读可以改某一条的 `origin_class` |

自测过的分类：旧稿目录→AI_DRAFT，用户订正文件名→HUMAN_ORIGINAL，同学回忆路径→THIRD_PARTY，私密图片→PRIMARY_RECORD，普通人物页→MIXED。

## 本轮不安装

| 候选 | 原因 |
|---|---|
| 在线向量库、云端代理、自动克隆 | 任务书禁止把私人库外传。FTS 已经够做第一轮检索 |
| Obsidian Local REST API | 原库只读，磁盘遍历已经覆盖文件。不开放本地插件端口 |
| Tesseract / OCR | 295 个附件未读，但 246 个在私密层。等某一章点名再识别，避免批量生成不可靠转写 |
| MarkItDown | 本轮非 Markdown 正文几乎没有 docx。唯一 PDF 在高中目录，尚未证明值得加依赖 |
| 商业网文技能（长篇扫榜、章节钩子、去 AI 味流水线） | 会把这本书拉向连载模板。和「不继承旧文风、不注水」冲突 |
| 写作体系里的旧总纲 | 已从检索删除 |

## 检索时的排除

查询 `docs_fts` 时同时排除路径前缀：

- `百万长文写作/`
- `长篇创作/`
- `正式成文/`
- `写作体系/`
- `高中/素材/文学化推演/`

前三个本来就不在库里。后两个已经删行。写章脚本还要再挡一次，防止以后重扫时把它们加回去。

## Git

本工程**没有** `git init`。本地仓库会诱使人和 Vault 的自动推送混在一起。`private_index/` 已在 `.gitignore` 里。若以后要版本管理，只在本目录单独初始化，不添加远程，不加入 Vault 的 `scripts/push_vault.sh`。

## 失败时

扫描脚本对单文件异常会记入 `scan_summary.json` 的 `errors` 并继续。本轮 `errors` 为空。FTS 若损坏，删除 `vault.db` 后重跑 `scripts/vault_audit.py`，再跑 `scripts/patch_index.py` 与 `scripts/mark_close_reads.py`。不要对 Vault 做修复。
