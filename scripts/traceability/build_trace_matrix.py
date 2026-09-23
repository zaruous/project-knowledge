#!/usr/bin/env python3
from pathlib import Path
import re

# ID 접두어 단일 기준: framework/standards/naming.md
PREFIXES = [
    "REQ", "DEV", "SCR", "API", "IF", "DB", "TC", "BUG", "CR",
    "OBJ", "SUBJ", "CAND", "EVD", "CRIT", "MET", "EVAL", "ACT",
    "DEC", "DS",
]
ID_RE = re.compile(rf"^({'|'.join(PREFIXES)})-\d{{4}}$")


def top_level_keys(block: str):
    data = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith((" ", "-", "#")):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data


def parse_metadata(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore").replace("\r\n", "\n")
    if path.suffix in (".yml", ".yaml"):
        return top_level_keys(text)
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    return top_level_keys(text[4:end])


def main():
    root = Path("entities")
    rows = []
    for path in root.rglob("*"):
        if path.suffix not in (".md", ".yml", ".yaml"):
            continue
        meta = parse_metadata(path)
        if meta and ID_RE.match(meta.get("id", "")):
            rows.append((meta.get("id"), meta.get("type", ""), meta.get("status", ""), str(path)))
    print("id,type,status,path")
    for row in sorted(rows):
        print(",".join(row))

if __name__ == "__main__":
    main()
