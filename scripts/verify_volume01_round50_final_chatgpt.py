"""Independent R50 closure invariants, not a certificate of literary quality.

Run from any branch containing the final manuscript (including post-merge main).
Unlike Kimi's R50 receipt checker, this script expects the one additional
ChatGPT continuity repair in chapter 017 and does not alter older receipts.
"""

from pathlib import Path
import hashlib
import json
import runpy
import subprocess


ROOT = Path(__file__).resolve().parents[1]
R49 = "3881eb880c975ae06aa01455974a24f7391f3546"
KIMI = "81f9884cf37aca0b4a8667b733ea97c3c2463198"
FINAL_PR_HEAD = "8223712ec910ae85272e07bb6c983869b12e0718"
FINAL_HANZI = 136693
count = runpy.run_path(str(ROOT / "scripts/hanzi_count.py"))["hanzi_count"]


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True)


def at(ref):
    return {
        f"{n:03}": git("show", f"{ref}:manuscript/volume-01/{n:03}.md")
        for n in range(1, 19)
    }


def total(texts):
    return sum(count(body) for body in texts.values())


def original_evaluation(body):
    start = body.index("> 刘佑林：")
    end = body.index("肯定会一鸣惊人！", start) + len("肯定会一鸣惊人！")
    return body[start:end]


current = {
    p.stem: p.read_text(encoding="utf-8")
    for p in sorted((ROOT / "manuscript/volume-01").glob("*.md"))
}
assert set(current) == {f"{n:03}" for n in range(1, 19)}
kimi = at(KIMI)
r49 = at(R49)
assert total(r49) == 136685
assert total(kimi) == 136688
assert total(current) == FINAL_HANZI
assert current["017"] != kimi["017"]
assert all(current[k] == kimi[k] for k in current if k != "017")

before = "铃已经响了，课桌上的题等着我翻开，我先把那一行扫完，才肯把纸压进书里。"
after = "铃已经响了，课桌上的题等着我翻开，我却仍把那张纸攥在手里，生怕自己改漏了一个字。"
assert before in kimi["017"]
assert before not in current["017"]
assert after in current["017"]
assert kimi["017"].replace(before, after) == current["017"]
assert count(current["017"]) - count(kimi["017"]) == 5

assert original_evaluation(current["011"]) == original_evaluation(r49["011"])
assert [line for line in current["018"].splitlines() if line.strip()][-2:] == [
    "她没有说“喜欢”，也没有说“不喜欢”。", "四个人都笑了。"
]
for fragment in (
    "我只在心里重复，嘴唇没有动。",
    "“你喜欢赵问竹吗？”",
    "“我喜欢你。”",
):
    assert fragment in current["018"]
for fragment in (
    "喻翰东看过未改的“竹”。",
    "伍筱丹看见的是我改过的版本",
    "赵问竹却一个版本也没看见",
    "纸是在晚自习的教室里到我手上的。至于递纸和正式跳舞是不是同一个晚上，我至今记不准。",
):
    assert fragment in current["017"]
assert "灯下那点颜色到底是不是羞怯，我不知道" in current["013"]
assert "我已经读了一年多大学" in current["001"]
assert "研学和表演后来取消，期末也没能按原定时间举行" in current["003"]
assert current["016"] == r49["016"]

subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", KIMI, "HEAD"], check=True)
subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", FINAL_PR_HEAD, "HEAD"], check=True)
subprocess.run(["git", "-C", str(ROOT), "diff", "--check"], check=True)
# The independently developed architecture documents on main predate this
# integration PR and intentionally contain Markdown's two-space hard breaks.
# Checking KIMI..HEAD would falsely attribute those trailing spaces to this
# final editorial patch. Check the exact PR patch, plus later edits only to
# the files this integration owns. Report that distinction in the audit.
subprocess.run(["git", "-C", str(ROOT), "diff", f"{KIMI}..{FINAL_PR_HEAD}", "--check"], check=True)
subprocess.run([
    "git", "-C", str(ROOT), "diff", f"{FINAL_PR_HEAD}..HEAD", "--check", "--",
    "README.md", "state/progress.json", "state/next_actions.md",
    "manuscript/volume-01", "editorial/volume01-round50-chatgpt-final-ten-dimension-audit-2026-11-04.md",
    "editorial/volume01-final-canon-and-volume02-handoff-2026-11-04.md",
    "scripts/verify_volume01_round50_final_chatgpt.py",
], check=True)

history = [{"commit": KIMI, "hanzi": total(kimi)}]
for sha in git("rev-list", "--ancestry-path", "--reverse", f"{KIMI}..HEAD").splitlines():
    try:
        n = total(at(sha))
    except subprocess.CalledProcessError as exc:
        raise AssertionError(f"Manuscript missing at {sha}") from exc
    assert n >= history[-1]["hanzi"], f"Official text decreased at {sha}"
    history.append({"commit": sha, "hanzi": n})
assert total(current) >= history[-1]["hanzi"]

old_receipt = json.loads((ROOT / "editorial/round50-kimi/read-receipt.json").read_text(encoding="utf-8"))
old_hashes = {f"{k}.md": hashlib.sha256(v.encode("utf-8")).hexdigest() for k, v in kimi.items()}
assert old_receipt["current_manuscript_sha256_normalized_lf"] == old_hashes
assert old_receipt["human_readers"] == 0

print(json.dumps({
    "status": "PASS",
    "scope": "R50 final machine checks only",
    "chapter_count": 18,
    "r49_hanzi": total(r49),
    "kimi_r50_hanzi": total(kimi),
    "final_hanzi": total(current),
    "final_delta_from_kimi": 5,
    "official_chain_non_decreasing": True,
    "changed_manuscript_chapters_from_kimi": ["017"],
    "protected_evaluation_and_018_ending": True,
    "k_50_read_receipt_applies_to_original_kimi_snapshot_only": True,
    "human_cold_readers": 0,
    "current_manuscript_sha256": {
        f"{k}.md": hashlib.sha256(v.encode("utf-8")).hexdigest()
        for k, v in current.items()
    },
    "history": history,
}, ensure_ascii=False, indent=2))
