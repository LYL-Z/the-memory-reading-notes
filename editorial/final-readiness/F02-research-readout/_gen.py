import os, glob, io

root = 'D:/The Memory/tmp/reading-notes-review'
os.chdir(root)

rows = []

research_notes = {
 'literary-research.md': ('研究', 'Y', '八家作家+诺兰，五问式取用（解决什么/为何有效/用在哪/何时有害/变成自己的语言）；末节列不采用做法'),
 'narrative-clocks.md': ('研究', 'Y', '三重时间定义、不可靠五分法、章型分流；全书级结构主张'),
 'character-dynamics.md': ('研究', 'Y', '人物冲突并列表；含 2026-09-16 用户确认层（赵知道/曾喜欢）'),
 'prose-and-ai-patterns.md': ('研究', 'Y', '12 条散文/AI 痕迹诊断；引 2026-11-13 作者字数裁决'),
 'four-volume-editorial-risks.md': ('研究', 'Y', '九项风险按 A/B/C 分级；明确「本轮不改正文」'),
 'volumes-01-to-04-reading.md': ('研究', 'Y', '逐部判断；第一部最完整、第四部短而密'),
 'review-round-comparison.md': ('研究', 'Y', '审稿轮次与既有判断的同向/冲突对照；自报未读清单'),
 'project-understanding.md': ('研究', 'Y', '全书命题+权威顺序（作者裁决晚于知识库首页）'),
 'next-phase-handoff.md': ('状态', 'Y', '版本 SHA、覆盖清单、作者要求、下一步顺序'),
 'reading-coverage.md': ('状态', 'Y', '76 章字数核验、FULL/PARTIAL/METADATA 计数、G1-G10'),
 'model-collaboration.md': ('状态', 'N', '只有 Grok 4.7；Opus NOT_RUN；交叉评议 NOT_RUN'),
 'michael-study.md': ('研究', 'N', '外部人物研究；只取一般方法，明确禁止搬句子'),
}

outline_notes = {
 'outline/volume-01.md': ('卷纲', 'Y', '35 轮历史层积：19→20→18 章；24 项承诺；《右边那张床》暂缓'),
 'outline/volume-03.md': ('卷纲', 'Y', '16 章四幕；三时间层；教师姓名与终稿卡冲突'),
 'outline/volume-04.md': ('卷纲', 'Y', 'R7 定稿 18 章 71,325；引用八部 105 章蓝图'),
 'outline/volume-05.md': ('卷纲', 'Y', 'R6 19 章 79,883；跨卷知情顺序；阿澈化名'),
 'outline/volume-06.md': ('卷纲', 'Y', '20 章；章名沿用 PR#56；时代 2024-2025'),
}

state_notes = {
 'state/2026-11-13-volume03-r3-project-memory.md': ('状态', 'Y', '作者「小说不是论文」裁决；III 16 章 135,479'),
 'state/2026-11-13-volume04-opening-handoff.md': ('状态', 'Y', '作者任务：诺兰式不可靠、世界级为长期目标、不模仿大麦哥'),
 'state/2026-11-13-volume04-continuation-handoff.md': ('状态', 'N', '007-012 字数与朱学良 Q4/Q5 边界'),
 'state/2026-11-13-volume04-full18-handoff.md': ('状态', 'Y', '18 章 56,599；日期锚；作者最新标准'),
 'state/2026-11-13-volume04-r4-handoff.md': ('状态', 'N', 'R4 68,036；高风险重复清单'),
 'state/2026-11-13-volume04-r5-handoff.md': ('状态', 'Y', '朱 56 题问卷分章用途；问卷声部模板化风险'),
 'state/2026-11-13-volume04-r6-handoff.md': ('状态', 'N', 'R6 71,002；010/011 偏薄'),
 'state/2026-11-13-volume04-r7-final-main-handoff.md': ('状态', 'Y', 'R7 71,325 并入 main；四部均章 3,962 偏薄'),
 'state/2026-11-13-volume05-r3-handoff.md': ('状态', 'Y', '八部 147 章仅在 PR#56；V R3 七章'),
 'state/2026-11-13-volume05-r5-handoff.md': ('状态', 'Y', 'V R5 19 章 76,204；均章 4,011'),
 'state/2026-11-13-volume05-r6-handoff.md': ('状态', 'Y', 'V R6 79,883；方程可实算'),
 'state/2026-11-14-volume06-gpt6-r5-handoff.md': ('状态', 'Y', 'R5 删重至 102,286，违反字数闸门，禁合并'),
 'state/2026-11-14-volume06-gpt6-r5-1-handoff.md': ('状态', 'Y', 'R5.1 106,962，六章仍低于 R4，全卷 FAIL'),
 'state/volume06-handoff.md': ('状态', 'Y', 'VI R4 126,088；逐章口述锚（83 名、川大保底等）'),
 'state/next_actions.md': ('状态', 'Y', '六部 115 章 732,799 已并入 main；七项优先'),
 'state/progress.json': ('状态', 'Y', '115 章/732,799；门禁 human_blind_readers=0'),
 'state/volume03-progress.json': ('状态', 'N', 'III 早期 127,142，已被 R3 135,479 取代'),
}

