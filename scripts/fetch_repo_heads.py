# -*- coding: utf-8 -*-
import json, base64, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "novelstudio-audit", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))

def text_file(repo, path):
    data = get(f"https://api.github.com/repos/{repo}/contents/{path}")
    raw = base64.b64decode(data["content"])
    return raw.decode("utf-8", errors="replace")

def head(s, n=80):
    lines = s.splitlines()
    return "\n".join(lines[:n])

pairs = [
    ("danjdewhurst/story-skills", "README.md"),
    ("danjdewhurst/story-skills", "package.json"),
    ("danjdewhurst/story-skills", "LICENSE"),
    ("kevboh/longform", "LICENSE.md"),
    ("kevboh/longform", "manifest.json"),
    ("brianpetro/obsidian-smart-connections", "LICENSE"),
    ("brianpetro/obsidian-smart-connections", "manifest.json"),
]
for repo, path in pairs:
    print("\n########", repo, path, "########")
    try:
        body = text_file(repo, path)
        print(head(body, 60 if path.endswith(".md") or path == "LICENSE" else 80))
    except Exception as e:
        print("ERR", type(e).__name__, e)
