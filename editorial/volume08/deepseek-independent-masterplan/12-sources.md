# 参考文献｜以及我实际核到什么程度

体例：MLA 简式。访问日期均为 **2026-11-24**。
每一条后面标一个**核查层级**，请按它判断可信度：

- **【全文】** 我读到了正文（或官方 PDF）的相关部分
- **【摘要】** 只读到出版方提供的摘要/题录
- **【转述】** 通过二手报道或数据库条目间接获得，未见原文

---

## 一、平台政策（这一节的结论直接影响了第 3 条要求的回答）

S1. Anthropic. "Usage Policy." Effective 12 Nov. 2026. https://www-cdn.anthropic.com/files/4zrzovbb/website/6ae2f5bb8675bcd9fac006125817ba1393b396e4.pdf 【全文】
　引用条款："Do Not Generate Sexually Explicit Content"（Depict or request sexual intercourse or sex acts / Generate content related to sexual fetishes or fantasies / Engage in erotic chats）；"Do Not Engage in Fraudulent, Abusive, or Predatory Practices"（Engage in actions or behaviors that circumvent the guardrails or terms of other platforms or services）。

S2. Anthropic. "Usage Policy." Effective 15 Sept. 2025. https://anthropic.com/legal/aup 【全文：Universal Usage Standards 部分】
　用于对照：现行版本在性内容条款上比 2025 版更具体。

S3. OpenAI. "Model Spec." 29 Oct. 2026. https://model-spec.openai.com/ 【全文：Do not generate disallowed content 一节】
　关键分层：Prohibited（仅涉未成年性内容）／Restricted（信息危害、敏感个人数据）／Sensitive content in appropriate contexts（明确包含 **erotica and gore**，允许变换）。

S4. OpenAI. "Usage Policies." Effective 20 Nov. 2026. https://openai.com/policies/usage-policies/ 【全文：Protect people／Keep young people safe 两节】

S5. xAI. "Acceptable Use Policy." Effective 26 June 2026. https://x.ai/legal/acceptable-use-policy 【转述】
　说明：直接访问 x.ai 被 Cloudflare 拦截，我通过一份公开法院文书对其条款的逐字引用获得文本（S6）。**未能独立核验是否存在更新版本**，采用前须复查。

S6. *X.AI LLC v. Ellison*, No. 0:26-cv-03425 (D. Minn. filed 27 July 2026), Compl. ¶ 25. CourtListener. https://www.courtlistener.com/docket/73678486/1/xai-llc-v-ellison 【全文：所含引文】

S7. xAI. "Pricing" / "API." https://docs.x.ai/developers/pricing ; https://x.ai/api 【全文：模型能力与上下文长度页】
　用于模型能力对照：grok-4.7 上下文 500k，输入 $2.00/M、输出 $6.00/M；grok-4.3 为 1M 上下文（Bedrock 发布页）。

---

## 二、物理（A 层：已被实验证实）

S8. Chou, C. W., et al. "Optical Clocks and Relativity." *Science*, vol. 329, no. 5999, 2010, pp. 1630–33. 【摘要＋转述】
　我读到的是 Physics Today 与 Science News 对该文的报道，二者一致给出：Al⁺ 光钟、75 m 光纤比对、升高 **33 cm** 可测出频差、10 m/s 量级运动时差、最好一台准确度 8.6×10⁻¹⁸。**未读原论文 PDF**，正文若要写具体数值须回查原文。

S9. Levi, Barbara Goss. "Time Dilation Seen at Just 10 m/s." *Physics Today*, 2010. https://physicstoday.aip.org/news/time-dilation-seen-at-just-10-m-s 【全文】

S10. "Everything Really Is Relative." *Science News*, 2010. https://sciencenews.org/article/everything-really-relative 【全文】

## 三、物理（A/B 层交界）

S11. Rozema, Lee A., et al. "Experimental Aspects of Indefinite Causal Order in Quantum Mechanics." *Nature Reviews Physics*, vol. 6, 2024, pp. 483–99. https://doi.org/10.1038/s42254-024-00739-8 【摘要＋题录】
　关键判断：量子开关已在多种单光子自由度实现；在计算、通信、计量、热力学有具体优势；**没有一般性计算优势**；不构成宏观因果逆转。

