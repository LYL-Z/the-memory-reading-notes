# -*- coding: utf-8 -*-
"""B05 / T058: 为 V1-018 与 V2-001..008 补 read_range 强证据（末行前20字 + 两口径字数）。

纪律：
1) 只改目标 8 行的第 4、9 字段，其余行按原始字节原样写回（保留各行 CRLF/LF 差异）。
2) 写前重读全文，写后校验：总行数不减、非空行仍为 9 字段、目标行内容与实测一致。
3) 所有数字由本脚本现场重算，与预期值 assert 比对，不采信台账原有「all N lines」。
"""
import io
import os
import re
import sys

P = 'editorial/full-corpus-readiness/read-records/read-records.tsv'

HAN = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')
FRONTMATTER = re.compile(r'\A---\r?\n.*?\r?\n---\r?\n', re.DOTALL)
HEADING = re.compile(r'(?m)^#{1,6}[ \t].*$')
FENCE = re.compile(r'(?ms)^```.*?^```')
HTML_COMMENT = re.compile(r'(?s)<!--.*?-->')


def official(text):
    text = text.lstrip('\ufeff')
    text = FRONTMATTER.sub('', text, count=1)
    text = FENCE.sub('', text)
    text = HTML_COMMENT.sub('', text)
    text = HEADING.sub('', text)
    return len(HAN.findall(text))


# path -> (lines, hanzi, raw, wc_l_note, 主事件, 隐私)
DATA = {
    'manuscript/volume-01/018.md': (
        319, 7080, 7086, '',
        '高一下历史课真心话大冒险：喻翰东问"你喜欢赵问竹吗"，他转向赵问竹当面说"我喜欢你"，四人笑场，课后无人再提',
        '喻翰东/伍筱丹/赵问竹/王麒皓/汪智文/曾子沣真名+四川大学寝室（中高）'),
    'manuscript/volume-02/001.md': (
        205, 7720, 7726, '',
        '小学某下午独自在益阳客厅自导自演"藏纸条—追车—盘问"警匪戏并反复重来，母亲下班进门，把一座城收成一张桌子',
        '谭双秋真名+益阳资阳区秀水俪园九栋+实验小学+夏恺宪/向睿馨（高）'),
    'manuscript/volume-02/002.md': (
        185, 6586, 6588, '',
        '高二分班放榜：先在二班名单找到赵问竹、再一行行找不到自己，终在五班（G2205）认出自己，与九班的王麒皓去食堂',
        '刘佑林真名+G2204/G2205班号+赵问竹二班+王麒皓九班（高）'),
    'manuscript/volume-02/003.md': (
        179, 7250, 7252, '',
        '分班考试前夜回旧四班 G2204 晚自习：为"复习得怎样"一句排演整晚，始终没起身走到赵问竹桌前',
        '赵问竹/喻翰东/伍筱丹/王麒皓真名+理实四班+525寝室（高）'),
    'manuscript/volume-02/004.md': (
        197, 8351, 8353, '',
        '由一日三餐写奶奶谭双秋与母亲何永红的劳作：做饭、走失后被找到、梅城猪田与老屋重建、父亲下厨与茶',
        '谭双秋（含"谭妈"）/何永红真名+安化梅城/东坪+实验小学86班（高）'),
    'manuscript/volume-02/005.md': (
        187, 8056, 8060,
        '本章末尾无换行符，wc -l 报 186；末行为第 187 行，已逐行读至该行。',
        '8月27日报到后住进过渡寝室自选床位、四班几人一夜湿背，28-29日分班考试（语文+选科／数学+英语），结果未出',
        '王麒皓/蒋明/阳隽豪/唐鑫宇/舒思宇/双汇/刘轩宏/汪智文/吴明博真名+525床位表+通勤路线（高）'),
    'manuscript/volume-02/006.md': (
        151, 6063, 6068,
        '本章末尾无换行符，wc -l 报 150；末行为第 151 行，已逐行读至该行。',
        '三人拍侦探短剧"钥匙不见了"、2017年夏结义，到2023-11-11十六岁生日宴把小学/初中/高中三拨人放进同一间包厢，散席各走',
        '夏恺宪/花阿姨/朱学良/邹鸿霖/李悦铭/王麒皓/汪智文/吴明博/李宇涵真名+2023-11-11+餐厅名（高）'),
    'manuscript/volume-02/007.md': (
        207, 6059, 6065, '',
        '15岁暑假武汉三天（江汉关、灯光秀、肥肥虾庄、户部巷、武大、黄鹤楼、东湖绿道），发现父母也在过自己的旅行；回益阳后暑假作业没做完',
        '赵问竹姓名+高一评语+武汉行程精确日期（中）'),
    'manuscript/volume-02/008.md': (
        273, 10447, 10452, '',
        '小学86班到六年级1305班：同桌王培森、前排曹卓雅、李顺贤补写的十栏评语、历年奖状与换班，最后离开益阳进长沙金海1907班',
        '李顺贤/李霞教师真名+王培森/曹卓雅/向睿馨/李漪涵/李晗/文曲星/郭婉妍+86/1305班号+奖状可回溯（高）'),
}


def main():
    raw = io.open(P, 'rb').read()
    rows = raw.split(b'\n')
    total_before = len(rows) - 1

    changed = []
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
        if fields[0] in DATA:
            nlines, off, rawc, wcnote, event, priv = DATA[fields[0]]
            text = io.open(fields[0], encoding='utf-8').read()
            actual_lines = len(text.split('\n')) - (1 if text.endswith('\n') else 0)
            assert actual_lines == nlines, (fields[0], actual_lines, nlines)
            assert official(text) == off, (fields[0], official(text), off)
            assert len(HAN.findall(text)) == rawc, (fields[0], len(HAN.findall(text)), rawc)
            body = [l for l in text.split('\n') if l.strip()]
            prefix = body[-1][:20]
            assert prefix
            fields[3] = f'L1-{nlines} (hanzi={off}; raw={rawc}含标题; 末行"{prefix}…")'
            fields[8] = ('逐行读至末行，末行前20字已引；' + (wcnote + ' ' if wcnote else '')
                         + f'主事件：{event}；隐私：{priv}')
            line = '\t'.join(fields)
            changed.append(fields[0])
        out.append((line + '\r').encode('utf-8') if has_cr else line.encode('utf-8'))

    if len(changed) != 9:
        print('ABORT: matched rows =', len(changed), changed, file=sys.stderr)
        sys.exit(2)

    total_after = len(out) - 1
    assert total_after == total_before, (total_before, total_after)

    io.open(P, 'wb').write(b'\n'.join(out))

    # ---- 写后校验 ----
    chk = io.open(P, 'rb').read().split(b'\n')
    bad = []
    for i, row in enumerate(chk):
        s = row.decode('utf-8').rstrip('\r')
        if s and len(s.split('\t')) != 9:
            bad.append((i + 1, len(s.split('\t'))))
    print('updated:', len(changed))
    print('rows before/after:', total_before, total_after)
    print('9-field violations:', bad)


if __name__ == '__main__':
    main()
