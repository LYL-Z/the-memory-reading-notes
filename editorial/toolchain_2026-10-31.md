# 工具决策 · 2026-10-31

语言 `zh-CN`。正文目标约 110 万汉字。官方字数是 `scripts/hanzi_count.py`，只数汉字。Story Skills 0.24.0 的 `characterCount("你好，世界！")` 为 6，标点计入。本计数器对同一句得到 4。

原库未改。没有安装 Obsidian 插件，没有打开 REST API，没有把私人笔记送去向量服务。

## 兼容性

| 项目 | 版本 | 许可证 | 安装方式 | 权限 | 结论 |
|---|---|---|---|---|---|
| danjdewhurst/story-skills | GitHub `v0.24.1`；npm 最新 `0.24.0`（已装这个） | MIT | `npm install story-skills@0.24.0`，Node ≥ 18。本机 Node 24.16 | 本地读写它自己的故事目录。不碰 Obsidian | 采用为章节工程 CLI。不运行 `story init`，避免先长出第二套人物表 |
| wgwtest/novel-writing | `v0.5.0-public` | MIT | Codex skill 目录，不是第二套数据库 | 只读审稿规则 | 不安装。审稿规则已收进 `chinese-prose-editor` 与证据技能 |
| jtydhr88/screenwriting-skills | 无 release，主分支 2026-10-03 | MIT | 26 个编剧技能 | 无 | 不安装整包。场景四问收进 `cinematic-scene-engine` |
| haowjy/creative-writing-skills | `v0.7.0` | Apache-2.0 | Claude / Cursor 插件，自带另一套故事目录 | 会建立自己的稿件结构 | 不安装。空话和读者检验收进中文编辑技能 |
| obsidian-local-rest-api | `5.5.2` | MIT | Obsidian 社区插件加本地 HTTP / MCP | 能读、改、删笔记 | 不装。原库只读。要接之前必须单独确认，并且只对副本开只读 |
| longform | `2.1.0`，2025-03 | Fuck Around and Find Out 0.2，含「不得作恶」的主观条款，不是 OSI 许可证 | Obsidian 插件，在库内建项目 | 改库内笔记顺序和统计 | 不装 |
| obsidian-smart-connections | `4.7.2` | Smart Plugins License，限制做成竞争性通用产品；私人使用允许 | 插件，在库内写向量索引 | 本地模型，索引含私人全文，写入原库 | 不装。检索继续用已有的 SQLite FTS |
| obsidian-dataview | 库内已启用；上游最新 `0.5.70`（2025-04） | MIT | 已经在原库 | 只查询笔记属性 | 不升级、不新装。它不是连续性账本 |

## 保留与排除

保留：

- Story Skills CLI，装在 `tools/story-cli`，已验证 `story --help`。
- 八个项目技能，只写规则，不各建一套人物表。
- 汉字计数器。
- 已有的证据库 `private_index/` 与 `editorial/character_tiers.md`。

排除：

- 四个写作框架同时做人物、章节和连续性。
- 三个会写入 Obsidian 库的插件。
- `story init`。它会按类型模板生成人物和世界观，和现有事实边界冲突。等人物等级表要导入时再单独做一次，并且只生成文件、不覆盖 `editorial/`。

## 架构

```text
原库 The Memory/The Memory     只读史料
private_index + editorial      唯一证据与人物等级
work/final                     将来的正文
tools/story-cli                章节检查与导出，不另存人物真相
scripts/hanzi_count.py         唯一字数
```

Story Skills 的 `continuity` 以后只检查 `work/final` 里已经写过的章节。人物等级仍以 `editorial/character_tiers.md` 为准。

## 安装顺序（已执行到第 4 步）

1. 核对八个仓库的版本、许可证和权限。
2. 本地安装 `story-skills@0.24.0`。
3. 写汉字计数器并自测。
4. 写八个专属技能。
5. 未做：`story init`、Obsidian 插件、向量索引、原库写入。
