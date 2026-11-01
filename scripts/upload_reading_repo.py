# -*- coding: utf-8 -*-
import base64
import json
import subprocess
import urllib.parse
from pathlib import Path

REPO = "LYL-Z/the-memory-reading-notes"
ROOT = Path(r"D:\The Memory\NovelStudio_Grok47")


def run(cmd, payload=None):
    return subprocess.run(
        cmd,
        input=None if payload is None else json.dumps(payload),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        cwd=ROOT,
        check=False,
    )


def gh(method, path, payload):
    proc = run(["gh", "api", "--method", method, path, "--input", "-"], payload)
    if proc.returncode != 0:
        raise SystemExit(f"{path}\n{(proc.stderr or proc.stdout or '').strip()}")
    return json.loads(proc.stdout) if (proc.stdout or "").strip() else {}


def exists(encoded):
    proc = run(["gh", "api", f"repos/{REPO}/contents/{encoded}?ref=main"])
    return proc.returncode == 0


files = subprocess.check_output(
    ["git", "-c", "core.quotepath=false", "ls-files"],
    cwd=ROOT,
    text=True,
    encoding="utf-8",
).splitlines()
uploaded = 0
for rel in files:
    if rel == "README.md":
        continue
    encoded = urllib.parse.quote(rel)
    if exists(encoded):
        print("skip", rel)
        continue
    raw = (ROOT / rel).read_bytes()
    gh(
        "PUT",
        f"repos/{REPO}/contents/{encoded}",
        {
            "message": f"Add {rel}",
            "content": base64.b64encode(raw).decode("ascii"),
            "branch": "main",
        },
    )
    uploaded += 1
    print("ok", rel)
print("uploaded", uploaded)
