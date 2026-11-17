# -*- coding: utf-8 -*-
"""
F05 引文语义正确性复核 · 机械层（③逐字 / ④忠实）+ 分层抽取
=================================================================
只做可复算的事：
  A. 抽取 bidirectional-mapping/volume-01..07 全部引用 token（反引号内 `x:NN`）
     并按上下文判定其指向：FULL（带 .md 的完整路径）/ CHAP（本章正文）/ 同（承前来源）/ ALIAS（简称）
  B. 对每条「紧贴引文」（token 后紧跟 「…」 / （「…」））在源文件指定行内做归一化匹配，
     输出 EXACT / NORM（仅空白·标点·加粗差异）/ ELLIPSIS_OK（省略号分段全中）/ PARTIAL / ABSENT / LINE_OFF
  C. 输出 f05_citations_raw.tsv 供人工判 ④⑤⑥

⑤⑥ 不自动判——那必须人读原文与审稿意见。脚本只在 ③/④ 不通过时提升可疑度。
用法： python f05_check.py [-v]
"""
import os, re, sys, json, glob, unicodedata
from collections import Counter

FACT = r"D:/The Memory/The Memory"
WRITE = r"D:/The Memory/tmp/reading-notes-review"
MAP = WRITE + "/editorial/full-corpus-readiness/bidirectional-mapping"
OUT = WRITE + "/editorial/final-readiness/F05-citation-semantics"

# 简称 → 事实仓相对路径（只登记能唯一确定的高频简称）
ALIAS = {
    'G2204时间线': '高中/G2204/G2204高一入学、分组与寝室时间线.md',
    'G2204高一入学、分组与寝室时间线': '高中/G2204/G2204高一入学、分组与寝室时间线.md',
    '时间线页': '高中/G2204/G2204高一入学、分组与寝室时间线.md',
    '学业档案': '大学/四川大学/强基班/刘佑林学业档案.md',
    '回忆': '高中/素材/个人回忆/刘佑林关于赵问竹的高中回忆-2026-08-12.md',
    '赵问竹书面评价': '高中/素材/同学回忆/赵问竹关于刘佑林的书面评价.md',
    '竹林杯': '高中/素材/个人回忆/竹林杯与高一关系变淡-2026-08-28.md',
    '新加坡之行': '高中/素材/个人回忆/新加坡之行-2026.md',
    '麓山国际作息时间': '高中/素材/个人回忆/麓山国际作息时间-用户提供-2026-09-12.md',
    '母亲QQ相册时间线': '家庭/素材/母亲QQ相册时间线-2011至2026.md',
    '生日宴名单': '家庭/素材/母亲QQ相册-生日宴同学名单-2023-11-11.md',
    '生日宴页': '家庭/素材/母亲QQ相册-生日宴同学名单-2023-11-11.md',
    '书信整理': '初中/2022届/素材/家庭书信/2022-01-25写给父母的信-叙事整理.md',
    '刘佑林口述': '高中/素材/个人回忆/刘佑林口述-选科强基住宿同桌外号-2026-09-12.md',
    '刘佑林口述-选科强基住宿同桌外号': '高中/素材/个人回忆/刘佑林口述-选科强基住宿同桌外号-2026-09-12.md',
    '03_...': 'editorial/full-corpus-readiness/03_complete-writing-standards.md',
    '04_author-facts': 'editorial/full-corpus-readiness/04_author-facts-and-life-timeline.md',
    '10_contradictions…tsv': 'editorial/full-corpus-readiness/10_contradictions-and-fact-boundaries.tsv',
    '2022中考…': '初中/2022届/素材/升学/2022中考至麓山国际入学时间线-刘佑林回忆.md',
    '荣誉证书档案': '高中/素材/成长记录/刘佑林高中荣誉证书档案-2022至2025.md',
}

QUOTE = re.compile(r'^[）)\]】]?[：:]?[（(]?[「“]([^」”]{2,240})[」”]')
TICK = re.compile(r'`([^`\n]{1,180})`')
SPEC = re.compile(r'^(?P<pre>.*?)[:：](?P<spec>\d+(?:[-,–]\d+)*)$')

