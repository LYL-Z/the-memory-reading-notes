"""R47 text/source-boundary invariants. This is not a literary or reader test."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
from contextlib import redirect_stdout
import hashlib
import io
import json
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = "a4f512e19d1ad763112086640504f5c37ee27160"
counter = runpy.run_path(str(ROOT / "scripts/hanzi_count.py"))
count, prose = counter["hanzi_count"], counter["prose_body"]


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args]).decode("utf-8")


def texts_at(ref):
    return {f"{i:03}": git("show", f"{ref}:manuscript/volume-01/{i:03}.md") for i in range(1, 19)}


# Retain the existing quote, final-line, same-word AB and manuscript hygiene checks.
with redirect_stdout(io.StringIO()):
    runpy.run_path(str(ROOT / "scripts/verify_volume01_round44_sol.py"))
inherited = json.loads((ROOT / "editorial/round44-sol/verification.json").read_text(encoding="utf-8"))
current = {p.stem: p.read_text(encoding="utf-8") for p in sorted((ROOT / "manuscript/volume-01").glob("*.md"))}
old = texts_at(BASE)
counts = {k: count(v) for k, v in current.items()}
old_counts = {k: count(v) for k, v in old.items()}
assert sum(old_counts.values()) == 136474
total = sum(counts.values())
assert total >= 136474

subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", BASE, "HEAD"], check=True)
history = [{"commit": BASE, "hanzi": 136474}]
for ref in git("rev-list", "--reverse", f"{BASE}..HEAD").splitlines():
    n = sum(count(v) for v in texts_at(ref).values())
    assert n >= history[-1]["hanzi"], f"Official version shrank: {ref}"
    history.append({"commit": ref, "hanzi": n})
assert total >= history[-1]["hanzi"], "Working manuscript is below last official version"

# Verify the invented numerical example, without treating it as a historic exam.
numeric_cases = []
for a in [Fraction(3), Fraction(201, 100)]:
    roots = [2 - a / 2, 2 + a / 2]
    for x in roots:
        assert abs(x - 1) + abs(x - 3) == a
    numeric_cases.append({"a": str(a), "roots": [str(x) for x in roots]})
for x in [Fraction(1), Fraction(2), Fraction(5, 2), Fraction(3)]:
    assert abs(x - 1) + abs(x - 3) == 2

hashes = {f"{k}.md": hashlib.sha256(v.encode("utf-8")).hexdigest() for k, v in current.items()}
receipt = json.loads((ROOT / "editorial/round47-sol/read-receipt.json").read_text(encoding="utf-8"))
assert receipt["reviewed_manuscript_sha256_normalized_lf"] == hashes, "Manual review receipt belongs to other text"
assert receipt["full_current_volume_cold_read_performed_this_round"] is False
assert receipt["human_readers"] == 0

assert "喻翰东先看过没有改字的版本。" in current["017"]
assert "伍筱丹看见的是我改过的版本" in current["017"]
assert "是不是同一个晚上，我至今记不准" in current["017"]
assert "后来我照旧会把答案递过去。" in current["007"]
assert "她需要的从来不是一本被人预先安排好的答案" not in current["007"]
assert "我只在心里重复，嘴唇没有动。" in current["018"]

# A bag of paragraphs removes exact moves from the gross-add/delete figures.
def paragraphs(texts):
    return Counter(p.strip() for s in texts.values() for p in prose(s).split("\n\n") if p.strip())


before, after = paragraphs(old), paragraphs(current)
added = sum(count(p) * n for p, n in (after - before).items())
deleted = sum(count(p) * n for p, n in (before - after).items())
assert added - deleted == total - 136474
result = {
    "round": 47,
    "base_commit": BASE,
    "base_hanzi": 136474,
    "chapter_count": len(current),
    "chapter_hanzi": counts,
    "chapter_delta_from_base": {k: counts[k] - old_counts[k] for k in counts},
    "total_hanzi": total,
    "net_hanzi": total - 136474,
    "official_history": history,
    "all_official_versions_non_decreasing": True,
    "next_official_version_minimum": total,
    "gross_added_paragraph_hanzi_excluding_exact_moves": added,
    "gross_deleted_paragraph_hanzi_excluding_exact_moves": deleted,
    "gross_note": "Whole changed paragraphs, not word-level edits or amounts of new source material. Exact moved paragraphs cancel.",
    "protected_original_evaluation_equal": inherited["protected_original_evaluation_equal"],
    "protected_last_two_lines_equal": inherited["protected_last_two_lines_equal"],
    "same_word_terminal_ab_equal": inherited["same_word_terminal_ab_equal"],
    "same_word_009_010_ab_equal": inherited["same_word_009_010_ab_equal"],
    "numeric_cases_checked": numeric_cases,
    "numeric_scope": "Fictional E example only. This is not verification of a historic exam or of the Mathematica program.",
    "manuscript_sha256_normalized_lf": hashes,
    "manual_context_receipt_matches": True,
    "new_full_volume_cold_read_this_round": False,
    "human_readers": 0,
    "literary_frozen": False,
    "main_merge_allowed": False,
    "source_vault_modified": False,
    "source_scope_note": "No source-vault write commands used; source HEAD and tracked status separately recorded. No full-vault new audit.",
}
if "--check-only" not in sys.argv:
    (ROOT / "editorial/round47-sol/verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({k: result[k] for k in ["round", "total_hanzi", "net_hanzi", "all_official_versions_non_decreasing", "protected_original_evaluation_equal", "protected_last_two_lines_equal", "manual_context_receipt_matches", "new_full_volume_cold_read_this_round", "human_readers"]}, ensure_ascii=False, indent=2))
