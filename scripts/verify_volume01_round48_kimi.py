"""R48 machine-checkable text, history and receipt invariants; not a literary test."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = "23ff2c949b7584ea11910937356bbf3a7053530d"
FLOOR = 136633
counter = runpy.run_path(str(ROOT / "scripts/hanzi_count.py"))
count = counter["hanzi_count"]


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args]).decode("utf-8")


def texts_at(ref):
    return {f"{i:03}": git("show", f"{ref}:manuscript/volume-01/{i:03}.md") for i in range(1, 19)}


current = {p.stem: p.read_text(encoding="utf-8") for p in sorted((ROOT / "manuscript/volume-01").glob("*.md"))}
assert len(current) == 18
base = texts_at(BASE)
counts = {k: count(v) for k, v in current.items()}
base_counts = {k: count(v) for k, v in base.items()}
assert sum(base_counts.values()) == FLOOR
total = sum(counts.values())
assert total >= FLOOR
subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", BASE, "HEAD"], check=True)
history = [{"commit": BASE, "hanzi": FLOOR}]
for ref in git("rev-list", "--reverse", f"{BASE}..HEAD").splitlines():
    n = sum(count(v) for v in texts_at(ref).values())
    assert n >= history[-1]["hanzi"], f"Official version shrank: {ref}"
    history.append({"commit": ref, "hanzi": n})
assert total >= history[-1]["hanzi"], "Working manuscript is below last official version"

# Original evaluation and terminal lines are byte-identical to R47 after LF normalization.
def evaluation(text):
    start = text.index("> 刘佑林：")
    end = text.index("肯定会一鸣惊人！", start) + len("肯定会一鸣惊人！")
    return text[start:end]

assert evaluation(current["011"]) == evaluation(base["011"])
base_last = [line for line in base["018"].splitlines() if line.strip()][-2:]
current_last = [line for line in current["018"].splitlines() if line.strip()][-2:]
assert current_last == base_last == ["她没有说“喜欢”，也没有说“不喜欢”。", "四个人都笑了。"]
assert "我只在心里重复，嘴唇没有动。" in current["018"]
assert "“你喜欢赵问竹吗？”" in current["018"]
assert "“我喜欢你。”" in current["018"]
assert "喻翰东先看过没有改字的版本。" in current["017"]
assert "伍筱丹看见的是我改过的版本" in current["017"]
assert "赵问竹却一个版本也没看见" in current["017"]
assert "是不是同一个晚上，我至今记不准" in current["017"]

# Verify the E mathematics, not its historicity. |x-1|+|x-3|=a.
numeric_cases = []
for a in [Fraction(3), Fraction(201, 100)]:
    roots = [2 - a / 2, 2 + a / 2]
    for x in roots:
        assert abs(x - 1) + abs(x - 3) == a
    numeric_cases.append({"a": str(a), "roots": [str(x) for x in roots]})
for x in [Fraction(1), Fraction(3, 2), Fraction(2), Fraction(5, 2), Fraction(3)]:
    assert abs(x - 1) + abs(x - 3) == 2
for a in [Fraction(0), Fraction(1), Fraction(199, 100)]:
    sample = [Fraction(-10), Fraction(0), Fraction(1), Fraction(2), Fraction(3), Fraction(10)]
    assert all(abs(x - 1) + abs(x - 3) != a for x in sample)
assert "a＝3" in current["007"]
assert "先把二点零一减二，得到零点零一，再除以二，得到零点零零五" in current["007"]
assert "我先把二分之一写在旁边" not in current["007"]

receipt = json.loads((ROOT / "editorial/round48-kimi/read-receipt.json").read_text(encoding="utf-8"))
hashes = {f"{k}.md": hashlib.sha256(v.encode("utf-8")).hexdigest() for k, v in current.items()}
assert receipt["manuscript_sha256_normalized_lf"] == hashes, "Read receipt belongs to other text"
assert receipt["full_current_volume_cold_read_performed_this_round"] is True
assert receipt["independent_blind_human_read"] is False
assert receipt["human_readers"] == 0
assert receipt["chapters_read_sequentially_in_full"] == [f"{i:03}" for i in range(1, 19)]

result = {
    "round": 48,
    "base_commit": BASE,
    "base_hanzi": FLOOR,
    "chapter_count": len(current),
    "chapter_hanzi": counts,
    "chapter_delta_from_r47": {k: counts[k] - base_counts[k] for k in counts},
    "total_hanzi": total,
    "net_hanzi": total - FLOOR,
    "official_history": history,
    "all_official_versions_non_decreasing": True,
    "next_official_version_minimum": total,
    "protected_original_evaluation_equal": True,
    "protected_last_two_lines_equal": True,
    "protected_017_latest_author_version": True,
    "numeric_cases_checked": numeric_cases,
    "numeric_scope": "Fictional E example only; no historic exam or Mathematica program certified.",
    "manuscript_sha256_normalized_lf": hashes,
    "read_receipt_matches": True,
    "full_current_volume_cold_read_this_round": True,
    "independent_blind_human_read": False,
    "human_readers": 0,
    "literary_frozen": False,
    "main_merge_allowed": False,
    "source_vault_modified": False,
    "scope_note": "Machine invariants only; no literary-quality or human-reader certification."
}
out = ROOT / "editorial/round48-kimi/verification.json"
if "--check-only" not in sys.argv:
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({k: result[k] for k in [
    "round", "total_hanzi", "net_hanzi", "all_official_versions_non_decreasing",
    "protected_original_evaluation_equal", "protected_last_two_lines_equal",
    "read_receipt_matches", "full_current_volume_cold_read_this_round", "human_readers"
]}, ensure_ascii=False, indent=2))