S12. "Watching the Clocks: Interpreting the Page–Wootters Formalism and the Internal Quantum Reference Frame Programme." arXiv:2203.06755. https://arxiv.org/abs/2203.06755 【全文：第 2.2 节】
　我据此处获得 PW 约束式 `(H_C+H_S)|Ψ⟩=0` 与条件态 `|ψ_W(t)⟩=⟨t|⊗I_W||Ψ⟩` 的标准表述。

S13. "Measurement Events Relative to Temporal Quantum Reference Frames." *Quantum*, vol. 9, 2025, art. 1616. https://quantum-journal.org/papers/q-2025-01-30-1616 【全文：摘要与通俗摘要】
　**本方案最关键的一条外部依据**：非理想（有限资源）钟导致时间非定域演化与时间序的根本限制；**若假定时间离散，幺正性与确定的时间序可恢复**。
　注意：这是理论工作，**没有**直接实验判决。小说公设从它出发，但不得声称它已被证实。

S14. Jafferis, Daniel, et al. "Traversable Wormhole Dynamics on a Quantum Processor." *Nature*, vol. 612, 2022, pp. 51–55. https://doi.org/10.1038/s41586-022-05424-3 【摘要＋题录】
　关键数据：9 比特线路、164 个双比特门、Google Sycamore；另见勘误 *Nature* 640 (2025): E32。

S15. Lykken, Joseph. "Traversable Wormhole Dynamics on a Quantum Processor." APS March Meeting Abstracts, 2024, W06.005. 【摘要】
　**必须引这一条的理由**：它明确说明该实验中"穿过虫洞"的空间自由度**与实验室的普通空间无关**，是纠缠动力学的涌现性质。任何"科学家造出虫洞"的表述都是错的。

S16. "The Universe's Most Basic Ingredient Is Information?"／IAS. *The Institute Letter*, Fall/Winter 2026. https://www.ias.edu/sites/default/files/IAS_Institute_letter_FW26_02-24.pdf 【全文：ER=EPR 一节】
　用于 ER=EPR（Maldacena & Susskind, 2013）的通行表述与"该猜想是否适用于我们所在宇宙仍是开放问题"的判断。

---

## 四、政治哲学与经济制度

S17. "Socialism." *Stanford Encyclopedia of Philosophy*. https://plato.stanford.edu/entries/socialism/ 【全文：中央计划、参与式计划、市场社会主义三节】
　用于"共产主义与世袭主权存在根本张力"这一判断的学理依据，以及计划经济的可行性批评（信息、计算、激励）。

S18. Norges Bank Investment Management. "Feedback on the SBTi's Net Zero Standard Second Public Consultation." 12 Dec. 2025. https://www.nbim.no/ 【全文：自述段】
　"manage USD 2,049 billion in assets and hold on average 1.5% of all listed companies globally"（2025 年第三季度末）。

S19. "Norway's Wealth Fund in 2025." BIFI Partners, 2026. https://bifipartners.com/insights/norway-wealth-fund-2025-lessons-uae 【转述】
　年末 NOK 21,268bn、7,201 家公司、68 国、股票占 71.3%、2025 年回报 15.1%、1998 年以来年化 6.6%。
　**这是二手汇总**；正式引用前应回查 NBIM 年报原文。

S20. 牛占林。《全球最大主权财富基金2025年获利近2500亿美元 年投资回报率达15.1%》。财联社，2026-02-27。https://www.cls.cn/detail/xk/2297765 【全文】
　与 S19 互相印证；另有"持有英伟达 1.3%、苹果 1.2%、微软 1.3%"等持股细节。

---

## 五、中文网络文学研究（用于爽感工程与市场判断）

