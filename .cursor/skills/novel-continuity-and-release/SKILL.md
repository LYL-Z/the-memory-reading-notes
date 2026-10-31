---
name: novel-continuity-and-release
description: >-
  Check continuity and release a chapter of 时间的复数人称. Use at the end of a
  chapter and before any export. Owns no cast list of its own. Length uses the
  Han-character counter, not Story Skills punctuation-inclusive counts.
---

# Continuity and release

Evidence stays in `editorial/` and `private_index/`. Manuscript chapters, when they exist, stay in `work/final/`. Story Skills may later check that manuscript. It must not grow a second cast, a second timeline, or a second promise ledger.

## Before a chapter is called done

1. Ages, school years, and who shares a desk match `editorial/timeline_seed.md` and the fact card.
2. A repeated event changes the meaning or it is cut.
3. Run `python scripts/hanzi_count.py` on the chapter. Record the number in `state/progress.json`.
4. Do not announce the book finished because a word-count tool crossed 1,100,000.

## Export

Markdown is the source. DOCX or EPUB comes later from that source. Do not export `private_index/` or `The Memory/私人资料/`.

## Not installed on purpose

Obsidian Local REST API, Smart Connections, and Longform are not connected to the original vault. Dataview is already enabled there and is not a continuity database. Do not turn any of them on in order to "finish" a release.
