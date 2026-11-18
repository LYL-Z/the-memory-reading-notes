# QWEN 执行状态（断点恢复文件）

> 恢复方式：**直接读本文件第五节「下一条动作」，从那里继续。不要重新交接、不要重做研究、不要重新制定计划。**
> **最后更新：第一部收口（阶段 E 上半完成）。累计 91 章正文完成。远端 HEAD 见第四节提交链末端。**

---

## 一、身份与边界

- 本线程＝《时间的复数人称》独立文学主创作线（QWEN 线），**PR #87**，分支 `creative/deepseek-literary-revision-20261117`。
- 另一 AI（WorkBuddy HY4 Flash）走 **PR #86**，分支 `literary-revision-20261117`。**两线并行，互不等待。**
- **禁止**：合并 #87／改 HY4 分支／合并 #84 #85／改事实仓／覆盖前任候选／重写历史／强推。
- 前四批以 DeepSeek 名义完成，**保留不重做**；第五批起以 QWEN 名义，目录 `editorial/literary-revision/qwen-max/`。
- 创作仓 **PUBLIC**，Draft PR 公开可见。**常规同步授权 ≠ 无限制发表许可**。
- 事实仓 `The Memory/私人资料/` **绝对禁止调用**。

## 二、环境与命令（照抄，勿改）

- Windows，**Bash 工具禁用，一律 PowerShell（pwsh 7）**。用户已选「完全访问」，不设 `require_escalated`、不请求风险确认。
- **每次调用先补 PATH**：`$env:PATH="D:\Git\cmd;C:\Program Files\GitHub CLI;"+$env:PATH`
- 主克隆（读源正文）：`D:\The Memory\tmp\reading-notes-review`
- **隔离 worktree（写候选）**：`D:\The Memory\tmp\ds-batch1`
- 源正文：一至六部 `manuscript/volume-0N/NNN.md`；**第七部 `work/m09/volume-07/NNN.md`**。

### 推送模板（已升级为重试循环，九十余次验证）

```
foreach($i in 1..3){
  git -c http.proxy= -c https.proxy= -c "credential.https://github.com.helper=!gh auth git-credential" push origin creative/deepseek-literary-revision-20261117 2>&1 | Select-Object -Last 1
  if($LASTEXITCODE -eq 0){ "PUSH OK"; break } else { Start-Sleep -Seconds 8 }
}
```

- 键名是**点号** `.helper`，写成 `/helper` 报 invalid key。
- **⚠ 网络故障是间歇性的，不要改配置**：`https_proxy`／`HTTPS_PROXY`／`http_proxy`／`ALL_PROXY` 全空，git 全局代理也全空，`Test-NetConnection github.com -Port 443` = True。曾出现 300s 超时与 schannel TLS 握手失败，**重试即成功**。
- commit 用 `-c user.name=LYL -c user.email=lyl@local`；push 后 `git rev-parse --short HEAD` 或 `git ls-remote` 核验。
- 长命令用 `run_in_background: true` ＋ `TaskOutput(block=true)`。
- **⚠ 后台 push 未完成时不要提前 Copy／编辑下一章**：`Copy-Item` 是后台命令的最后一步，提前手动复制并编辑会被后台 Copy 覆盖。**必须先 `TaskOutput(block=true)` 等完。**
- python 脚本写到 `$env:TEMP` 再执行，用 `[IO.File]::WriteAllText(..., (New-Object Text.UTF8Encoding $false))`。
- **⚠ 源文件复制后可能是 CRLF**：python 多行匹配前必须 `.replace("\r\n","\n")`。
- **⚠ Edit 的 old_string 必须用弯引号 “”**（脚本已把「」统一替换）。大范围整段替换／段落搬移改用 python 的 `s.index(a)` / `s.index(b)` 切片。
- 含中文括号文件名禁用 `git rm`（用 `rm -f` + `git add -A`）；单文件 >100MB 须 LFS。

### 固定工作流（每章一轮）

`Copy-Item` 源章→候选路径 → Read 源章全文 → 脚本批量修缺陷（首行标记＋reps，逐条打印 MISS）→ 若干 Edit 插入新增 → 脚本统计与清洁度校验 → Write REVIEW → `python $env:TEMP\upd6.py` → commit＋push（后台，重试循环）→ Copy 下一章。

### 清洁度校验固定项

