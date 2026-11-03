"""R49 machine checks only; no literary-quality or human-reader certification."""
from pathlib import Path
import hashlib
import json
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = "7d03ec3636592ff27a301da250bd366fc380e063"
FLOOR = 136676
counter = runpy.run_path(str(ROOT / "scripts/hanzi_count.py"))
count = counter["hanzi_count"]
commands = [{
    "command": "python scripts/verify_volume01_round48_chatgpt.py（阶段0、修改前）",
    "exit_code": 0,
    "stdout": "{\"status\":\"PASS\",\"current_hanzi\":136676,\"protected_011_017_018\":true,\"historical_non_decreasing\":true}",
    "stderr": "",
    "note": "在R49正文修改前实际运行通过；不将修改后的136685误报到R48固定校验器。"
}]


def run(name, args):
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    commands.append({"command": name, "exit_code": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()})
    if p.returncode:
        raise RuntimeError(f"{name} failed: {p.stderr}")


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args]).decode("utf-8")


def texts_at(ref):
    return {f"{i:03}": git("show", f"{ref}:manuscript/volume-01/{i:03}.md") for i in range(1, 19)}


run("python scripts/hanzi_count.py (self-test)", ["python", str(ROOT / "scripts/hanzi_count.py")])
run("git diff --check", ["git", "-C", str(ROOT), "diff", "--check"])

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
assert "六个字" in current["018"]
assert "喻翰东先看过没有改字的版本。" in current["017"]
assert "伍筱丹看见的是我改过的版本" in current["017"]
assert "赵问竹却一个版本也没看见" in current["017"]
assert "是不是同一个晚上，我至今记不准" in current["017"]

assert "我已经读了一年多大学" in current["001"]
assert "快一年半大学" not in current["001"]
assert "研学和表演后来取消，期末也没能按原定时间举行" in current["003"]
assert "研学、期末和表演后来取消" not in current["003"]

receipt = json.loads((ROOT / "editorial/round49-kimi/read-receipt.json").read_text(encoding="utf-8"))
hashes = {f"{k}.md": hashlib.sha256(v.encode("utf-8")).hexdigest() for k, v in current.items()}
assert receipt["current_manuscript_sha256_normalized_lf"] == hashes, "Read receipt belongs to other text"
assert receipt["full_current_volume_cold_read_performed_this_round"] is True
assert receipt["independent_blind_human_read"] is False
assert receipt["human_readers"] == 0
assert receipt["chapters_read_sequentially_in_full"] == [f"{i:03}" for i in range(1, 19)]
assert receipt["forbidden_retired_manuscripts_used"] is False

result = {
    "round": 49,
    "base_commit": BASE,
    "base_hanzi": FLOOR,
    "chapter_count": len(current),
    "chapter_hanzi": counts,
    "chapter_delta_from_r48_chatgpt": {k: counts[k] - base_counts[k] for k in counts},
    "total_hanzi": total,
    "net_hanzi": total - FLOOR,
    "official_history": history,
    "all_official_versions_non_decreasing": True,
    "next_official_version_minimum": total,
    "protected_original_evaluation_equal": True,
    "protected_last_two_lines_equal": True,
    "protected_017_latest_author_version": True,
    "protected_018_core_facts": True,
    "r49_fact_repairs": ["001 university duration", "003 final exam postponed not permanently cancelled"],
    "manuscript_sha256_normalized_lf": hashes,
    "read_receipt_matches": True,
    "full_current_volume_cold_read_this_round": True,
    "independent_blind_human_read": False,
    "human_readers": 0,
    "literary_frozen": False,
    "main_merge_allowed": False,
    "source_vault_modified": False,
    "commands": commands,
    "not_run": [],
    "development_failures": [{
        "command": "R49脚本初稿在修改后重复调用R48固定校验器",
        "exit_code": 1,
        "cause": "R48校验器按设计只接受136676，R49正文已为136685；并非正文回退或保护项失败。",
        "resolution": "保留修改前阶段0的PASS记录，R49使用独立基线比较与保护校验，不把新字数误报到旧校验器。"
    }],
    "scope_note": "Machine invariants only; no literary-quality or human-reader certification."
}
out = ROOT / "editorial/round49-kimi/verification.json"
if "--check-only" not in sys.argv:
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({k: result[k] for k in [
    "round", "total_hanzi", "net_hanzi", "all_official_versions_non_decreasing",
    "protected_original_evaluation_equal", "protected_last_two_lines_equal",
    "read_receipt_matches", "full_current_volume_cold_read_this_round", "human_readers"
]}, ensure_ascii=False, indent=2))
