# -*- coding: utf-8 -*-
"""Read-only vault inventory. Writes only under NovelStudio_Grok47."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import sys
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

PROCESSOR = "vault-audit-0.1.0"
VAULT = Path(r"D:\The Memory\The Memory")
STUDIO = Path(r"D:\The Memory\NovelStudio_Grok47")
PRIVATE = STUDIO / "private_index"
EDITORIAL = STUDIO / "editorial"

NOVEL_TOPS = {"百万长文写作", "长篇创作", "正式成文"}
TECH_TOPS = {".git", ".obsidian", ".claudian", ".workbuddy", "scripts", "tmp"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".heic"}
AUDIO_EXT = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi"}
DOC_EXT = {".pdf", ".docx", ".doc", ".pptx", ".xlsx", ".xls"}

WIKILINK_RE = re.compile(r"!??\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
TAG_RE = re.compile(r"(?<![\w/])#([^\s#\]|]+)")
HANZI_RE = re.compile(r"[\u4e00-\u9fff]")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_id_for(rel: str) -> str:
    return hashlib.sha256(rel.encode("utf-8")).hexdigest()[:16]


def classify(rel: str, ext: str) -> tuple[str, str]:
    parts = rel.split("/")
    top = parts[0]
    name = parts[-1]
    if "用户订正" in name:
        return "HUMAN_ORIGINAL", "filename"
    if top in NOVEL_TOPS:
        return "AI_DRAFT", "novel_directory"
    if any(token in rel for token in ("同学回忆", "书面评价", "书面回忆")):
        return "THIRD_PARTY", "path_token"
    if top in TECH_TOPS or top.startswith("."):
        return "UNKNOWN", "technical"
    if top == "私人资料":
        if ext in IMAGE_EXT or ext in DOC_EXT or ext in AUDIO_EXT or ext in VIDEO_EXT:
            return "PRIMARY_RECORD", "private_attachment"
        return "MIXED", "private_text_often_mediated"
    if top == "问卷回收":
        return "THIRD_PARTY", "questionnaire"
    if top in {"写作体系", "项目管理", "背景资料", "文化与审美"}:
        return "MIXED", "system_or_compiled"
    if top in {"小学", "初中", "高中", "大学", "家庭", "人物关系", "隐私"}:
        return "MIXED", "compiled_life_page"
    return "UNKNOWN", "unclassified"


def sensitivity_for(rel: str, name: str) -> str:
    if rel.startswith("私人资料/") or rel.startswith("隐私/") or "私密" in name:
        return "restricted"
    return "personal"


def kind_for(ext: str, rel: str) -> str:
    if ext == ".md":
        return "md"
    if ext == ".txt":
        return "txt"
    if ext == ".canvas":
        return "canvas"
    if ext == ".excalidraw":
        return "excalidraw"
    if ext in IMAGE_EXT:
        return "image"
    if ext in AUDIO_EXT:
        return "audio"
    if ext in VIDEO_EXT:
        return "video"
    if ext == ".pdf":
        return "pdf"
    if ext in {".docx", ".doc"}:
        return "docx"
    if ext in {".db", ".sqlite", ".sqlite3"}:
        return "database"
    if ext == ".json":
        return "other"
    if rel.startswith(".git/"):
        return "other"
    return "other"


def parse_status_for(origin: str, kind: str, hint: str) -> str:
    if hint == "technical":
        return "有意排除"
    if origin == "AI_DRAFT":
        return "有意排除"
    if kind in {"md", "txt"}:
        return "已提取"
    if kind == "image" or kind == "pdf":
        return "需 OCR"
    if kind in {"audio", "video"}:
        return "需 OCR"
    return "非文本"


def read_text(path: Path) -> str | None:
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return None


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, min(len(lines), 400)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    meta: dict = {}
    current_key = None
    current_list = None
    for line in lines[1:end]:
        if not line.strip():
            continue
        if line.startswith("  - ") or line.startswith("- "):
            item = line.split("-", 1)[1].strip().strip("'\"")
            if current_key is not None:
                if current_list is None:
                    current_list = []
                    meta[current_key] = current_list
                current_list.append(item)
            continue
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            current_key = key.strip()
            value = value.strip().strip("'\"")
            current_list = None
            if value:
                meta[current_key] = value
            else:
                meta[current_key] = ""
    body = "\n".join(lines[end + 1 :])
    return meta, body


def headings(body: str, limit: int = 8) -> list[str]:
    found = []
    for line in body.splitlines():
        if line.startswith("#"):
            found.append(line.lstrip("#").strip()[:120])
            if len(found) >= limit:
                break
    return found


def self_test() -> None:
    cases = {
        "百万长文写作/章稿/a.md": "AI_DRAFT",
        "长篇创作/总提纲-百万字自传小说.md": "AI_DRAFT",
        "正式成文/第七章-茶.md": "AI_DRAFT",
        "项目管理/用户订正-2026-09-12-书名.md": "HUMAN_ORIGINAL",
        "高中/素材/同学回忆/x.md": "THIRD_PARTY",
        ".git/HEAD": "UNKNOWN",
        "私人资料/相册/a.jpg": "PRIMARY_RECORD",
        "私人资料/聊天/a.md": "MIXED",
        "高中/G2204/人物/同学/赵问竹.md": "MIXED",
        "问卷回收/某班.md": "THIRD_PARTY",
    }
    for rel, expected in cases.items():
        ext = Path(rel).suffix.lower()
        got, _hint = classify(rel, ext)
        if got != expected:
            raise SystemExit(f"classifier failed: {rel} -> {got}, expected {expected}")


def init_db(db_path: Path) -> sqlite3.Connection:
    if db_path.exists():
        db_path.unlink()
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute(
        """
        CREATE TABLE files (
            source_id TEXT PRIMARY KEY,
            relative_path TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            size INTEGER NOT NULL,
            mtime TEXT NOT NULL,
            extension TEXT NOT NULL,
            kind TEXT NOT NULL,
            origin_class TEXT NOT NULL,
            origin_hint TEXT NOT NULL,
            parse_status TEXT NOT NULL,
            sensitivity TEXT NOT NULL,
            hanzi INTEGER NOT NULL
        )
        """
    )
    con.execute(
        """
        CREATE VIRTUAL TABLE docs_fts USING fts5(
            source_id UNINDEXED,
            path,
            title,
            body
        )
        """
    )
    return con


def walk_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".trash"}]
        for name in filenames:
            yield Path(dirpath) / name


def audit() -> dict:
    self_test()
    PRIVATE.mkdir(parents=True, exist_ok=True)
    EDITORIAL.mkdir(parents=True, exist_ok=True)
    (STUDIO / "state").mkdir(parents=True, exist_ok=True)

    inventory_path = PRIVATE / "inventory.jsonl"
    receipts_path = PRIVATE / "read_receipts.jsonl"
    db_path = PRIVATE / "vault.db"
    con = init_db(db_path)

    by_top = Counter()
    by_ext = Counter()
    by_origin = Counter()
    by_kind = Counter()
    by_sensitivity = Counter()
    by_parse = Counter()
    bytes_by_top = Counter()
    hanzi_by_origin = Counter()
    files_by_origin = Counter()
    errors = []
    ai_paths = []
    unread_by_top_kind = Counter()
    life_md = 0
    life_hanzi = 0
    file_count = 0
    byte_count = 0
    started = now_iso()

    with inventory_path.open("w", encoding="utf-8") as inv, receipts_path.open(
        "w", encoding="utf-8"
    ) as rec:
        for path in walk_files(VAULT):
            rel = path.relative_to(VAULT).as_posix()
            ext = path.suffix.lower()
            top = rel.split("/", 1)[0]
            try:
                stat = path.stat()
                digest = sha256_file(path)
                size = stat.st_size
                mtime = datetime.fromtimestamp(stat.st_mtime).astimezone().isoformat(timespec="seconds")
                origin, hint = classify(rel, ext)
                sens = sensitivity_for(rel, path.name)
                kind = kind_for(ext, rel)
                status = parse_status_for(origin, kind, hint)
                sid = source_id_for(rel)
                hanzi = 0
                links: list[str] = []
                tags: list[str] = []
                aliases = []
                title = ""
                indexed = False
                text_hash = None
                coverage = "sha256-only"
                fail_reason = None

                indexable = (
                    kind in {"md", "txt"}
                    and origin != "AI_DRAFT"
                    and hint != "technical"
                    and size <= 2_000_000
                    and sens != "skip"
                )
                if origin == "AI_DRAFT" and kind in {"md", "txt"} and size <= 2_000_000:
                    text = read_text(path)
                    if text is not None:
                        hanzi = len(HANZI_RE.findall(text))
                        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
                        coverage = "hashed-and-counted-not-read"
                    else:
                        status = "技术受限"
                        fail_reason = "decode_failed"
                elif indexable:
                    text = read_text(path)
                    if text is None:
                        status = "技术受限"
                        fail_reason = "decode_failed"
                        coverage = "sha256-only"
                    else:
                        hanzi = len(HANZI_RE.findall(text))
                        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
                        meta, body = split_frontmatter(text) if kind == "md" else ({}, text)
                        title = str(meta.get("title") or "")
                        if not title:
                            hs = headings(body, 1)
                            title = hs[0] if hs else path.stem
                        raw_aliases = meta.get("aliases") or meta.get("alias") or []
                        if isinstance(raw_aliases, str):
                            aliases = [raw_aliases]
                        elif isinstance(raw_aliases, list):
                            aliases = [str(a) for a in raw_aliases][:40]
                        raw_tags = meta.get("tags") or []
                        if isinstance(raw_tags, str):
                            tags = [raw_tags]
                        elif isinstance(raw_tags, list):
                            tags = [str(t) for t in raw_tags][:40]
                        body_tags = TAG_RE.findall(body)
                        for tag in body_tags:
                            if tag not in tags and len(tags) < 40:
                                tags.append(tag)
                        links = []
                        seen = set()
                        for target in WIKILINK_RE.findall(text):
                            target = target.strip()
                            if target and target not in seen:
                                seen.add(target)
                                links.append(target)
                            if len(links) >= 200:
                                break
                        con.execute(
                            "INSERT INTO docs_fts(source_id, path, title, body) VALUES (?, ?, ?, ?)",
                            (sid, rel, title, text),
                        )
                        indexed = True
                        status = "已提取"
                        coverage = "full-text-indexed-not-close-read"
                        if top not in TECH_TOPS:
                            life_md += 1
                            life_hanzi += hanzi
                elif kind in {"image", "pdf", "audio", "video", "docx"} and hint != "technical":
                    unread_by_top_kind[f"{top}|{kind}"] += 1
                    coverage = "unprocessed-attachment"
                else:
                    coverage = "excluded-or-nontext"

                row = {
                    "source_id": sid,
                    "relative_path": rel,
                    "sha256": digest,
                    "size": size,
                    "mtime": mtime,
                    "extension": ext,
                    "kind": kind,
                    "origin_class": origin,
                    "origin_hint": hint,
                    "parse_status": status,
                    "sensitivity": sens,
                    "links": links if sens != "restricted" else [],
                    "link_count": len(links),
                    "tags": tags if sens != "restricted" else [],
                    "aliases": aliases if sens != "restricted" else [],
                    "hanzi": hanzi,
                    "read_receipt": {
                        "time": now_iso(),
                        "processor": PROCESSOR,
                        "coverage": coverage,
                        "text_sha256": text_hash,
                        "fts_indexed": indexed,
                        "fail_reason": fail_reason,
                    },
                }
                inv.write(json.dumps(row, ensure_ascii=False) + "\n")
                rec.write(
                    json.dumps(
                        {
                            "source_id": sid,
                            "relative_path": rel,
                            "sha256": digest,
                            "coverage": coverage,
                            "parse_status": status,
                            "processor": PROCESSOR,
                            "time": row["read_receipt"]["time"],
                            "fail_reason": fail_reason,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                con.execute(
                    """
                    INSERT INTO files VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        sid,
                        rel,
                        digest,
                        size,
                        mtime,
                        ext,
                        kind,
                        origin,
                        hint,
                        status,
                        sens,
                        hanzi,
                    ),
                )
                if origin == "AI_DRAFT":
                    ai_paths.append(rel)

                file_count += 1
                byte_count += size
                by_top[top] += 1
                bytes_by_top[top] += size
                by_ext[ext or "(none)"] += 1
                by_origin[origin] += 1
                by_kind[kind] += 1
                by_sensitivity[sens] += 1
                by_parse[status] += 1
                hanzi_by_origin[origin] += hanzi
                files_by_origin[origin] += 1
                if file_count % 500 == 0:
                    print(f"scanned {file_count}", file=sys.stderr)
            except Exception as exc:
                errors.append({"path": rel, "error": str(exc), "trace": traceback.format_exc()[-500:]})
                file_count += 1

    con.commit()
    con.close()
    ai_paths.sort()
    (EDITORIAL / "ai_draft_paths.txt").write_text("\n".join(ai_paths) + ("\n" if ai_paths else ""), encoding="utf-8")

    summary = {
        "processor": PROCESSOR,
        "started": started,
        "finished": now_iso(),
        "vault_file_count": file_count,
        "vault_byte_count": byte_count,
        "by_top": dict(by_top),
        "bytes_by_top": dict(bytes_by_top),
        "by_ext": dict(by_ext),
        "by_origin": dict(by_origin),
        "by_kind": dict(by_kind),
        "by_sensitivity": dict(by_sensitivity),
        "by_parse_status": dict(by_parse),
        "hanzi_by_origin": dict(hanzi_by_origin),
        "life_text_files_indexed": life_md,
        "life_text_hanzi_indexed": life_hanzi,
        "ai_draft_file_count": len(ai_paths),
        "error_count": len(errors),
        "errors": errors[:50],
        "unread_attachments": dict(unread_by_top_kind),
        "semantic_close_read": False,
        "note": "已提取 means full text entered the local FTS index. It does not mean close reading.",
    }
    (EDITORIAL / "scan_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps({
        "files": file_count,
        "bytes": byte_count,
        "errors": len(errors),
        "ai_drafts": len(ai_paths),
        "life_md": life_md,
        "life_hanzi": life_hanzi,
        "by_origin": dict(by_origin),
        "by_parse": dict(by_parse),
    }, ensure_ascii=False))
    return summary


if __name__ == "__main__":
    audit()
