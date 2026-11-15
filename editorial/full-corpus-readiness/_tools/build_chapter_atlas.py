#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract per-chapter structural indicators across all 135 chapters.

Read-only. Outputs:
  - seven-volumes-chapter-atlas.tsv (06)
  - diagnostics summary printed to stdout
"""
import io, os, re, json, subprocess, csv, collections

RN = r"D:/The Memory/tmp/reading-notes-review"
OUT = os.path.join(RN, "editorial", "full-corpus-readiness")
V7_REV = "pr/84"

CHARS = ["刘佑林","赵问竹","王麒皓","唐鑫宇","宋俊豪","刘弈帆","刘奕帆","阳隽豪","何舟","汪智文",
         "董佳好","钟康明","颜子杰","曾子沣","赵文邦","唐嘉睿","高泽聪","张天泽","刘桓彬","鞠佳恒",
         "王际翔","喻翰东","伍筱丹","向睿馨","夏恺宪","阳松","舒思宇","王麒睿","夏思成","张可文",
         "龙昱丞","陶军","李顺贤","李霞","杨革非","向雄海","邓智刚","朱学良","王培森","陈喜",
         "父亲","母亲","奶奶","爷爷","外婆","外公","舅舅","小姑","李博涵","郑森","成澜","阿澈"]

# AI-writing-habit probes (regex, label)
PROBES = [
    (r"我后来才(明白|懂|知道|意识到)", "later_realize"),
    (r"现在(回想|想|看)起来", "now_looking_back"),
    (r"不是[^。！？]{1,30}而是", "not_but"),
    (r"我(想|要)说[^。]{0,12}(却|但|又)(没有|没)", "wanted_to_say_but"),
    (r"忽然(明白|懂|意识到|知道)", "suddenly_realize"),
    (r"我(终于|总算)(明白|懂|知道)", "finally_realize"),
    (r"这(才|就是)(长大|成长|成熟)", "growth_word"),
    (r"根[据本]?[问卷档资]", "meta_questionnaire"),
    (r"知识库|档案|资料(里|中)(记录|写|载)", "meta_archive"),
    (r"【(有界推演|文学化重构)", "annotated_reconstruction"),
    (r"写到这里", "meta_authorial"),
    (r"我(学到|懂得)了", "lesson_learned"),
    (r"那一刻我", "that_moment"),
    (r"至少我(知道|明白)", "at_least_i_know"),
]

def read_ch(v, ch):
    if v == 7:
        return subprocess.run(["git","-C",RN,"show",f"{V7_REV}:manuscript/volume-07/{ch}.md"],
                              capture_output=True).stdout.decode("utf-8","ignore")
    return io.open(os.path.join(RN,"manuscript",f"volume-0{v}",ch+".md"),encoding="utf-8").read()

def main():
    rows=[]
    diag = collections.Counter()
    per_vol_probe = collections.defaultdict(collections.Counter)
    for v in range(1,8):
        n = 20 if v==7 else {1:18,2:24,3:16,4:18,5:19,6:20}[v]
        for i in range(1,n+1):
            ch=f"{i:03d}"
            t=read_ch(v,ch)
            paras=[p.strip() for p in t.split("\n") if p.strip()]
            title=paras[0].lstrip("# ").strip()
            body=[p for p in paras if not p.startswith("#")]
            hz=sum(1 for c in t if "\u4e00"<=c<="\u9fff")
            # dialogue lines (quoted speech)
            dial=len(re.findall(r"[“「][^”」]{1,120}[”」]", t))
            quotes=len(re.findall(r"[“”「」]", t))
            present=[c for c in CHARS if c in t]
            years=sorted(set(re.findall(r"(?:19|20)\d{2}\s*年", t)))
            dates=sorted(set(re.findall(r"\d{1,2}月\d{1,2}日", t)))
            probes={lab:len(re.findall(pat,t)) for pat,lab in PROBES}
            for lab,c in probes.items():
                diag[lab]+=c; per_vol_probe[v][lab]+=c
            # first/last body paragraph
            rows.append(dict(
                volume=v, chapter=ch, path=(f"manuscript/volume-07/{ch}.md" if v==7 else f"manuscript/volume-0{v}/{ch}.md"),
                version=("PR#84/R9" if v==7 else "main@799a97d"),
                title=title, hanzi=hz, paragraphs=len(body), dialogue_lines=dial, quote_marks=quotes,
                characters=",".join(present[:12]), year_marks=",".join(years), date_marks=",".join(dates),
                probe_later_realize=probes["later_realize"], probe_now_looking=probes["now_looking_back"],
                probe_not_but=probes["not_but"], probe_say_but_silent=probes["wanted_to_say_but"],
                probe_suddenly=probes["suddenly_realize"], probe_meta_q=probes["meta_questionnaire"]+probes["meta_archive"],
                probe_meta_authorial=probes["meta_authorial"], probe_lesson=probes["lesson_learned"],
                first_sentence=(body[0][:70] if body else ""), last_sentence=(body[-1][:70] if body else "")))

    fields=list(rows[0].keys())
    p=os.path.join(OUT,"06_seven-volumes-chapter-atlas.tsv")
    with io.open(p,"w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t"); w.writeheader()
        for r in rows: w.writerow(r)
    print("atlas rows:",len(rows),"->",p)
    print("total hanzi:",format(sum(r["hanzi"] for r in rows),","))
    print("total dialogue lines:",sum(r["dialogue_lines"] for r in rows))
    print()
    print("=== global probe counts ===")
    for k,vv in diag.most_common(): print(f"{vv:5d}  {k}")
    print()
    print("=== per-volume: probe density (count per 10k hanzi) ===")
    for v in range(1,8):
        hz=sum(r["hanzi"] for r in rows if r["volume"]==v)
        c=per_vol_probe[v]
        tot=sum(c.values())
        print(f"V{v} hz={hz:>7,} probes={tot:>4} density={tot/hz*10000:6.2f}")
    print()
    print("=== per-volume: mean hanzi / mean dialogue lines ===")
    for v in range(1,8):
        rs=[r for r in rows if r["volume"]==v]
        print(f"V{v} chapters={len(rs)} mean_hz={sum(r['hanzi'] for r in rs)//len(rs):>6} mean_dialogue={sum(r['dialogue_lines'] for r in rs)/len(rs):5.1f}")

if __name__=="__main__":
    main()
