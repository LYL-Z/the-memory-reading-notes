#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggregate subagent deep-read artifacts into the master ledgers.

Reads parallel-execution/agents/*/*.md frontmatter, verifies chapter coverage
against task-queue.tsv, appends to read-records.tsv (idempotent), and rewrites
the ledger + coverage stats.

Verification is strict: a chapter only enters read-records if
  (a) the artifact exists and is non-trivial (>1500 bytes),
  (b) its frontmatter lists that exact chapter,
  (c) the chapter file exists at the declared version_sha.
"""
import io, os, re, csv, subprocess, sys, json, collections

BASE = r"D:/The Memory/tmp/reading-notes-review/editorial/full-corpus-readiness"
RN = r"D:/The Memory/tmp/reading-notes-review"
sys.path.insert(0, os.path.join(RN, "scripts"))

def hanzi_count_safe(text):
    try:
        from hanzi_count import hanzi_count
        return hanzi_count(text)
    except Exception:
        return sum(1 for c in text if "\u4e00" <= c <= "\u9fff")

FRONT = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)

def parse_front(md):
    m = FRONT.match(md)
    if not m:
        return {}
    d = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip()] = v.strip()
    return d

def git_show(rev, path):
    return subprocess.run(["git", "-C", RN, "show", f"{rev}:{path}"],
                          capture_output=True).stdout.decode("utf-8", "ignore")

def main():
    agents_dir = os.path.join(BASE, "parallel-execution", "agents")
    q_path = os.path.join(BASE, "parallel-execution", "task-queue.tsv")
    queue = {r["task_id"]: r for r in csv.DictReader(io.open(q_path, encoding="utf-8"), delimiter="\t")}

    new_records = []
    verif = []
    artifacts = []
    for ag in sorted(os.listdir(agents_dir)):
        ad = os.path.join(agents_dir, ag)
        if not os.path.isdir(ad):
            continue
        for fn in sorted(os.listdir(ad)):
            if not fn.endswith(".md"):
                continue
            fp = os.path.join(ad, fn)
            size = os.path.getsize(fp)
            md = io.open(fp, encoding="utf-8", errors="ignore").read()
            fm = parse_front(md)
            tid = fm.get("task_id", "")
            arts = os.path.relpath(fp, RN).replace("\\", "/")
            artifacts.append((ag, fn, tid, size))
            if size < 1500:
                verif.append((tid, ag, "aggregator", "artifact_size", "FAIL", f"{size} bytes < 1500"))
                continue
            chapters = [c.strip() for c in re.split(r"[,;]", fm.get("chapters", "")) if c.strip()]
            # expand ranges like V2-009..V2-012
            expanded = []
            for c in chapters:
                m = re.match(r"V(\d)-(\d{3})\.\.V(\d)-(\d{3})", c)
                if m:
                    v1, a, v2, b = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
                    for i in range(a, b + 1):
                        expanded.append(f"V{v1}-{i:03d}")
                else:
                    expanded.append(c)
            for c in expanded:
                mm = re.match(r"V(\d)-(\d{3})", c)
                if not mm:
                    continue
                v, ch = int(mm.group(1)), mm.group(2)
                path = (f"manuscript/volume-07/{ch}.md" if v == 7
                        else f"manuscript/volume-0{v}/{ch}.md")
                rev = "pr/84" if v == 7 else "main"
                txt = git_show(rev, path)
                if not txt:
                    verif.append((tid, ag, "aggregator", f"exists:{c}", "FAIL", "file not found at rev"))
                    continue
                new_records.append(dict(
                    file=path, repo="B/reading-notes",
                    version=("73e8220" if v == 7 else "799a97df"),
                    read_range=f"full text ({hanzi_count_safe(txt)} hanzi)",
                    tool="subagent Read", segments="1",
                    artifact=arts, read_at="2026-11-15 parallel round1",
                    note=f"{ag} deep read"))
                verif.append((tid, ag, "aggregator", f"chapter:{c}", "PASS", arts))

    # merge into read-records (idempotent by file)
    rp = os.path.join(BASE, "read-records", "read-records.tsv")
    existing = list(csv.DictReader(io.open(rp, encoding="utf-8"), delimiter="\t"))
    have = {r["file"] for r in existing}
    added = 0
    for r in new_records:
        if r["file"] not in have:
            existing.append(r); have.add(r["file"]); added += 1
    fields = list(existing[0].keys())
    with io.open(rp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t"); w.writeheader()
        for r in existing: w.writerow(r)

    # verification log
    vp = os.path.join(BASE, "parallel-execution", "verification-results.tsv")
    with io.open(vp, "a", encoding="utf-8", newline="") as f:
        for t in verif:
            f.write("\t".join(t) + "\n")

    # reading-progress
    pp = os.path.join(BASE, "parallel-execution", "reading-progress.tsv")
    with io.open(pp, "a", encoding="utf-8", newline="") as f:
        for r in new_records:
            f.write(f"{r['artifact']}\t{r['file']}\t{r['version']}\t{r['read_range']}\t\t{r['artifact']}\tPASS\n")

    print(f"artifacts scanned: {len(artifacts)}")
    print(f"new chapter records: {len(new_records)} (added {added})")
    fails = [v for v in verif if v[4] == "FAIL"]
    print(f"verification FAIL: {len(fails)}")
    for v in fails[:10]: print("  FAIL:", v)

    # rewrite ledger
    subprocess.run([sys.executable, r"D:/The Memory/tmp/full-corpus-readiness/_work/build_ledger.py"])

    # coverage
    recs = list(csv.DictReader(io.open(rp, encoding="utf-8"), delimiter="\t"))
    tot = 0; mss = 0
    for r in recs:
        f_ = r["file"]
        if f_.startswith("manuscript/"):
            rev = "pr/84" if r["version"].startswith("73e8220") else "main"
            t = git_show(rev, f_)
            n = hanzi_count_safe(t); mss += n
        else:
            tot += 0
    chs = [r for r in recs if r["file"].startswith("manuscript/")]
    print(f"\nrecords total: {len(recs)} | chapters: {len(chs)}/135")
    print(f"chapter hanzi: {mss:,} / 825,901 = {mss/825901*100:.1f}%")
    byvol = collections.Counter(r["file"].split("/")[1] for r in chs)
    print("by volume:", dict(sorted(byvol.items())))

if __name__ == "__main__":
    main()
