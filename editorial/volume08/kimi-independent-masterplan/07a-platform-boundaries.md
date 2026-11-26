# 平台官方边界与研究分工摘要

核查时间：2026-11-24。官方政策和模型页面会变化，正式创作前应重新核对当前版本。本文件只作研究与工作流说明，不承诺任何平台必然生成指定内容。

## Anthropic / Claude

公开 Usage Policy 明确保护儿童，限制利用真实个人图像制作性或私密内容，并对欺骗、隐私和敏感用途提出要求。模型总览按具体模型列出上下文和能力；部分 Claude 模型提供 1M token 上下文或测试能力，但不能泛化为“Claude 都能无误差读完整项目”。

公开政策不是“露骨内容必然可生成”的承诺。实际创作还受当前产品条款、部署规则和输出限制影响。适合由作者通过当次试写评估其长文、人物关系和文学复审表现，而不是沿用“Claude 只负责克制文风”的刻板分工。

## OpenAI / GPT

Model Spec 对未成年人或年龄模糊的性内容、非自愿与剥削性内容设有禁止，并对露骨性内容、真实人物敏感内容与适用情境作出区分。模型页面和上下文能力随具体模型变化，不能用一个固定版本号代表整个 GPT 系列。

GPT 可以用于资料核查、逻辑审计、公式检查、跨方案比较与文学创作，不宜被旧任务书固定成“只做结构和验收”。当次实际输出质量比角色想象更可靠。

## xAI / Grok

公开 Acceptable Use Policy 包含儿童保护、真实个人性影像、隐私、欺骗与滥用限制。API 文档中的 `nsfw` 自定义审核信号，是供调用方识别并拦截或降级处理的内容标记，**不是露骨内容生成许可证**。

不同 Grok 产品、API 模型、上下文和区域可能有不同规则。“Grok 没有限制”或“只要把亲密段落交给 Grok 就行”没有官方依据。它可以参与探索、对白和成熟主题研究，但不承担绕过其他平台边界的角色。

## 本轮可执行范围

- 可以研究成熟言情、欲望、身体、婚姻和家庭。
- 可以写独立原创成年人物明确互相选择的非露骨亲密。
- 可以讨论不同平台公开政策的差异和适用场景。
- 不写露骨性细节，不为可识别真实人物虚构私密性史，不把未成年人性化。
- 不因某平台限制而安排另一平台完成同一越界内容。
- 不把长上下文窗口等同于完整理解；每批仍需阅读账本与事实核验。

## 建议的协作方式

如果未来需要多模型参与，按任务拆分：科学核查、人物试读、连续性审计、正文试写和作者整合。每位参与者读取同一份必要的作者指令与场景材料，独立提交；最终由作者决定，而不是以模型投票取代文学判断。

## 官方入口

- Anthropic Usage Policy：https://www.anthropic.com/legal/aup
- Claude Models Overview：https://docs.anthropic.com/en/docs/about-claude/models/overview
- OpenAI Model Spec：https://model-spec.openai.com/
- OpenAI Usage Policies：https://openai.com/policies/usage-policies/
- OpenAI Models：https://platform.openai.com/docs/models
- xAI Acceptable Use Policy：https://x.ai/legal/acceptable-use-policy
- xAI Models：https://docs.x.ai/docs/models
- xAI Custom Moderation Controls：https://docs.x.ai/developers/advanced-api-usage/custom-moderation-controls
