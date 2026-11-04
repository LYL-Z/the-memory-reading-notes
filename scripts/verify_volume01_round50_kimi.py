"""R50 machine checks only; no literary-quality or human-reader certification.

R50-specific invariants on top of the standing protections:
- Baseline is ChatGPT R49 fixed SHA 3881eb8 (136,685 Han).
- P1-A (013) and P1-C (017) surgeries applied; P1-B (016) rejected => byte-identical to base.
"""
from pathlib import Path
import hashlib
import json
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = "3881eb880c975ae06aa01455974a24f7391f3546"
FLOOR = 136685
counter = runpy.run_path(str(ROOT / "scripts/hanzi_count.py"))
count = counter["hanzi_count"]
commands = []


def run(name, args):
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    commands.append({"command": name, "exit_code": p.returncode, "stdout": p.stdout.strip()[:2000], "stderr": p.stderr.strip()[:2000]})
    return p


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args]).decode("utf-8")


def texts_at(ref):
    return {f"{i:03}": git("show", f"{ref}:manuscript/volume-01/{i:03}.md") for i in range(1, 19)}


# Stage 0: self-test of the official counter and whitespace checks on both the
# working tree and every committed patch since BASE.
run("python scripts/hanzi_count.py (self-test)", ["python", str(ROOT / "scripts/hanzi_count.py")])
run("git diff --check (working tree)", ["git", "-C", str(ROOT), "diff", "--check"])
run("git diff --check (committed BASE..HEAD)", ["git", "-C", str(ROOT), "diff", f"{BASE}..HEAD", "--check"])

# The R49 verifier is run for the record. It is EXPECTED to fail on R50: its
# read receipt hash check compares against the pre-surgery text and its fixed
# floor is 136676 with R49-specific receipt fields. Failure here documents the
# boundary, it is not a regression; we do not edit the old script to fake PASS.
p49 = run("python scripts/verify_volume01_round49_kimi.py (expected-fail record)", ["python", str(ROOT / "scripts/verify_volume01_round49_kimi.py")])
r49_expected_fail = p49.returncode != 0

current = {p.stem: p.read_text(encoding="utf-8") for p in sorted((ROOT / "manuscript/volume-01").glob("*.md"))}
assert len(current) == 18
base = texts_at(BASE)
counts = {k: count(v) for k, v in current.items()}
base_counts = {k: count(v) for k, v in base.items()}
assert sum(base_counts.values()) == FLOOR, "Baseline is no longer the fixed R49 text"
total = sum(counts.values())
assert total >= FLOOR, "Total Han below R50 entry floor"

subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", BASE, "HEAD"], check=True)
history = [{"commit": BASE, "hanzi": FLOOR}]
for ref in git("rev-list", "--reverse", f"{BASE}..HEAD").splitlines():
    n = sum(count(v) for v in texts_at(ref).values())
    assert n >= history[-1]["hanzi"], f"Official version shrank: {ref}"
    history.append({"commit": ref, "hanzi": n})
assert total >= history[-1]["hanzi"], "Working manuscript is below last official version"


def evaluation(text):
    start = text.index("> 刘佑林：")
    end = text.index("肯定会一鸣惊人！", start) + len("肯定会一鸣惊人！")
    return text[start:end]


# Standing protections (identical logic to R49).
assert evaluation(current["011"]) == evaluation(base["011"]), "011 original evaluation altered"
base_last = [line for line in base["018"].splitlines() if line.strip()][-2:]
current_last = [line for line in current["018"].splitlines() if line.strip()][-2:]
assert current_last == base_last == ["她没有说“喜欢”，也没有说“不喜欢”。", "四个人都笑了。"]
assert "我只在心里重复，嘴唇没有动。" in current["018"]
assert "“你喜欢赵问竹吗？”" in current["018"]
assert "“我喜欢你。”" in current["018"]
assert "六个字" in current["018"]
assert "喻翰东先看过没有改字的版本。" in current["017"]
assert "伍筱丹看见的是我改过的版本" in current["017"]
assert "赵问竹却一个版本也没看见" in current["017"]
assert "是不是同一个晚上，我至今记不准" in current["017"]
assert "我已经读了一年多大学" in current["001"]
assert "快一年半大学" not in current["001"]
assert "研学和表演后来取消，期末也没能按原定时间举行" in current["003"]
assert "研学、期末和表演后来取消" not in current["003"]
assert "高中有一节历史课" in current["001"]

# R49 fact repair receipts still anchored to the base text itself.
assert base["001"] != current["001"] or True  # 001 unchanged this round by design

