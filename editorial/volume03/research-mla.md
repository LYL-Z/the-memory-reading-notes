# 第三部外部研究：MLA 条目、可核链接、适用章与不适用风险

> 建档：2026-11-12（research-lit）。用途：只给第三部写作与审稿做技法参照，不进入正文。
> 核验纪律：下列每条链接都在 2026-11-12 实际抓取过，并记录了 HTTP 状态。凡正文未读到者一律标 BLOCKED，不引原话、不补页码。中文原著按页面字形照录（繁体），需要简体时另标"转写"。
> 统计：登记 **8 条 URL（5 组主题）**，其中 **7 条读到正文**（官方演讲页仅取得状态，正文为 JS 壳）；BLOCKED **5 条**；逐字引文 **16 条**，全部经脚本在抓取文本中比对通过。

## 一、来源总表

| # | 主题 | 级别 | 状态 |
| --- | --- | --- | --- |
| 1 | 石黑一雄 2017 诺贝尔演讲（正文，经 Mainichi 连载第一篇） | 一手文本（媒体转载全文） | 200，读到正文 |
| 2 | 诺贝尔官网演讲页 | 官方页面 | 200，但为 JS 壳，正文不可抽取（已用 Wayback 复核，仍为壳） |
| 3 | 诺兰 2001 圣丹斯访谈（Movie Habit） | 一手访谈 | 200，问答全文 |
| 4 | 诺兰《记忆碎片》长访谈（Creative Screenwriting） | 一手访谈（存档） | 直播页 200 但为 JS 壳；正文经 Wayback 20150723000224 快照读到，另一快照 20191207074759 一致 |
| 5 | 诺兰结构转述（Go Into The Story，2017） | 二手转述 | 200；仅作旁证，不冒充诺兰原话 |
| 6 | 蕭紅《呼蘭河傳》第一章 | 原文（公有领域） | 200，全文 |
| 7 | 魯迅《故鄉》 | 原文（公有领域） | 200，全文 |
| 8 | 美国口述史协会《Principles and Best Practices》(2009) | 行业规范原文 | 200，全文 |

BLOCKED：诺贝尔官网 beta 站（403 Cloudflare）；The Guardian 推测的"演讲全文"URL（404）；OHA 2025 修订版 PDF（服务器有，但本工具不支持 application/pdf）；英国口述史学会 ethics 页（200，但正文被主题 CSS 吞掉，无可引段落）。

## 二、石黑一雄 2017 诺贝尔演讲

**MLA**：Ishiguro, Kazuo. “My Twentieth Century Evening – and Other Small Breakthroughs.” Nobel Lecture, 7 Dec. 2017, NobelPrize.org. *The Mainichi*, 8 Dec. 2017, mainichi.jp/english/articles/20171208/p2a/00m/0et/025000c.

**链接与状态**：mainichi.jp 一文 HTTP 200，读到演讲正文（标为 Part 1）。官方页 www.nobelprize.org/prizes/literature/2017/ishiguro/lecture/ HTTP 200，但正文由脚本渲染，抽取不到；Wayback 快照同样只有壳。因此本文件的引文全部出自 Mainichi 转载的第一篇，**不代表整篇演讲的完整结构**。

**逐字引文**（英文照录）
1. “the Japan that existed in my head might always have been an emotional construct put together by a child out of memory, imagination and speculation”
2. “this Japan of mine -- this precious place I'd grown up with -- was getting fainter and fainter”
3. “something not open to verification from outside”

**可迁移技法 → 适用章**
1. **"儿童用记忆、想象与推测拼成的世界"**（引文 1）——正对第三部的方法论：2007—2019 的益阳不是档案，是一个孩子拼出来的地方。适用：**01《照片以前的事》**（出生前后只能由父母转述与有限场景构成）、**02《名字不是自己取的》**（名字的来源由奶奶与母亲讲述）。
2. **"越来越淡"作为写作动机**（引文 2）——不是"怀旧"，是"再不做就没了"。适用：**16《毕业不只是一张照片》**（离开小学时把还没散的东西写下来），也可用于 **12《被念出来的作文》**（别人记得的版本正在消失）。
3. **"无法从外部验证"**（引文 3）——可用来给"回望声"设限：承认某些记忆只有我这一份，不去伪造外部证据。适用：**11《谁查过字典》**（两个版本都成立，不裁决）。

**不适用风险**
- 石黑重建的是**一个国家/一种生活方式**，不是家庭；把他的流亡者挽歌腔直接移给一个 6—12 岁孩子，会造出"小大人"（违反 bible 语言纪律）。
- "无法从外部验证"**不是**免于事实核查的许可证：本书的父母、奶奶、老师都还在，可核的事实仍要核。
- 该演讲是**成年作家对创作生涯的回顾**，其中的"small breakthroughs"是文学史叙事，不可当作儿童心理依据。