`re.findall(r"[A-Za-z]{2,}",body)`（白名单：班级号 G2204／G2205；V7-001 母亲口语 scientific；V7-010 引语 PDF；V7-016 入境三句）；`s.count("**")`＝0；`s.count("「")`＝0；逗号尾行为 0；繁体检查 `[c for c in "撐這個們來時說後點於為與並發現實經驗裏" if c in s]`；关键短语计数防重复；受限真名扫描；**新增段是否提前复用原稿动作／剧透后文／时序颠倒／切断原稿对句**。

## 三、进度总表

| 阶段 | 卷 | 章数 | 状态 | 原稿 | 候选 | 净增 |
|---|---|---|---|---|---|---|
| A | 第四部 | 18/18 | **完成并推送** | 74,460 | 96,726 | +22,266（+29.9%） |
| B | 第三部 | 16/16 | **完成并推送** | 140,227 | 165,481 | +25,254（+18.0%） |
| C | 第五部 | 19/19 | **完成并推送** | 80,985 | 97,578 | +16,593（+20.5%） |
| D | 第七部 | 20/20 | **完成并推送** | 93,102 | 110,407 | +17,305（+18.6%） |
| E 上 | **第一部** | **18/18** | **完成并推送** | **140,403** | **152,629** | **+12,226（+8.7%）** |
| E 下 | 第二部 | 0/24 | **未开始，源文未读** | 172,099 | — | — |
| F | 第六部 | 0/20＋018A | 未开始 | 126,271 | — | — |
| G | 全书综合 | — | 未开始 | — | — | — |

**累计 91 章正文完成并推送。全书 135 章，剩 44 章（第二部 24＋第六部 20）。**

**⚠ 第一部基线已校正**：索引中 V1-010 原记 5,252、V1-017 原记 5,539 与源文件不符。已用 `fixidx1.py` 重新计数回写：**010→5,976、017→6,231**，第一部原稿总量 138,987→**140,403**。其余 16 行无误。**对外官方口径仍用 825,901。**

## 四、提交链（远端已核验）

`6ed5eac`（接手基线）→`bbb7afa`（第四部收口）→`879c871`（叫停断点）→`8b1c322`（第五部收口）→`dcb2880`→`e4b20d7`（第七部收口，73 章）→`6882abc`→`95cdbbe`（V1-004）→`4fed053`（005）→`eacfd97`（006）→`2760be6`（007）→`9deb36b`（008）→`360dc04`（009）→`33a07ae`（010）→`9e51fec`（011）→`a95e045`（012）→`1bd3bd4`（013）→`7204ab0`（014）→`16ed898`（015）→`ba260a5`（016）→`a587f7e`（017）→**本次（018＋第一部收口）**。

## 五、下一条动作（恢复后直接执行）

1. `$env:PATH="D:\Git\cmd;C:\Program Files\GitHub CLI;"+$env:PATH`
2. `Set-Location "D:\The Memory\tmp\ds-batch1"`；`git status -sb`；`git rev-parse --short HEAD` 确认干净且已同步。
3. **读取第二部第一章源文**：`D:\The Memory\tmp\reading-notes-review\manuscript\volume-02\001.md`（**第二部 24 章源文全部未读**）。
4. `Copy-Item` 到 `editorial\literary-revision\qwen-max\volume-02\V2-001-CANDIDATE.md`（目录需先建）。
5. **给 `cnt3.py` / `upd6.py` 的 vol 列表加入 `"02"`**（现为 `["01","03","04","05","07"]`），可用 `patchvol.py`。
6. 按固定工作流处理，每章 commit＋push，**不停下等指令**。

## 六、各卷处理原则（已确立，勿混用）

- **第三／四／五／七部**：原稿偏短、偏概述，采取**「只加不换」**——保留原稿场面，另补原稿完全没有的生活领域。**判据：净增接近零＝只改了语言，不是扩充。** 每章须能回答「补进了哪一个原稿没有的生活领域」。
- **第一部（第二部预计同类）**：原稿极成熟，单章 5,500–12,000 字，非线性与迟到揭示密集，语言几乎没有 AI 感。**一律不做语言重写，只做「缺陷修复＋材料新增」，原稿对白与场面原则上逐字保留。** 主要缺陷是**编辑事故级重复写入**（同一段心理／同一个例子／同一个站位写两三遍），第一部共清理约 30 处、净删约 1,200 字，全部为同义复述。**每章新增两段，净增全部来自新增。**

## 七、铁律（历次自查拦截汇总，写作前必读）