PUNCT_TABLE = str.maketrans({
    '｜': '|', '→': '>', '–': '-', '—': '-', '－': '-', '〜': '~', '～': '~',
    '（': '(', '）': ')', '，': ',', '。': '.', '；': ';', '：': ':', '、': ',',
    '！': '!', '？': '?', '“': '"', '”': '"', '‘': "'", '’': "'",
    '「': '"', '」': '"', '『': '"', '』': '"', '…': '...', '·': '.', '•': '.',
})


def norm(s, drop_punct=False):
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('**', '').replace('__', '').replace('`', '')
    s = s.translate(PUNCT_TABLE)
    s = re.sub(r'[\s\u3000]', '', s)
    if drop_punct:
        s = re.sub(r'[^\w\u4e00-\u9fff]', '', s)
    return s.lower()


def build_index():
    idx, bybase = {}, {}
    for root in (FACT, WRITE):
        for dp, dn, fs in os.walk(root):
            dn[:] = [d for d in dn if d not in ('.git', '.workbuddy', '私人资料', 'lover-best', 'node_modules')]
            for fn in fs:
                if not fn.endswith('.md'):
                    continue
                p = os.path.join(dp, fn).replace('\\', '/')
                rel = os.path.relpath(p, root).replace('\\', '/')
                idx[(root, rel)] = p
                bybase.setdefault(fn, []).append(p)
    return idx, bybase


def resolve(p, idx, bybase):
    p = p.replace('\\', '/').strip()
    if '...' in p or '…' in p:
        return None
    for root in (FACT, WRITE):
        if (root, p) in idx:
            return idx[(root, p)]
    h = bybase.get(os.path.basename(p), [])
    for x in h:
        if x.replace('\\', '/').endswith('/' + p):
            return x
    return h[0] if len(h) == 1 else None


def line_nums(spec):
    out = []
    for part in re.split(r'[,\s]+', spec):
        m = re.match(r'^(\d+)[-–](\d+)$', part)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if 0 < b - a < 500:
                out += list(range(a, b + 1))
        elif part.isdigit():
            out.append(int(part))
    return out


CHUNK = re.compile(r'[…⋯]{1,3}|\.{3,}')


def segments(q):
    return [x.strip() for x in CHUNK.split(q) if len(norm(x, True)) >= 3]


def match_level(quote, window_text):
    nq, nw = norm(quote, True), norm(window_text, True)
    if not nq:
        return ('EMPTY', None)
    if nq in nw:
        return ('EXACT', None)
    if norm(quote) in norm(window_text):
        return ('NORM', None)
    ss = segments(quote)
    if not ss:
        return ('ABSENT', norm(quote, True)[:30])
    miss = [s for s in ss if norm(s, True) not in nw]
    if not miss:
        return ('ELLIPSIS_OK', None)
    cover = 1 - sum(len(norm(s, True)) for s in miss) / max(len(nq), 1)
    return ('PARTIAL' if cover >= 0.72 else 'ABSENT', miss[0][:40])


TEXT_CACHE = None


def text_index():
    global TEXT_CACHE
    if TEXT_CACHE is None:
        TEXT_CACHE = []
        for dp, dn, fs in os.walk(FACT):
            dn[:] = [d for d in dn if d not in ('.git', '.workbuddy', '私人资料', 'lover-best', 'node_modules')]
            for fn in fs:
                if not fn.endswith('.md'):
                    continue
                fp = os.path.join(dp, fn)
                try:
                    t = open(fp, encoding='utf-8').read()
                except Exception:
                    continue
                TEXT_CACHE.append((fp.replace('\\', '/'), norm(t, True), t.split('\n')))
    return TEXT_CACHE


def locate_by_text(quote):
    """源不可解析时，用引文最长片段在事实仓里反查真实位置。返回 (path, line, seg)。"""
    segs = sorted(segments(quote), key=lambda x: -len(norm(x, True)))
    if not segs:
        return None
    seg = norm(segs[0], True)
    if len(seg) < 6:
        return None
    hits = []
    for fp, nt, lines in text_index():
        k = nt.find(seg)
        if k < 0:
            continue
        # 计算行号
        acc = 0
        ln = 1
        for i, L in enumerate(lines, 1):
            if acc + len(norm(L, True)) >= k:
                ln = i
                break
            acc += len(norm(L, True))
        hits.append((fp, ln, segs[0]))
    if len(hits) == 1:
        return hits[0]
    if hits:
        # 多命中：优先 高中/家庭/大学 素材页，且路径短的
        hits.sort(key=lambda x: (len(x[0]), x[0]))
        return hits[0] + (f'多命中{len(hits)}',)
    return None


