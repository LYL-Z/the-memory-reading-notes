"""统计三章的对白体例：加引号的对白单元数 / 独立成段的引号对白段数。只读正文。"""
import re
import sys

files = [
    "manuscript/volume-01/009.md",
    "manuscript/volume-01/010.md",
    "manuscript/volume-01/011.md",
]

# 中文引号对（含单引号），成对统计
PAIR = re.compile(r"“([^”]{0,200})”|「([^」]{0,200})」")


def paragraphs(path):
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    # 跳过标题行（# 开头）
    body = [l for l in lines if l.strip() and not l.startswith("#")]
    return body, text


total_q = 0
for f in files:
    body, text = paragraphs(f)
    units = [a or b for a, b in PAIR.findall(text)]
    pure_lines = [l for l in body if l.strip().startswith("“") and l.strip().endswith("”") and l.strip().count("“") == 1]
    inline = len(units) - len(pure_lines)
    print(f"{f}: 引号对白单元={len(units)}  独立成段={len(pure_lines)}  行内嵌入={inline}")
    total_q += len(units)

print("合计引号对白单元 =", total_q)
