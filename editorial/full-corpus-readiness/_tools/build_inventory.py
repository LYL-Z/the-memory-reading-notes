#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a full-corpus inventory for the two repositories.

Read-only. Produces 01_repository-inventory.tsv and the ledger skeleton.
"""
import io, os, subprocess, hashlib, sys, csv

BASE = r"D:/The Memory"
OUT = r"D:/The Memory/tmp/reading-notes-review/editorial/full-corpus-readiness"
TM = os.path.join(BASE, "The Memory")           # repo A  the-memory
RN = os.path.join(BASE, "tmp", "reading-notes-review")  # repo B  the-memory-reading-notes

RN_MAIN = "799a97df7b72d5f8bfcc57868fef9815427e97de"   # origin/main
RN_V7 = "73e8220969b7fa0d0ad2a7e9b8bca9c05ffb1b32"     # PR#84 R9 (may differ; resolved dynamically)
TM_MAIN = "ef33c98d63b88283e840f5414db154eb9118c4e4"   # master

CHARACTERS = ["刘佑林","赵问竹","王麒皓","唐鑫宇","宋俊豪","刘弈帆","刘奕帆","阳隽豪","何舟","汪智文",
              "董佳好","钟康明","颜子杰","曾子沣","赵文邦","唐嘉睿","高泽聪","张天泽","刘桓彬","鞠佳恒",
              "王际翔","喻翰东","伍筱丹","向睿馨","夏恺宪","阳松","舒思宇","王麒睿","夏思成",
              "父亲","母亲","奶奶","外婆","外公","舅舅","小姑","李顺贤","李霞","杨革非","向雄海","邓智刚",
              "朱学良","何永中","何永红","刘必胜","何沛泽","郑森","李博涵","成澜","成龙"]

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True)
    return r.stdout.decode("utf-8", "ignore")

def git_ls(repo, rev):
    out = sh(["git", "-c", "core.quotepath=false", "ls-tree", "-r", "--long", rev], cwd=repo)
    rows = []
    for line in out.splitlines():
        if not line.strip():
            continue
        meta, path = line.split("\t", 1)
        parts = meta.split()
        mode, typ, sha, size = parts[0], parts[1], parts[2], parts[3]
        rows.append((path, sha, int(size) if size.isdigit() else 0, mode, typ))
    return rows

def categorize(repo_tag, path):
    p = path.replace("\\", "/")
    if repo_tag == "B":
        if p.startswith("manuscript/"):      return "NOVEL_TEXT"
        if p.startswith("outline/"):         return "STRUCTURE_PLAN"
        if p.startswith("editorial/fact_cards/"): return "SECONDARY_FACTCARD"
        if p.startswith("editorial/author-decisions/"): return "AUTHOR_RULING"
        if p.startswith("editorial/author-interviews/"): return "AUTHOR_INTERVIEW"
        if p.startswith("editorial/six-volume-integration/"): return "INTEGRATION_LEDGER"
        if p.startswith("editorial/volume07/"): return "EDITORIAL_REVIEW"
        if p.startswith("editorial/longform-architecture/"): return "STRUCTURE_PLAN"
        if p.startswith("editorial/style-and-influences/"): return "CRAFT_REFERENCE"
        if p.startswith("editorial/"):        return "EDITORIAL_REVIEW"
        if p.startswith("research/"):         return "SECONDARY_RESEARCH"
        if p.startswith("state/"):            return "STATE_LEDGER"
        if p.startswith("evidence/"):         return "EVIDENCE_NOTE"
        if p.startswith("work/"):             return "WORK_EXPERIMENT"
        if p.startswith("scripts/") or p.startswith("tools/"): return "TOOLING"
        if p.startswith(".cursor/") or p.startswith(".github/"): return "TOOLING"
        return "META"
    else:
        if p.startswith(".obsidian/") or p.startswith(".git"): return "META_CONFIG"
        if p.startswith("写作体系/"):          return "CREATIVE_STANDARD"
        if p.startswith("百万长文写作/") or p.startswith("长篇创作/"): return "LEGACY_DRAFT"
        if p.startswith("项目管理/"):          return "AUTHOR_RULING"
        if p.startswith("隐私/") or p.startswith("私人资料/"): return "PRIVATE_SOURCE"
        if p.startswith("问卷回收/"):          return "PRIMARY_SOURCE"
        if p.startswith("文化与审美/"):        return "AESTHETIC_SOURCE"
        if p.startswith("背景资料/"):          return "BACKGROUND_SOURCE"
        if p.startswith("人物关系/"):          return "RELATIONSHIP_SOURCE"
        if p.startswith("人物") and p.endswith(".md"): return "INDEX"
        if p.startswith("家庭/"):              return "PRIMARY_SOURCE"
        if p.startswith("高中/") or p.startswith("初中/") or p.startswith("小学/") or p.startswith("大学/"):
            if "/人物/" in p:                  return "PERSON_PAGE"
            return "PRIMARY_SOURCE"
        if p.startswith("正式成文/"):          return "PUBLIC_EXPORT"
        if p.startswith("公开脱敏资料/"):      return "PUBLIC_EXPORT"
        if p.startswith("知识库"):             return "INDEX"
        return "META"

def priority(cat, path):
    if cat in ("AUTHOR_RULING","AUTHOR_INTERVIEW"): return "P1_AUTHOR_RULING"
    if cat in ("PRIVATE_SOURCE",):                  return "P1_PRIVATE_SOURCE"
    if cat in ("PRIMARY_SOURCE","PERSON_PAGE","RELATIONSHIP_SOURCE","BACKGROUND_SOURCE"): return "P1_PRIMARY"
    if cat in ("NOVEL_TEXT",):                      return "P1_CANON_TEXT"
    if cat in ("CREATIVE_STANDARD","STRUCTURE_PLAN","CRAFT_REFERENCE"): return "P1_STANDARD"
    if cat in ("SECONDARY_FACTCARD","SECONDARY_RESEARCH","EDITORIAL_REVIEW","INTEGRATION_LEDGER"): return "P2_SECONDARY"
    if cat in ("AESTHETIC_SOURCE",):                return "P2_AESTHETIC"
    if cat in ("LEGACY_DRAFT",):                    return "P3_LEGACY_EXCLUDED"
    if cat in ("STATE_LEDGER","EVIDENCE_NOTE","WORK_EXPERIMENT"): return "P3_WORKING"
    if cat in ("INDEX",):                           return "P2_INDEX"
    if cat in ("TOOLING","META","META_CONFIG","PUBLIC_EXPORT"): return "P4_META"
    return "P3_WORKING"

def volumes(repo_tag, path, text_head):
    p = path.replace("\\", "/")
    vols = set()
    import re
    for m in re.finditer(r"volume-0([1-7])", p):
        vols.add(m.group(1))
    for m in re.finditer(r"第([一二三四五六七])部", text_head):
        vols.add(str("一二三四五六七".index(m.group(1)) + 1))
    for m in re.finditer(r"volume0([1-7])", p):
        vols.add(m.group(1))
    if repo_tag == "A":
        if p.startswith(("高中/",)): vols.add("2"); vols.add("3"); vols.add("4")
        if p.startswith(("初中/",)): vols.add("4")
        if p.startswith(("小学/",)): vols.add("2")
        if p.startswith(("大学/",)): vols.add("5"); vols.add("7")
        if p.startswith(("家庭/",)): vols.add("3")
    return ",".join(sorted(v for v in vols if v))

def characters(text_head):
    return ",".join([c for c in CHARACTERS if c in text_head][:6])

def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []

    # --- repo A ---
    for path, sha, size, mode, typ in git_ls(TM, TM_MAIN):
        if typ != "blob":
            continue
        full = os.path.join(TM, path)
        head = ""
        if path.lower().endswith((".md", ".txt", ".csv", ".json", ".tsv")):
            try:
                head = io.open(full, encoding="utf-8", errors="ignore").read(3000)
            except Exception:
                head = ""
        cat = categorize("A", path)
        rows.append(dict(repository="A/the-memory", relative_path=path,
                         source_location="local+remote", branch_or_commit="master@" + TM_MAIN[:8],
                         file_type=os.path.splitext(path)[1].lower().lstrip(".") or "none",
                         file_size=size, file_hash="gitblob:" + sha,
                         content_category=cat,
                         reading_status="UNREAD", reading_method="", reading_coverage="",
                         limitation="", related_volumes=volumes("A", path, head),
                         related_characters=characters(head),
                         source_priority=priority(cat, path)))

    # --- repo B main ---
    for path, sha, size, mode, typ in git_ls(RN, RN_MAIN):
        if typ != "blob":
            continue
        full = os.path.join(RN, path)
        head = ""
        if path.lower().endswith((".md", ".txt", ".csv", ".json", ".tsv")):
            try:
                head = io.open(full, encoding="utf-8", errors="ignore").read(3000)
            except Exception:
                head = ""
        cat = categorize("B", path)
        rows.append(dict(repository="B/reading-notes", relative_path=path,
                         source_location="local+remote", branch_or_commit="main@" + RN_MAIN[:8],
                         file_type=os.path.splitext(path)[1].lower().lstrip(".") or "none",
                         file_size=size, file_hash="gitblob:" + sha,
                         content_category=cat,
                         reading_status="UNREAD", reading_method="", reading_coverage="",
                         limitation="", related_volumes=volumes("B", path, head),
                         related_characters=characters(head),
                         source_priority=priority(cat, path)))

    # --- repo B PR#84 additions ---
    v7 = sh(["git", "rev-parse", "pr/84"], cwd=RN).strip()
    added = [l.split("\t")[1] for l in sh(["git", "-c", "core.quotepath=false", "diff", "--name-status",
                                           RN_MAIN, "pr/84"], cwd=RN).splitlines() if l.startswith("A\t")]
    main_paths = set(r["relative_path"] for r in rows if r["repository"] == "B/reading-notes")
    for path in added:
        if path in main_paths:
            continue
        out = subprocess.run(["git", "show", f"pr/84:{path}"], cwd=RN, capture_output=True).stdout
        try:
            head = out.decode("utf-8", "ignore")[:3000]
        except Exception:
            head = ""
        cat = categorize("B", path)
        rows.append(dict(repository="B/reading-notes", relative_path=path,
                         source_location="local+remote", branch_or_commit="PR#84@" + v7[:8],
                         file_type=os.path.splitext(path)[1].lower().lstrip(".") or "none",
                         file_size=len(out), file_hash="gitblob:" + subprocess.run(
                             ["git", "rev-parse", f"pr/84:{path}"], cwd=RN, capture_output=True).stdout.decode().strip(),
                         content_category=cat,
                         reading_status="UNREAD", reading_method="", reading_coverage="",
                         limitation="unmerged_draft", related_volumes=volumes("B", path, head) or "7",
                         related_characters=characters(head),
                         source_priority=priority(cat, path)))

    # --- repo A private layer (gitignored, local only) ---
    priv_root = os.path.join(TM, "私人资料")
    if os.path.isdir(priv_root):
        for dirpath, dirnames, filenames in os.walk(priv_root):
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, TM).replace("\\", "/")
                try:
                    size = os.path.getsize(full)
                except OSError:
                    size = 0
                ext = os.path.splitext(fn)[1].lower().lstrip(".")
                head = ""
                if ext in ("md", "txt", "csv", "json"):
                    try:
                        head = io.open(full, encoding="utf-8", errors="ignore").read(3000)
                    except Exception:
                        head = ""
                cat = "PRIVATE_SOURCE"
                rows.append(dict(repository="A/the-memory", relative_path="REDACTED/"+ext or "REDACTED/none",
                                 source_location="local_only", branch_or_commit="gitignored/local",
                                 file_type=ext or "none", file_size=size,
                                 file_hash="local-only",
                                 content_category=cat,
                                 reading_status="UNREAD", reading_method="", reading_coverage="",
                                 limitation="gitignored_private_layer;not_in_public_repo",
                                 related_volumes="REDACTED",
                                 related_characters="REDACTED",
                                 source_priority="P1_PRIVATE_SOURCE"))

    fields = ["repository","relative_path","source_location","branch_or_commit","file_type","file_size",
              "file_hash","content_category","reading_status","reading_method","reading_coverage",
              "limitation","related_volumes","related_characters","source_priority"]
    p1 = os.path.join(OUT, "01_repository-inventory.tsv")
    with io.open(p1, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("inventory rows:", len(rows), "->", p1)

    import collections
    c = collections.Counter((r["repository"], r["content_category"]) for r in rows)
    for k, v in sorted(c.items(), key=lambda x: -x[1]):
        print(f"{v:6d}  {k[0]:20s}  {k[1]}")

if __name__ == "__main__":
    main()