evidence_notes = {
 'evidence/chapter-001.md': ('事实账', 'Y', 'F/I/X 三级；作者 2026-10-31 口述确认刘总与书名'),
 'evidence/chapter-002.md': ('事实账', 'N', '第二章「有材料/推演」两栏'),
 'evidence/chapter-003.md': ('事实账', 'Y', '床位表、525 八人、竹林杯、作息表；甲级口述'),
}

root_notes = {
 'AGENTS.md': ('规则', 'Y', '六部规则 9 条：三钟、四级标签、尺度、实名'),
 'README.md': ('状态', 'Y', '六部 115 章 732,799；七/八部仍称「候选」'),
 '给ChatGPT.md': ('作者原话', 'Y', '作者第一人称写作说明；禁止清单'),
}

v13 = {
 '1-001': '13=书架解释稍满', '1-002': '13=固定收束雏形', '1-003': '13=章末预告偏目录式',
 '1-004': '13=章末解释偏长', '1-005': '13=「再坚持一下」稍总结', '1-006': '13=收束安静，不删',
 '1-007': '13=参数过程略展示', '1-008': '13=「手放哪儿」重复', '1-009': '13=父亲问卷抢篇幅',
 '1-010': '13=短章，重复即内容', '1-011': '13=2026 程序段位置可议', '1-012': '13=一句解释可留',
 '1-013': '13=略满但具体', '1-014': '13=排练长度合法', '1-015': '13=525 复述略重复',
 '1-016': '13=干净章', '1-017': '13=排练长但有物', '1-018': '13=三节分法清楚',
 '2-001': '13=稍有说明文味', '2-002': '13=自省长句可忍', '2-003': '13=分寸可以',
 '2-004': '13=主题句可再少', '2-005': '13=童年段像加时', '2-006': '13=点名段可接受',
 '2-007': '13=一句像美学声明', '2-008': '13=章长可收', '2-009': '13=章末具体',
 '2-010': '13=六门复盘略平均', '2-011': '13=几乎无空转', '2-012': '13=动作密度高',
 '2-013': '13=自责已够', '2-014': '13=结尾够', '2-015': '13=长度刚好',
 '2-016': '13=地名多', '2-017': '13=座位图刚好', '2-018': '13=评语罗列略长',
 '2-019': '13=生物名词可减', '2-020': '13=收在未说那句', '2-021': '13=门牌已自纠',
 '2-022': '13=问卷条目略密', '2-023': '13=听完与伤人并存', '2-024': '13=收束重复最明显',
 '3-001': '13=具体，未收成起源', '3-002': '13=误写可再集中', '3-003': '13=试验次数多',
 '3-004': '13=搬米次数可收', '3-005': '13=幼儿园日常略满', '3-006': '13=修车与阳台重复',
 '3-007': '13=修东西吃饭重复', '3-008': '13=上山吃饭两遍', '3-009': '13=游戏轮次近',
 '3-010': '13=第二次大扫除功能近', '3-011': '13=后部像补温和结局', '3-012': '13=运动会可紧',
 '3-013': '13=物价收摊略长', '3-014': '13=手抄报重复', '3-015': '13=清单长',
 '3-016': '13=搬桌过程长',
 '4-001': '13=长度刚好', '4-002': '13=短，已拆归功', '4-003': '13=短章样本，无段末论文',
 '4-004': '13=历史讲解与报名同功', '4-005': '13=紧', '4-006': '13=短得合适',
 '4-007': '13=几次讨嫌功能近', '4-008': '13=后半略散', '4-009': '13=拍照语音略长',
 '4-010': '13=短，已停住补写冲动', '4-011': '13=分工场略长', '4-012': '13=评语与作文同功',
 '4-013': '13=散席略长', '4-014': '13=拒绝把别人排成队伍', '4-015': '13=晚饭电影略长',
 '4-016': '13=洗碗看火同功', '4-017': '13=账单可略收', '4-018': '13=刷新重复像手指',
}

