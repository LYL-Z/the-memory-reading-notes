---
name: vault-memory-audit
description: >-
  Read-only inventory of The Memory vault for 时间的复数人称. Use before any
  chapter, outline, or claim that the archive has been fully read. Covers
  hashing, source classes, legacy AI isolation, and close-read receipts.
---

# Vault memory audit

The Obsidian vault `The Memory/The Memory` is read-only. Write only under `NovelStudio_Grok47`.

## When

Start of a session that continues the novel, and after many new notes appear.

## Steps

1. Read `state/progress.json` and `state/next_actions.md`.
2. If `private_index/vault.db` is missing, run `scripts/vault_audit.py`, then `scripts/patch_index.py`.
3. Do not use these paths for plot or voice: `百万长文写作/`, `长篇创作/`, `正式成文/`, `写作体系/`, `高中/素材/文学化推演/`, or the outer `小说连载稿/`.
4. A hash row is not a close read. Close reading appends one line to `private_index/read_receipts.jsonl`.
5. Do not install Obsidian plugins into the original vault. Do not enable a REST API against it.

## Failure

Record a per-file error. Do not repair the vault. If the index is corrupt, delete `private_index/vault.db` and rerun the scripts.