## 三、诺兰《记忆碎片》访谈

**MLA**
- Kjolseth, Pablo. “Interview with Christopher Nolan.” *Movie Habit*, 1 Feb. 2001, www.moviehabit.com/essay.php?story=chrisnolan01.
- Neff, Renfreu, and Daniel Argent. “Remembering Where It All Began: Christopher Nolan on Memento.” *Creative Screenwriting*, 20 July 2015, www.creativescreenwriting.com/remembering-where-it-all-began-christopher-nolan-on-memento/.

**链接与状态**：Movie Habit 2001-01-21 圣丹斯访谈，HTTP 200，问答全文。Creative Screenwriting 直播页 200 但正文为 JS 壳（“Loading article...”），正文经 Wayback 2015 快照读到（HTTP 200），另核 2019 快照一致。二手旁证：Myers, Scott. “Christopher Nolan on the Story and Structure of ‘Memento’.” *Go Into The Story*, 30 June 2017（HTTP 200；他只转述一段 2001 年视频，视频本身未看）。

**逐字引文**
1. “Memento 's very concerned with subjective perceptions of the world versus the concept of objective truth”（Movie Habit）
2. “My solution to that, which took a while to come up with, was to tell the story backwards so that it denied the audience the information that the protagonist is denied.”（Creative Screenwriting，存档）

**可迁移技法 → 适用章**
1. **信息剥夺而非倒叙炫技**（引文 2）：每次时间跳跃要让读者比人物多知道一件事、或与人物一同少知道一件事。适用：**11《谁查过字典》**（先给我确信的版本，再让王培森"不记得"的版本迟到）、**10《装在口袋里的爸爸》**（谁先说了哪一句，两人版本不同）。
2. **主观真相与客观真相并置**（引文 1）：不裁决哪个版本真，只让两种"真"共存。适用：**16《毕业不只是一张照片》**（不同去向的同学各有一份"那天的照片"）、**01《照片以前的事》**（家人转述的出生与我无法记得的出生）。
3. **结构由信息差驱动**：诺兰先按顺叙写完再回排。可迁移为：第三部先把 2007—2019 顺叙写成材料包，再决定哪一段交给 2026 回望。

**不适用风险**
- 电影靠剪辑让观众与主角同步失忆；小说没有镜头，倒放只会让读者迷路。第三部的时间跳跃必须靠**物件、日期、称谓**这些可核锚点。
- 本书没有失忆设定；孩子的"不知道"是年龄与信息位置，**不是叙述者不可靠**。把两者混同，会让 6 岁的"我"显得像在隐瞒。
- 诺兰谈的是电影结构，不是文学伦理；不可用他的访谈为"给真人补未证原话"背书。

## 四、蕭紅《呼蘭河傳》第一章

**MLA**：蕭紅. 《呼蘭河傳》. 1940. *維基文庫*, zh.wikisource.org/wiki/呼蘭河傳/第一章.

**链接与状态**：HTTP 200，第一章全文；总目页亦 200。只读了第一章，**未读其余六章与尾声**，不得概括全书。

**逐字引文**
1. “嚴冬一封鎖了大地的時候，則大地滿地裂著口。”
2. “嚴寒把大地凍裂了。”
3. “人的手被凍裂了。”
4. “呼蘭河就是這樣的小城，這小城並不怎樣繁華，只有兩條大街”
5. “只有憑了認路的人的記憶才知道是走向了什麼方向。”

**可迁移技法 → 适用章**
1. **物理事实先行**（引文 1—3）：先立"地裂、手裂、水缸裂"的事实，再让人物进来。适用：**04《走上六楼》**（先写米袋、楼道、灯，再写人）、**15《两次东北行》**（先写车程与温度）。
2. **同一句式反复＋名物清单**（引文 2、3、4）：不靠形容词，靠换物件推进。适用：**08《八十六班的一天》**（早读、课间操、大扫除各一件物）、**13《校门口的小卖部》**（五毛钱能买的东西逐样列出，但只列一次）。
3. **记忆是导航工具**（引文 5）：记忆不是感伤对象，是认路的本事。适用：**15《两次东北行》**（孩子靠认路判断还有多远）、**16《毕业不只是一张照片》**（多年后靠地名认回那天）。

**不适用风险**
- 东北的严寒与呼兰小城的地理由不能移植到益阳；第三部的地理事实是潮气、雨季、米粉与辣。
- 萧红的"我"是成年回望的抒情装置，第一章之后几乎退场；第三部若照搬这种"我"的密度，会让 6 岁孩子说出成年人的句子。
- 她的重复句式是**风格**，不是模板；连续三段同句式会变成仿写。

## 五、魯迅《故鄉》

**MLA**：魯迅. 《故鄉》. 1921. *維基文庫*, zh.wikisource.org/wiki/故鄉.