def add(p, typ, claim, note):
    b = open(p, 'rb').read()
    t = b.decode('utf8')
    kb = round(len(b)/1024, 1)
    lines = t.count('\n') + 1
    rows.append((p.replace('\\', '/'), kb, lines, typ, claim, note))

for p in sorted(glob.glob('research/grok-onboarding/*.md')):
    n = os.path.basename(p)
    typ, claim, note = research_notes[n]
    add(p, typ, claim, note)

for p in sorted(glob.glob('research/grok-onboarding/chapter-cards/*.md')):
    add(p, '索引', 'N', '76 章卡说明：14 项/章；未读段不写判断')

vol_name = {'volume-01': 'Ⅰ', 'volume-02': 'Ⅱ', 'volume-03': 'Ⅲ', 'volume-04': 'Ⅳ'}
for p in sorted(glob.glob('research/grok-onboarding/chapter-cards/volume-*/*.md')):
    vd = os.path.basename(os.path.dirname(p))
    n = os.path.basename(p)
    t = open(p, encoding='utf8').read()
    title = t.split('\n')[0].lstrip('# ').strip()
    if n == '_unread.md':
        add(p, '索引', 'N', vol_name[vd] + ' 卷未读清单：本卷 0 未读')
    else:
        key = vol_name[vd].replace('Ⅰ', '1').replace('Ⅱ', '2').replace('Ⅲ', '3').replace('Ⅳ', '4') + '-' + n[:3]
        add(p, '章卡', '局部', vol_name[vd] + '-' + n[:3] + '《' + title + '》；14 项；' + v13[key])

for p in sorted(glob.glob('outline/*.md')):
    typ, claim, note = outline_notes[p.replace('\\', '/')]
    add(p, typ, claim, note)

for p in sorted(glob.glob('state/*.md')) + ['state/progress.json', 'state/volume03-progress.json']:
    typ, claim, note = state_notes[p.replace('\\', '/')]
    add(p, typ, claim, note)

for p in sorted(glob.glob('evidence/*.md')):
    typ, claim, note = evidence_notes[p.replace('\\', '/')]
    add(p, typ, claim, note)

for p in ['AGENTS.md', 'README.md', '给ChatGPT.md']:
    typ, claim, note = root_notes[p.replace('\\', '/')]
    add(p, typ, claim, note)

with io.open('editorial/final-readiness/F02-research-readout/F02-files.tsv', 'w', encoding='utf-8', newline='\n') as f:
    f.write('file\t体量KB\t读毕行数\t类型\t含实质主张\t备注\n')
    for r in rows:
        f.write('\t'.join(str(x) for x in r) + '\n')

print('rows', len(rows), 'totalKB', round(sum(r[1] for r in rows), 1), 'totalLines', sum(r[2] for r in rows))
