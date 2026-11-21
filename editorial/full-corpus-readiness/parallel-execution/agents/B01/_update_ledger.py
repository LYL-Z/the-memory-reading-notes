# -*- coding: utf-8 -*-
"""B01 / T054: 为 V7 13 章补 read_range 强证据（末行前20字 + 可复算字数）。

只改 13 行，其余行按原始字节保留（含各行的 CRLF/LF 差异），避免与并发代理互相覆盖。
"""
import io, re, os

P = 'editorial/full-corpus-readiness/read-records/read-records.tsv'
TMP = r'C:\Users\Lenovo\AppData\Local\Temp\v7'

DATA = {
    '001': (197, 4038, 4043, '录取通知书到家：EMS拆封、报到日期纠正、邻居议论', '真名刘佑林+川大物理学院+益阳（高）'),
    '002': (264, 4241, 4247, '报到入住东园七舍两人间，与曾子沣第一晚定下钥匙规矩', '曾子沣姓名+川大+楼栋（中高）'),
    '003': (361, 4520, 4527, '军训与赵文邦熟起来：早饭、拉歌、青羊宫杜甫草堂遇雨', '赵文邦+平遥/长治+川大；刘桓彬/张天泽/龙昱丞（高）'),
    '004': (263, 4766, 4771, '寝室磨合：游戏弃队友、0.02精度之争、桌界与病中带粥', '曾子沣+湖南武冈+武冈二中（高）'),
    '005': (269, 4482, 4487, '第一周上课：微积分/线代/力学/网球，作业单位换算16→1.6', '陶军（力学教师）姓名+川大（中）'),
    '006': (233, 4161, 4168, '大一成绩：两个81、思政78、加权算错、热学75与电磁92', '刘佑林+成绩单数字（低中）'),
    '007': (291, 4032, 4039, '饭圈扩大：唐嘉睿组局、高泽聪双胞胎、帮搬显示屏', '高泽聪+西安+八十三中；唐嘉睿+河北/广东（高）'),
    '008': (256, 4475, 4478, '拍微视频：剧本四稿、忘带内存卡、剪到十六分钟再压到八分钟', '赵文邦/曾子沣姓名（中）'),
    '009': (205, 3874, 3882, '署名与贡献之争：导演栏排序、校赛一等奖、读赵文邦回忆', '赵文邦姓名+川大（中）'),
    '013': (311, 4225, 4232, '与父亲：泡茶、重庆十八梯山城步道、父亲新疆与电信经历、删朋友圈', '父亲职务（安化电信副总）+益阳（中高）'),
    '014': (387, 5470, 5478, '五一西安五天三人行：电影、兵马俑、华山、城墙，无联系方式', '赵问竹姓名+西安五一（高）'),
    '015': (303, 5788, 5797, '整理西安照片：裁掉陌生人肩膀、群里称“我妈朋友的女儿”、记忆与文件对不上', '赵问竹姓名+合照（高）'),
    '020': (287, 5252, 5259, '项目“保存”失效：改名半成品、向同学与父亲承认没做完', '低'),
}

def prefix(text, n=20):
    body = [l for l in text.split('\n') if l.strip()]
    return body[-1][:n]

HAN = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')
FRONTMATTER = re.compile(r'\A---\r?\n.*?\r?\n---\r?\n', re.DOTALL)
HEADING = re.compile(r'(?m)^#{1,6}[ \t].*$')
FENCE = re.compile(r'(?ms)^```.*?^```')
HTML_COMMENT = re.compile(r'(?s)<!--.*?-->')

def official(text):
    """与 scripts/hanzi_count.py 同口径：扣 frontmatter/围栏/注释/标题行。"""
    text = text.lstrip('\ufeff')
    text = FRONTMATTER.sub('', text, count=1)
    text = FENCE.sub('', text)
    text = HTML_COMMENT.sub('', text)
    text = HEADING.sub('', text)
    return len(HAN.findall(text))

raw = open(P, 'rb').read()
rows = raw.split(b'\n')          # 保留每行末尾的 \r
assert rows[-1] == b''

changed = 0
out = []
for row in rows:
    has_cr = row.endswith(b'\r')
    line = row[:-1].decode('utf-8') if has_cr else row.decode('utf-8')
    if not line:
        out.append(row)
        continue
    fields = line.split('\t')
    if len(fields) != 9:
        out.append(row)
        continue
    m = re.match(r'manuscript/volume-07/(\d{3})\.md$', fields[0])
    if m and m.group(1) in DATA:
        ch = m.group(1)
        nlines, off, rawc, event, priv = DATA[ch]
        text = io.open(os.path.join(TMP, ch + '.md'), encoding='utf-8').read()
        actual_lines = len(text.split('\n')) - (1 if text.endswith('\n') else 0)
        actual_off = official(text)
        actual_raw = len(HAN.findall(text))
        assert (actual_lines, actual_off, actual_raw) == (nlines, off, rawc), (ch, actual_lines, actual_off, actual_raw)
        fields[3] = f'L1-{nlines} (hanzi={off}; raw={rawc}含标题; 末行"{prefix(text)}…")'
        fields[8] = f'逐行读至末行，末行前20字已引；主事件：{event}；隐私：{priv}'
        line = '\t'.join(fields)
        changed += 1
    out.append((line + '\r').encode('utf-8') if has_cr else line.encode('utf-8'))

assert changed == 13, changed
open(P, 'wb').write(b'\n'.join(out))
print('updated rows:', changed, '| total rows:', len(out) - 1)
