# -*- coding: utf-8 -*-
"""Upload listed studio files to the private reading repo.

New files are created. Files already on main are updated with their blob sha.
"""
import base64
import json
import subprocess
import sys
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


def main(paths):
    for rel in paths:
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f"missing {rel}")
        encoded = urllib.parse.quote(rel)
        probe = run(["gh", "api", f"repos/{REPO}/contents/{encoded}?ref=main"])
        payload = {
            "message": f"Update {rel}",
            "content": base64.b64encode(path.read_bytes()).decode("ascii"),
            "branch": "main",
        }
        if probe.returncode == 0:
            payload["sha"] = json.loads(probe.stdout)["sha"]
            payload["message"] = f"Revise {rel}"
        proc = run(
            ["gh", "api", "--method", "PUT", f"repos/{REPO}/contents/{encoded}", "--input", "-"],
            payload,
        )
        if proc.returncode != 0:
            raise SystemExit(f"{rel}\n{(proc.stderr or proc.stdout or '').strip()}")
        print("ok", rel)


if __name__ == "__main__":
    main(sys.argv[1:])