1. 年龄无独立依据即删；**奶奶在世**，不得写「奶奶走的那年」。
2. 跨章事件不擅自合并（雨天、两个「零」事件、两夜先后）。
3. 正文禁 markdown 加粗／英文／繁体／直角引号（人物口语与真实引语为白名单例外）。
4. **新增段不得逐字重复原稿已有对白或动作**；不得抢别章核心场景。
5. 未核人数一律模糊化。
6. **不得与原稿时序冲突、不得引用尚未发生的后文情节、不得切断原稿紧密对句。**
7. 住宿史须核：**初中金海三年全寄宿**；高一、高二上寄宿，高二下半走读，高三全走读。
8. **不得给赵问竹新增任何一句话、一个动作、一处心理**（第一部全卷已严格执行）。
9. 母亲授权极窄：**只用她自己问卷写下的答案，非家庭矛盾非隐私**；第一部全卷未新增母亲任何一句话。
10. **王麒睿须化名**（V2 问卷 Q1），创作仓 PUBLIC；**王麒皓是另一人，无化名要求**。
11. 数字须自洽（字数、笔画、人口、年龄）；物理数学须逐项验算。
12. 不得虚构第三方情绪、访谈证词、真实聊天回复。

## 八、辅助脚本（临时，均在 `$env:TEMP`）

- `cnt3.py` — 扫描候选对照 `chapter-index.json` 输出 orig/cand/delta 与总计。vol 列表 `["01","03","04","05","07"]`。
- `upd6.py` — 统计＋更新 QUEUE/LEDGER/各卷 MANIFEST/COUNTS。**每章 commit 前必跑。** 最近输出 `chapters: 90`。
- `patchvol.py` — 给 cnt3/upd6 的 vol 列表插入新卷号。
- `fixidx1.py` — 对 `manuscript/volume-01/*.md` 重新计数回写索引（已执行）。
- `scan_auth.py` — 全库扫描「王麒睿／虢俊杰／李茹冰」。**⚠ 最近一次 73 文件零命中，此后已增 V1-001…018，需重跑。**
- `sum1.py` — 第一部全卷体量表（已执行，输出见 V1-018 REVIEW 第二部分）。
- `chk101.py`…`chk118.py`、`chk501.py`…`chk519.py`、`chk701.py`…`chk720.py` — 清洁度校验模板，改路径即可复用。
- 各章一次性脚本 `fix101.py`…`fix118.py`、`mv115.py`／`mv116.py`（段落搬移）等。
- 索引：`D:\The Memory\tmp\chapter-index.json`，结构 `[vol, ch, title, hanzi]`。官方口径脚本 `scripts/hanzi_count.py`。

## 九、未完成与待裁（不阻塞创作）

**未完成**：第二部 24 章、第六部 20 章＋018A、阶段 G 全书综合；三类装置中**「邀请」仍无任何实写正文**（档案装置已七处、问卷装置已有专章 V5-005）；世界文学**联网**研究与真实来源登记未做；`DS-PACK-01.md` 未读；`QWEN-REVISION-LEDGER.tsv` 的 commit 列仍全为 `local`；91 章候选**从未通过 present_files 交付**，只走 GitHub。

**体量缺口（已登记 R2）**：第四部 96,726 距 11–13 万差 1.3–3.3 万；第五部 97,578 距 11–13 万差 1.2–3.2 万；第七部 110,407 距 12–14 万差 1–3 万。

**待作者裁决（集中登记，不得因此阻塞其他章）**：完整清单见各卷末章 REVIEW——
- 第一部：`volume-01/QWEN-V1-018-REVIEW.md` 第二部分第七节（13 项，**007 饮品品牌收窄为唯一内容级删改，优先确认**）
- 第五部：`volume-05/QWEN-V5-019-REVIEW.md` 后半
- 第七部：`volume-07/QWEN-V7-020-REVIEW.md` 第二部分（9 项）

**授权待办（发表前必须完成，不影响创作与同步）**：涉朱学良问卷章节须交他过目；涉母章节须交母亲过目（V3-001 第一优先）；涉刘拓段落须交刘拓过目；涉董佳好章节若定稿点名须先完成授权；**涉赵文邦书面引文、赵问竹书面评价、陈喜老师姓名须完成第三方过目**。

**已知过期文件陷阱**：`outline/volume-03.md:26,32` 把春游／大扫除派给李顺贤；`outline/volume-06.md:3` 章名沿用 PR #56；`QWEN-V3-007-REVIEW.md` 仍写「九岁／小两岁」而正文已订正为八岁／小一岁。
