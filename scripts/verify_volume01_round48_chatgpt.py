"""R48 ChatGPT-stage invariants; Kimi-stage receipt remains an immutable historic snapshot."""
from __future__ import annotations

import hashlib
import json
import re
import runpy
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R47 = "23ff2c949b7584ea11910937356bbf3a7053530d"
KIMI = "15a45ad3f14d8503654efb58c0f1e25a6dc53a21"
MINIMUM = 136641
EXPECTED = 136676
count = runpy.run_path(str(ROOT / "scripts/hanzi_count.py"))["hanzi_count"]


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True)


def texts_at(ref: str) -> dict[str, str]:
    return {f"{i:03}": git("show", f"{ref}:manuscript/volume-01/{i:03}.md") for i in range(1, 19)}


def ends(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip()][-2:]


def evaluation(text: str) -> str:
    start = text.index("> 刘佑林：")
    end = text.index("肯定会一鸣惊人！", start) + len("肯定会一鸣惊人！")
    return text[start:end]


current = {p.stem: p.read_text(encoding="utf-8") for p in sorted((ROOT / "manuscript/volume-01").glob("*.md"))}
assert len(current) == 18, "Expected exactly 18 manuscript chapters"
r47 = texts_at(R47)
kimi = texts_at(KIMI)
assert sum(map(count, r47.values())) == 136633
assert sum(map(count, kimi.values())) == MINIMUM
counts = {k: count(v) for k, v in current.items()}
total = sum(counts.values())
assert total == EXPECTED, f"Unexpected full-volume Hanzi total: {total}"
assert total >= MINIMUM

# Scope: 004 and 007 keep Kimi's changes; 014/015 revert to R47; 018 fixes one character.
for n in current:
    if n in ("014", "015"):
        assert current[n] == r47[n], f"{n} must equal R47 source for precise rollback"
    elif n == "018":
        target = kimi[n].replace("我在心里试了一遍“我喜欢赵问竹”。七个字，",
                                  "我在心里试了一遍“我喜欢赵问竹”。六个字，")
        assert target != kimi[n] and current[n] == target
    else:
        assert current[n] == kimi[n], f"Unplanned manuscript modification in {n}"

assert evaluation(current["011"]) == evaluation(r47["011"])
assert ends(current["018"]) == ends(r47["018"]) == [
    "她没有说“喜欢”，也没有说“不喜欢”。",
    "四个人都笑了。",
]
assert "“你喜欢赵问竹吗？”" in current["018"]
assert "“我喜欢你。”" in current["018"]
assert "我只在心里重复，嘴唇没有动。" in current["018"]
assert "喻翰东先看过没有改字的版本。" in current["017"]
assert "伍筱丹看见的是我改过的版本" in current["017"]
assert "赵问竹却一个版本也没看见" in current["017"]
assert "是不是同一个晚上，我至今记不准" in current["017"]
assert "先把二点零一减二，得到零点零一，再除以二，得到零点零零五" in current["007"]

# The Kimi-stage reading receipt is checked against Kimi's actual frozen SHA, never this revision.
receipt = json.loads((ROOT / "editorial/round48-kimi/read-receipt.json").read_text(encoding="utf-8"))
hashes = {f"{n}.md": hashlib.sha256(t.encode("utf-8")).hexdigest() for n, t in kimi.items()}
assert receipt["manuscript_sha256_normalized_lf"] == hashes
assert receipt["human_readers"] == 0

# Historical rule: every official commit since R47 stays non-decreasing.
subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", R47, "HEAD"], check=True)
last = 136633
for ref in git("rev-list", "--reverse", f"{R47}..HEAD").splitlines():
    now = sum(count(t) for t in texts_at(ref).values())
    assert now >= last, f"Official total decreased at commit {ref}: {last} -> {now}"
    last = now
assert last == total

status = json.loads((ROOT / "state/progress.json").read_text(encoding="utf-8"))
assert status["hanzi_total"] == total
assert status["round48_status"] == "CHATGPT_INTERNAL_REVIEW_AND_POLISH_COMPLETE_PENDING_AUTHOR"

print(json.dumps({
    "status": "PASS",
    "stage": "R48_CHATGPT_INTERNAL_REVIEW",
    "r47_hanzi": 136633,
    "kimi_hanzi": MINIMUM,
    "current_hanzi": total,
    "diff_from_kimi": total - MINIMUM,
    "protected_011_017_018": True,
    "k_read_receipt_matches_kimi_snapshot": True,
    "historical_non_decreasing": True,
    "human_readers": 0,
    "literary_frozen": False
}, ensure_ascii=False, indent=2))