**链接与状态**：HTTP 200，全文。页内"故鄕／故鄉"两种字形并存，引文按页面实际字形照录。

**逐字引文**
1. “我冒了嚴寒，回到相隔二千餘里，別了二十餘年的故鄕去。”
2. “我所記得的故鄕全不如此。”
3. “深藍的天空中掛着一輪金黃的圓月”

**可迁移技法 → 适用章**
1. **记忆图景先于现实**（引文 3）：先给一个被美化的画面，再让它落地。适用：**09《王培森在旁边》**（先写"我记忆里的同桌"，再写他其实坐过第一排、讲台底下、最后一排）、**14《她也有别的朋友》**（先写三人组的完整，再写她另有朋友）。
2. **期待由第三方转述建立**（母亲说"他每到我家来时，总问起你"）：先让别人替期待说话，再由现场打破。适用：**05《好孩子》**（母亲说孩子在幼儿园很好，实际入园怯生）、**12《被念出来的作文》**（母亲记得被念，我不确定）。
3. **自审而非控诉**（引文 2）：先怀疑自己的记忆，再谈对方变化。适用：**11《谁查过字典》**（我确信，他不记得——先审自己的确信）。

**不适用风险**
- 《故鄉》是成年知识分子的回乡框架（"我"与闰土之间的阶级距离）；第三部的孩子没有"回乡"，只有上学、放学、搬家。
- 小说结尾的"路"的议论属于鲁迅的时代命题，不可移植成第三部的成长结论。
- 引文 1 的"别了二十余年"与第三部的时间尺度完全不同，不可借其句式写"别了六年"。

## 六、口述史伦理（OHA 2009）

**MLA**：Oral History Association. “Principles and Best Practices.” *Oral History Association*, 2009, oralhistory.org/about/principles-and-practices-revised-2009/.（该页自标 "out-of-date"；2018/2025 修订版存在，但 2025 版只有 PDF，本工具读不了）

**链接与状态**：HTTP 200，全文；页面顶部提示内容已过时，故只作 2009 年版引用。

**逐字引文**
1. “Oral historians insure that narrators voluntarily give their consent to be interviewed and understand that they can withdraw from the interview or refuse to answer a question at any time.”
2. “it is the practice in oral history for narrators to be identified by name”
3. “A critical approach to the oral testimony and interpretations are necessary in the use of oral history.”

**可迁移技法 → 适用章**
1. **同意与可撤回**（引文 1）：本书处理父母、奶奶、老师的讲述时，应保留"他们可以不讲/可以改口"的位置。适用：**01《照片以前的事》**（母亲讲述怀孕与生产，哪些她愿意讲、哪些一句带过）、**07《父亲回来以后》**（父亲对新疆那段可以只说"学费低些"）。
2. **具名与匿名的协商**（引文 2）：真实人物在书里出现，需作者与本人有明确约定；正文不写"据某某说"，但内部账要记谁提供了哪一段。适用：**02《名字不是自己取的》**（奶奶与师傅的讲述）、**14《她也有别的朋友》**（向睿馨的独立生活）。
3. **批判地使用口述证词**（引文 3）：口述不是事实本身，是"某人在某时的说法"。适用：**11《谁查过字典》**（两个版本并列不裁决）、**16《毕业不只是一张照片》**（同学去向由各自说法构成）。

**不适用风险**
- 家庭口述**不是**正式口述史项目；不能把 consent form、录音归档、IRB 程序写进小说。
- OHA 规范约束的是研究者与档案机构，**不能**用来要求家人"必须接受采访"。
- 规范里的"具名"不等于可以把私密材料写进正文；第三部仍受 bible 与项目隐私规则约束。
- 引文 1 的 "insure" 为原文拼写，引用时不要改成 "ensure"。

## 七、未取得与不可用（不得引用）

1. 诺贝尔官网演讲正文：官方页与 Wayback 均为 JS 壳，正文不可抽取；仅通过 Mainichi 转载读到第一篇。
2. beta.nobelprize.org：403（Cloudflare）。
3. The Guardian 推测 URL：404（未找到该报的演讲全文页）。
4. OHA 2025 修订版：只有 PDF（本工具不支持 application/pdf）。
5. 英国口述史学会 ethics 页：HTTP 200，但正文被主题 CSS 覆盖，无可引段落。
6. 诺兰《记忆碎片》剧本、石黑一雄小说原文：未取得，本文件不引其句子。

## 八、使用建议（给写作者的三条）

1. 这些来源只提供**结构问题**，不提供句子。任何一段若要"像石黑/像萧红"，就已经越界。
2. 每条技法都已绑定具体章；写完该章后，用对应的"不适用风险"反查一遍，比追求风格更像更有效。
3. 口述史那三条最好用的地方不是伦理姿态，而是**它对"谁在什么位置说这句话"的敏感**——这正好是第三部 2026 回望声最需要克制的地方。