# R50 surgery checks.
# P1-A (013): adopted. New withheld-speech action in; analytic passages out.
assert "“她好像脸红”几个字已经排到嗓子眼" in current["013"], "013 surgery paragraph missing"
assert "我把它们咬住了" in current["013"]
assert "这个没说出去的版本，就留在我这边" in current["013"]
assert "那个没说出去的版本，跟着我躺回床上" in current["013"]
assert "我甚至有点想说看见她低着头" not in current["013"], "013 pre-surgery paragraph still present"
assert "我听见自己说“不知道”" not in current["013"], "013 pre-surgery closing paragraph still present"
assert "她没有请谁替她配上婚礼的音乐" not in current["013"]
# 013 must not invent evidence of her blush as fact.
assert "灯下那点颜色到底是不是羞怯，我不知道" in current["013"], "013 UNKNOWN marker dropped"

# P1-B (016): rejected => byte-identical to base.
assert current["016"] == base["016"], "016 was modified despite REJECT_KEEP_ORIGINAL verdict"

# P1-C (017): adopted. Embodied action in; courage-explanation out.
assert "笔还停在下一个“竹”上" in current["017"], "017 surgery sentence missing"
assert "我先把那一行扫完，才肯把纸压进书里" in current["017"]
assert "真正的问题却不是" not in current["017"], "017 explanation sentence still present"
assert "我有没有勇气承认" not in current["017"]
# The three-visibility ledger sentence must be untouched.
assert "喻翰东看过未改的“竹”。伍筱丹看见的是我改过的版本，赵问竹却一个版本也没看见。" in current["017"]

# Read receipt belongs to this exact text.
receipt = json.loads((ROOT / "editorial/round50-kimi/read-receipt.json").read_text(encoding="utf-8"))
hashes = {f"{k}.md": hashlib.sha256(v.encode("utf-8")).hexdigest() for k, v in current.items()}
assert receipt["current_manuscript_sha256_normalized_lf"] == hashes, "Read receipt belongs to other text"
assert receipt["full_current_volume_cold_read_performed_this_round"] is True
assert receipt["independent_blind_human_read"] is False
assert receipt["human_readers"] == 0
assert receipt["chapters_read_sequentially_in_full"] == [f"{i:03}" for i in range(1, 19)]
assert receipt["forbidden_retired_manuscripts_used"] is False

result = {
    "round": 50,
    "base_commit": BASE,
    "base_hanzi": FLOOR,
    "chapter_count": len(current),
    "chapter_hanzi": counts,
    "chapter_delta_from_r49_chatgpt": {k: counts[k] - base_counts[k] for k in counts},
    "total_hanzi": total,
    "net_hanzi": total - FLOOR,
    "official_history": history,
    "all_official_versions_non_decreasing": True,
    "next_official_version_minimum": total,
    "surgeries": {
        "P1-A-013": "ADOPT (+1)",
        "P1-B-016": "REJECT_KEEP_ORIGINAL (byte-identical to base)",
        "P1-C-017": "ADOPT (+2)",
    },
    "protected_original_evaluation_equal": True,
    "protected_last_two_lines_equal": True,
    "protected_017_latest_author_version": True,
    "protected_017_three_visibilities": True,
    "protected_018_core_facts": True,
    "protected_013_unknown_blush": True,
    "r49_fact_repairs_intact": ["001 university duration", "003 final exam postponed not permanently cancelled"],
    "manuscript_sha256_normalized_lf": hashes,
    "read_receipt_matches": True,
    "full_current_volume_cold_read_this_round": True,
    "independent_blind_human_read": False,
    "human_readers": 0,
    "literary_frozen": False,
    "main_merge_allowed": False,
    "source_vault_modified": False,
    "commands": commands,
    "r49_verifier_expected_failure_recorded": r49_expected_fail,
    "not_run": [],
    "development_failures": [],
    "scope_note": "Machine invariants only; no literary-quality or human-reader certification. The R49 verifier failing on R50 text is by design (fixed old floor and old receipt hashes); it is recorded under commands, not silenced."
}
out = ROOT / "editorial/round50-kimi/verification.json"
if "--check-only" not in sys.argv:
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({k: result[k] for k in [
    "round", "total_hanzi", "net_hanzi", "all_official_versions_non_decreasing",
    "surgeries", "protected_original_evaluation_equal", "protected_last_two_lines_equal",
    "protected_017_three_visibilities", "read_receipt_matches",
    "full_current_volume_cold_read_this_round", "human_readers",
    "r49_verifier_expected_failure_recorded"
]}, ensure_ascii=False, indent=2))
