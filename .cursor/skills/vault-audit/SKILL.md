---
name: vault-audit
description: Read-only inventory of The Memory vault for the autobiographical novel. Use before any chapter, outline, or style decision in NovelStudio_Grok47.
---

# Vault audit

The Obsidian vault is read-only. Write only inside `NovelStudio_Grok47`.

## When

Use this at the start of a session that continues the novel, and again after many new notes appear.

## Steps

1. Read `state/progress.json` and `state/next_actions.md`.
2. If `private_index/vault.db` is missing, run `scripts/vault_audit.py`, then `scripts/patch_index.py`.
3. Do not query these prefixes for plot or voice: `百万长文写作/`, `长篇创作/`, `正式成文/`, `写作体系/`, `高中/素材/文学化推演/`.
4. Close-reading a file appends one line to `private_index/read_receipts.jsonl`. A hash row is not a close read.
5. Stop before family-interior scenes and before any explicit sexual scene involving a person under 21.

## Failure

A scan error is recorded per file. Do not repair the vault. Delete `private_index/vault.db` and rerun the scripts if the index is corrupt.