def chapter_file(vol, chap):
    p = (f"{WRITE}/manuscript/volume-0{vol}/{chap}.md" if vol <= 6
         else f"{WRITE}/work/m09/volume-07/{chap}.md")
    return p if os.path.isfile(p) else None


def main():
    idx, bybase = build_index()
    rows = []
    files = []
    for v in range(1, 8):
        files += sorted(glob.glob(f"{MAP}/volume-{v:02d}/V{v:02d}-*.md"))

    for f in files:
        base = os.path.basename(f)
        mv = re.match(r'V(\d{2})-(\d{3})\.md$', base)
        if not mv:
            continue
        vol, chap = int(mv.group(1)), mv.group(2)
        chapf = chapter_file(vol, chap)
        raw = open(f, encoding='utf-8').read().split('\n')
        para_path = None      # 本段最近一次完整路径
        table_first = None    # 当前表格块的首个完整路径（「同」的归属）
        in_table = False
        for ln, text in enumerate(raw, 1):
            is_row = text.lstrip().startswith('|')
            if is_row and not in_table:
                in_table, table_first = True, None
            elif not is_row and in_table:
                in_table, table_first = False, None
            if not text.strip() or text.lstrip().startswith('#'):
                para_path = None
            # 单元格边界（表格行）
            cuts = [i for i, c in enumerate(text) if c == '|'] if is_row else []
            cell_first = {}
            line_first = None
            for m in TICK.finditer(text):
                body = m.group(1)
                sm = SPEC.match(body)
                if not sm:
                    continue
                pre, spec = sm.group('pre').strip(), sm.group('spec')
                # 定位所属单元格
                ci = sum(1 for c in cuts if c < m.start())
                kind, src, label = None, None, body
                if pre.endswith('.md'):
                    kind, src = 'FULL', resolve(pre, idx, bybase)
                    if src:
                        para_path = src
                        cell_first.setdefault(ci, src)
                        if line_first is None:
                            line_first = src
                        if table_first is None and is_row:
                            table_first = src
                elif pre == '':
                    before = text[max(0, m.start() - 12):m.start()]
                    if re.search(r'同卷\s*(?:Q\d+)?\s*[（(]?\s*$', before):
                        kind, src = 'SAME', para_path
                    elif re.search(r'同(?:文件|页|表|书)\s*(?:Q\s*\d+)?\s*[（(]?\s*$', before):
                        kind, src = 'SAME', line_first or cell_first.get(ci) or para_path
                    elif re.search(r'同\s*(?:Q\d+)?\s*[（(]?\s*$', before):
                        kind = 'SAME'
                        src = cell_first.get(ci) or table_first or para_path
                    else:
                        kind, src = 'AUTO', None
                        extra = cell_first.get(ci) or (para_path if is_row else None)
                elif re.match(r'^\d{3}$', pre):
                    kind, src = 'CHAP_REF', chapter_file(vol, pre) or None
                else:
                    a = ALIAS.get(pre)
                    kind = 'ALIAS'
                    src = resolve(a, idx, bybase) if a else None
                    if src:
                        para_path = src
                        cell_first.setdefault(ci, src)
                after = text[m.end():]
                qm = QUOTE.match(after)
                quote = qm.group(1) if qm else ''
                rec = dict(ch=base[:-3], ln=ln, cite=label, kind=kind,
                           quote=quote, status='', miss='', src=src or '')
                if kind == 'AUTO':
                    cands = [x for x in (extra, chapf) if x]
                    seen = []
                    for c in cands:
                        if c not in seen:
                            seen.append(c)
                    best, bestrank, bestlvl = None, -9, None
                    RANK = {'EXACT': 6, 'ELLIPSIS_OK': 5, 'NORM': 4, 'PARTIAL': 3,
                            'LINE_OFF': 2, 'ABSENT': 1, 'LINE_OOR': 0}
                    for c in seen:
                        sl = open(c, encoding='utf-8').read().split('\n')
                        nn = line_nums(spec)
                        if quote:
                            if nn and max(nn) > len(sl):
                                lv = 'LINE_OOR'
                            else:
                                lv, _ = match_level(quote, '\n'.join(sl[i-1] for i in nn if 1 <= i <= len(sl)))
                                if lv == 'ABSENT' and nn:
                                    lo, hi = max(1, min(nn)-3), min(len(sl), max(nn)+3)
                                    lv2, _ = match_level(quote, '\n'.join(sl[lo-1:hi]))
                                    if lv2 != 'ABSENT':
                                        lv = 'LINE_OFF'
                        else:
                            lv = 'NO_QUOTE' if len(nn) <= len(sl) else 'LINE_OOR'
                        r = RANK.get(lv, -1)
                        if r > bestrank:
                            best, bestrank, bestlvl = c, r, lv
                    if best:
                        src = best
                        rec['src'] = best
                        rec['kind'] = 'CHAP' if best == chapf else 'CONT'
                if not src:
                    got = locate_by_text(quote) if quote else None
                    if got:
                        rec['status'] = 'SRC_INFERRED'
                        rec['src'] = got[0]
                        rec['miss'] = f'实见第{got[1]}行'
                        s2 = open(got[0], encoding='utf-8').read().split('\n')
                        ns2 = line_nums(spec)
                        if ns2 and max(ns2) <= len(s2):
                            lv, ms = match_level(quote, '\n'.join(s2[i-1] for i in ns2 if 1 <= i <= len(s2)))
                            rec['status'] = 'INFER_' + lv
                            rec['miss'] = f'实见第{got[1]}行'
                    else:
                        rec['status'] = 'SRC_UNRESOLVED'
                    rows.append(rec); continue
                s = open(src, encoding='utf-8').read().split('\n')
                ns = line_nums(spec)
                if ns and max(ns) > len(s):
                    rec['status'] = 'LINE_OOR'
                    rec['miss'] = f'{max(ns)}>{len(s)}'
                    rows.append(rec); continue
                if not quote:
                    rec['status'] = 'NO_QUOTE'
                    rows.append(rec); continue
                cited = '\n'.join(s[i - 1] for i in ns if 1 <= i <= len(s))
                lvl, miss = match_level(quote, cited)
                if lvl == 'ABSENT' and ns:
                    lo, hi = max(1, min(ns) - 3), min(len(s), max(ns) + 3)
                    l2, m2 = match_level(quote, '\n'.join(s[lo - 1:hi]))
                    if l2 != 'ABSENT':
                        lvl, miss = 'LINE_OFF', f'{l2}@{lo}-{hi}'
                rec['status'], rec['miss'] = lvl, miss or ''
                rec['excerpt'] = norm(cited)[:200]
                rows.append(rec)

    order = {'ABSENT': 0, 'PARTIAL': 1, 'LINE_OFF': 2, 'LINE_OOR': 3, 'SRC_UNRESOLVED': 4,
             'INFER_ABSENT': 5, 'INFER_PARTIAL': 6, 'INFER_LINE_OFF': 7, 'INFER_NORM': 8,
             'INFER_ELLIPSIS_OK': 9, 'INFER_EXACT': 10,
             'NORM': 11, 'ELLIPSIS_OK': 12, 'EXACT': 13, 'EMPTY': 14, 'NO_QUOTE': 15}
    rows.sort(key=lambda r: (order.get(r['status'], 9), r['ch'], r['ln']))
    with open(f"{OUT}/f05_citations_raw.tsv", 'w', encoding='utf-8', newline='') as fh:
        cols = ('ch', 'ln', 'cite', 'kind', 'quote', 'status', 'miss', 'src', 'excerpt')
        fh.write('\t'.join(['章', '行', '引用', '类型', '引文', '状态', '缺失片段', '源文件', '原文摘录']) + '\n')
        for r in rows:
            fh.write('\t'.join(str(r.get(k, '')).replace('\t', ' ') for k in cols) + '\n')

    c = Counter(r['status'] for r in rows)
    k = Counter(r['kind'] for r in rows)
    print('状态：', json.dumps(c, ensure_ascii=False))
    print('类型：', json.dumps(k, ensure_ascii=False))
    print(f'合计 token {len(rows)}；其中有引文 {sum(1 for r in rows if r["quote"])}')


if __name__ == '__main__':
    main()
