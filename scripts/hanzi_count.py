# -*- coding: utf-8 -*-
"""Count Han characters in novel prose. Punctuation, markup, and headings are excluded."""

from __future__ import annotations

import re
import sys
from pathlib import Path

HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)
HEADING = re.compile(r"(?m)^#{1,6}[ \t].*$")
FENCE = re.compile(r"(?ms)^```.*?^```")
HTML_COMMENT = re.compile(r"(?s)<!--.*?-->")


def prose_body(text: str) -> str:
    text = text.lstrip("\ufeff")
    text = FRONTMATTER.sub("", text, count=1)
    text = FENCE.sub("", text)
    text = HTML_COMMENT.sub("", text)
    text = HEADING.sub("", text)
    return text


def hanzi_count(text: str) -> int:
    return len(HAN.findall(prose_body(text)))


def count_paths(paths: list[Path]) -> tuple[int, list[tuple[str, int]]]:
    rows = []
    total = 0
    for path in paths:
        n = hanzi_count(path.read_text(encoding="utf-8"))
        rows.append((str(path), n))
        total += n
    return total, rows


def self_test() -> None:
    assert hanzi_count("你好，世界！") == 4
    assert hanzi_count("---\ntitle: 元数据\n---\n# 标题\n\n正文。\n") == 2
    assert hanzi_count("```\n汉字\n```\n\n外面\n") == 2
    sample = "你好，世界！"
    # Story Skills 0.24.1 counts this as 6 graphemes, punctuation included.
    assert hanzi_count(sample) != 6


if __name__ == "__main__":
    self_test()
    args = [Path(p) for p in sys.argv[1:]]
    if not args:
        print("hanzi_count self-test ok")
        raise SystemExit(0)
    total, rows = count_paths(args)
    for name, n in rows:
        print(f"{n}\t{name}")
    if len(rows) > 1:
        print(f"{total}\tTOTAL")