S21. 中国作家协会网络文学中心。《2025 中国网络文学蓝皮书》。中国作家网，2026-08-10。https://wyb.chinawriter.com.cn/attachment/202608/10/c1432a39-2e81-400c-a4a2-7a7e01559fc2.pdf 【全文：摘要与创作、产业两节】
　数据：作品总量超 3300 万部；2025 年营收约 490 亿元；读者规模 5.25 亿；注册作者超 3500 万；新增影视长剧改编授权约 100 部、微短剧约 9000 部、动画约 90 部、漫画约 450 部。
　另提出"博弈型叙事"与"影视化前置／短篇崛起"两大新潮。

S22. 《在AI与短剧的变局中｜中国网络文学双年榜2024—2025（下）》。中国作家网，2026-07-07。https://www.chinawriter.com.cn/n1/2026/0707/c404027-40754956.html 【全文】
　**本方案市场判断的核心依据**：2025 年起点中文网年度月票排行前五为《捞尸人》《苟在初圣魔门当人材》《没钱修什么仙》《夜无疆》《玄鉴仙族》，"这些年度最受欢迎的小说全都不再明亮、温暖"。

S23. 《分化、激情与暗流｜中国网络文学双年榜2024—2025（上）》。中国作家网，2026-07-06。https://www.chinawriter.com.cn/n1/2026/0706/c404027-40754217.html 【全文】

S24. 肖映萱。《媒介分化与"女本位"变革——2024—2025年女频网络文学综述》。中国作家网，2026-05-26。https://www.chinawriter.com.cn/n1/2026/0526/c404027-40727710.html 【全文】
　用于"酸涩文""年代文""癫文"与女频读者对"被允许的欲望"的需求分析。

S25. 《〈十日终焉〉：游戏现实主义新网文经典》。中国作家网，2026-08-28。https://www.chinawriter.com.cn/n1/2026/0828/c404027-40788182.html 【全文】
　"痛爽共生""游戏现实主义""规则文"等概念来源。

S26. 《图像时代，让文学回归文字》。中国作家网，2025-04-16。https://www.chinawriter.com.cn/n1/2025/0416/c404027-40460775.html 【全文】
　"200 万同时追更""中国小说学会2024年度中国好小说网络小说第一名"等说法出自此文，属媒体表述，非官方统计。

S27. 《网络文学多元化发展进入新阶段》。中国作家网，2026-01-08。https://www.chinawriter.com.cn/n1/2026/0108/c404027-40641641.html 【全文】

S28. 《数字媒介如何推动网络小说结构新变》。中国作家网，2026-10-20。https://www.chinawriter.com.cn/n1/2026/1020/c404027-40818073.html 【全文】

S29. 《〈2025中国网络文学发展研究报告〉发布》。光明网，2026-04-20。https://news.gmw.cn/2026-04/20/content_38717451.htm 【全文】
　用户规模 5.26 亿、网民使用率 46.7%、"30 万全平台均订"等数据出自此文对中国社科院报告的报道。

S30. 网文666。《网文黄金三章怎么写才能留住读者？》。https://www.wangwen666.com/post/339.html 【全文】
　**仅作为行业经验文本引用，不作为学术依据。**文中"前三章流失率超过百分之七十""获得推荐位概率不足百分之五"等数字无一手来源，我在正文中明确标注为未经证实的说法。

---

## 六、我没有核到的东西（诚实清单）

1. **xAI 现行 AUP 的生效日期**：只核到 2026-06-26 版，无法确认是否有更新版本（官网被 Cloudflare 拦截）。
2. **Chou et al. 2010 原论文**：只读到两篇二手报道，数值互相一致，但未读 PDF。
3. **Page & Wootters 1983 原文**：通过 S12 的转述获得，未读原文。
4. **NBIM 年报原文**：只读到机构自述信与两篇二手汇总。
5. **起点月票榜的原始榜单页**：只读到中国作家网的综述转述。
6. **《捞尸人》等五部作品的正文**：**一部也没有读**。本文对它们的判断全部基于研究综述的类型描述，不是文本对照。任何"学习某部作品的具体写法"的表述，都必须先实际读该作品。
7. **Claude / GPT 的上下文长度与具体型号能力**：未逐一核验官方模型页；本文只使用"官方政策"与"可查的 xAI 定价页"，对能力不作断言。
