"""R44/R45文本完整性核验。阅读状态引用署名记录，脚本不证明阅读或文学效果。"""
from pathlib import Path
import collections
import difflib
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = "793e4b20400e62d0199c9b1ec9ec2ceafeb4afdc"
ns = {"__name__": "round44_counter"}
exec(compile((ROOT / "scripts/hanzi_count.py").read_text(encoding="utf-8"), "hanzi_count.py", "exec"), ns)
count, body = ns["hanzi_count"], ns["prose_body"]
paths = sorted((ROOT / "manuscript/volume-01").glob("*.md"))
assert [p.stem for p in paths] == [f"{i:03}" for i in range(1, 19)]
current = [p.read_text(encoding="utf-8") for p in paths]
old = [subprocess.check_output(["git", "-C", str(ROOT), "show", f"{BASE}:manuscript/volume-01/{i:03}.md"]).decode("utf-8") for i in range(1, 21)]
quoted = lambda s: "\n".join(l for l in s.splitlines() if l.startswith(">"))
last_two = lambda s: [l for l in s.splitlines() if l.strip()][-2:]
assert quoted(old[10]) == quoted(current[10]), "赵原始评价改变"
assert last_two(old[19]) == last_two(current[-1]), "末两句改变"
assert current[-1].startswith("# 历史课\n"), "目录等非正文误入终章"
assert re.findall(r"(?m)^## (.)$", current[-1]) == ["一", "二", "三"]
assert "我只在心里重复，嘴唇没有动。" in current[-1]
assert "她仍没有开口，我心里已经吵得一片。" in current[-1]
assert "他说一局救了我两三次" in current[0]
assert "低一年级的工程力学强基生" not in current[0]
assert "不同于上一回窗边" not in current[14]
assert "究竟是在我改字前还是改字后" in current[16]
assert "是不是同一个晚上，我至今记不准" in current[16]
assert "伍筱丹看见的是我改过的版本" in current[16]
for s in current:
    assert "# 第一部现行审阅目录" not in s
    assert "私人资料/" not in s and "![[" not in s
    paragraphs = [p.strip() for p in s.split("\n\n") if len(p.strip()) > 35]
    assert not [p for p, n in collections.Counter(paragraphs).items() if n > 1]
normalize = lambda s: re.sub(r"\s+", "", body(s))
ab = ROOT / "work/round44-structure-ab"
three = "\n\n".join((ab / "three-chapters" / f"{i:03}.md").read_text(encoding="utf-8") for i in [18, 19, 20])
assert normalize(three) == normalize(current[-1]), "终场同词对照已漂移"
assert normalize((ab / "009-010-one-chapter.md").read_text(encoding="utf-8")) == normalize(current[8] + "\n\n" + current[9])
counts = {p.stem: count(s) for p, s in zip(paths, current)}
hashes = {p.name: hashlib.sha256(s.encode("utf-8")).hexdigest() for p, s in zip(paths, current)}
receipt_path = ROOT / "editorial/round45-sol/read-receipt.json"
receipt = json.loads(receipt_path.read_text(encoding="utf-8")) if receipt_path.exists() else {}
read_current = bool(
    receipt.get("full_read_completed")
    and receipt.get("repair_contexts_reviewed")
    and receipt.get("reviewed_final_manuscript_hashes_normalized_lf") == hashes
)
total = sum(counts.values())
assert total >= 135731
paragraphs = lambda ss: [p.strip() for p in body("\n\n".join(ss)).split("\n\n") if p.strip()]
a, b = paragraphs(old), paragraphs(current)
added = deleted = 0
for op, i, j, k, l in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
    if op in ["replace", "delete"]:
        deleted += count("\n\n".join(a[i:j]))
    if op in ["replace", "insert"]:
        added += count("\n\n".join(b[k:l]))
assert added - deleted == total - 127508
result = {
    "base_commit": BASE,
    "chapter_count": len(paths),
    "chapter_hanzi": counts,
    "total_hanzi": total,
    "minimum": 135731,
    "margin": total - 135731,
    "r43_hanzi": 127508,
    "net_from_r43": total - 127508,
    "gross_paragraph_added_hanzi": added,
    "gross_paragraph_deleted_hanzi": deleted,
    "gross_note": "含整段重写，不是全部新增史料；全卷对齐避免将终场迁移虚计成新故事",
    "manuscript_sha256_normalized_lf": hashes,
    "hash_note": "UTF-8、LF换行的正文文件指纹；避免Windows检出CRLF使同文异哈希",
    "protected_original_evaluation_equal": True,
    "protected_last_two_lines_equal": True,
    "same_word_terminal_ab_equal": True,
    "same_word_009_010_ab_equal": True,
    "human_readers": 0,
    "full_new_continuous_cold_read_complete": read_current,
    "continuous_read_is_independent_blind": False,
    "continuous_read_source_commit": receipt.get("full_read_source_commit"),
    "reading_receipt": "editorial/round45-sol/read-receipt.json" if receipt else None,
    "reading_status_note": "阅读状态来自编辑署名记录与修后指纹匹配，不是脚本读文件即视为通读；整读R44候选后修16处，回读差异与上下文，未假称修后再全卷盲读。" if read_current else "尚无覆盖当前正文指纹的完整通读及修后回读记录。",
    "literary_frozen": False,
    "main_merge_allowed": False,
    "verification_scope": "R44候选18章按顺序全文阅读，修后回读16处差异及接缝、首尾；脚本核计数、指纹、保护引文与同词A/B。原库审查沿用前轮，不冒称此次重新全库审计；不是陌生真人效果。" if read_current else "核差异、场景与上下文、首尾、题理、计数与来源边界；完整阅读状态另查署名记录，不由脚本背书。",
}
(ROOT / "editorial/round44-sol/verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
