# -*- coding: utf-8 -*-
"""
F01 反例测试：检索器不得把影子树过期备份当成现行事实。

背景
----
事实仓 `The Memory/.workbuddy/.tools/backup_before_region_20260902/` 是 2026-09-02
区域重构前的过期备份（43 份 md，git 未跟踪且被 .gitignore 第 12 行 `/.workbuddy/` 屏蔽）。
其中 `高中/2025届/人物/学生/颜子杰.md` 保留 3 处未销账「待核」，而现行版只剩 2 处。

本测试构造一个最小检索器，验证三层防线：
  L1 白名单：只收 `git ls-files` 已跟踪的 md（影子树天然出局）
  L2 显式路径排除：任何路径以 `.workbuddy/` 开头即拒
  L3 版本对账：索引内文件必须与磁盘当前内容哈希一致（防止拿旧版本快照冒充现行）

反例对照：不做任何过滤的 os.walk 朴素检索，会把 43 份过期备份当现行事实。
"""
import hashlib
import os
import re
import subprocess
import sys

FACT_ROOT = r"D:/The Memory/The Memory"
SHADOW = ".workbuddy"
PRIVATE = ("私人资料/", "lover-best/")
TARGET_REL = "高中/2025届/人物/学生/颜子杰.md"
STALE_LINE = "地域范围: 【待核】"
# 未销账标记：只认值位标记，排除「待核项关闭」这类流程标题与销账记录
OPEN_RE = re.compile(r"【待核】|待核[。；]")

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("  PASS  " if ok else "  FAIL  ") + name + ("  |  " + detail if detail else ""))


def tracked_md():
    """L1 白名单：git 已跟踪的 md。"""
    out = subprocess.run(["git", "-C", FACT_ROOT, "ls-files", "-z"],
                         capture_output=True, check=True).stdout.decode("utf-8")
    return {p for p in out.split("\0") if p.lower().endswith(".md")}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]


def build_index():
    """白名单 + 显式排除 + 私密层拒读，返回 {rel: sha}。"""
    idx = {}
    for rel in tracked_md():
        if rel.startswith(SHADOW + "/") or rel.startswith(PRIVATE):
            continue
        p = os.path.join(FACT_ROOT, rel)
        if os.path.exists(p):
            idx[rel] = sha(p)
    return idx


def naive_walk():
    """反例：不设任何防线，全树 os.walk。"""
    hits = []
    for root, dirs, files in os.walk(FACT_ROOT):
        for f in files:
            if f.lower().endswith(".md"):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, FACT_ROOT).replace(os.sep, "/")
                try:
                    txt = open(p, encoding="utf-8", errors="replace").read()
                except OSError:
                    continue
                if "待核" in txt:
                    hits.append((rel, len(OPEN_RE.findall(txt))))
    return hits


def search(index, keyword="待核"):
    """在索引范围内检索，返回 [(rel, hit_lines)]。"""
    out = []
    for rel in index:
        txt = open(os.path.join(FACT_ROOT, rel), encoding="utf-8", errors="replace").read()
        if keyword in txt:
            out.append((rel, txt.splitlines()))
    return out


def main():
    print("=" * 78)
    print("F01 反例测试：影子树污染 / 白名单+版本过滤")
    print("=" * 78)
    print("事实仓: %s" % FACT_ROOT)
    print("影子树: %s/.tools/backup_before_region_20260902/" % SHADOW)

    shadow_dir = os.path.join(FACT_ROOT, SHADOW, ".tools", "backup_before_region_20260902")
    shadow_md = []
    for root, dirs, files in os.walk(shadow_dir):
        for f in files:
            if f.lower().endswith(".md"):
                shadow_md.append(os.path.relpath(os.path.join(root, f), FACT_ROOT).replace(os.sep, "/"))

    print("\n[1] 影子树规模")
    print("    备份 md 份数: %d" % len(shadow_md))
    check("影子树含 43 份过期备份", len(shadow_md) == 43, "实测 %d" % len(shadow_md))

    print("\n[2] 反例：朴素全树检索（不设防线）")
    naive = naive_walk()
    shadow_hits = [h for h in naive if h[0].startswith(SHADOW + "/")]
    print("    命中文件总数: %d，其中影子树: %d" % (len(naive), len(shadow_hits)))
    for rel, n in shadow_hits[:5]:
        print("      ! %s  （未销账待核 %d 处）" % (rel, n))
    check("朴素检索确实被影子树污染", len(shadow_hits) > 0, "%d 份影子文件命中" % len(shadow_hits))

    print("\n[3] 防线执行：白名单 + 路径排除 + 版本对账")
    idx = build_index()
    print("    索引内 md 数: %d" % len(idx))
    leaked = [r for r in idx if r.startswith(SHADOW + "/")]
    check("L1/L2 索引零影子树路径", leaked == [], "泄漏 %d" % len(leaked))
    priv = [r for r in idx if r.startswith(PRIVATE)]
    check("私密层未被索引", priv == [], "泄漏 %d" % len(priv))
    drift = [r for r, h in idx.items() if sha(os.path.join(FACT_ROOT, r)) != h]
    check("L3 索引哈希与磁盘一致", drift == [], "漂移 %d" % len(drift))

    print("\n[4] 关键反例：颜子杰.md 的「待核」状态")
    sh = os.path.join(FACT_ROOT, SHADOW, ".tools", "backup_before_region_20260902", TARGET_REL)
    cur = os.path.join(FACT_ROOT, TARGET_REL)
    sh_txt = open(sh, encoding="utf-8", errors="replace").read()
    cur_txt = open(cur, encoding="utf-8", errors="replace").read()
    sh_open = OPEN_RE.findall(sh_txt)
    cur_open = OPEN_RE.findall(cur_txt)
    print("    备份版未销账待核: %d 处 %s" % (len(sh_open), sh_open))
    print("    现行版未销账待核: %d 处 %s" % (len(cur_open), cur_open))
    check("备份版含 3 处待核（过期状态）", len(sh_open) == 3, str(sh_open))
    check("现行版已收敛到 2 处", len(cur_open) == 2, str(cur_open))
    check("过期断言『%s』只存在于影子树" % STALE_LINE,
          STALE_LINE in sh_txt and STALE_LINE not in cur_txt)

    print("\n[5] 检索结果纯净性")
    hits = search(idx)
    print("    过滤后命中文件: %d" % len(hits))
    bad = [r for r, _ in hits if r.startswith(SHADOW + "/")]
    check("检索结果不含任何影子树路径", bad == [], str(bad[:3]))
    stale_hits = [r for r, lines in hits if any(STALE_LINE in ln for ln in lines)]
    check("过滤后无过期断言回流", stale_hits == [], str(stale_hits[:3]))
    got = [r for r, _ in hits if r == TARGET_REL]
    check("现行版仍在检索范围内（未误杀）", got == [TARGET_REL])

    print("\n[6] 对照：若把影子树加入索引会怎样（仅模拟，不落盘）")
    fake = dict(idx)
    fake[SHADOW + "/.tools/backup_before_region_20260902/" + TARGET_REL] = sha(sh)
    fake_hits = [r for r, lines in search(fake) if any(STALE_LINE in ln for ln in lines)]
    print("    模拟索引命中过期断言: %s" % (fake_hits or "无"))
    check("一旦纳入影子树，过期断言立刻回流（证明防线必要）", len(fake_hits) > 0)

    ok = all(r[1] for r in results)
    print("\n" + "=" * 78)
    print("结果: %d/%d 通过 — %s" % (sum(1 for r in results if r[1]), len(results),
                                     "PASS" if ok else "FAIL"))
    print("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
