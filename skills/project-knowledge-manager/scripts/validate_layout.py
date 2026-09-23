#!/usr/bin/env python3
from pathlib import Path
import sys

REQUIRED = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "_config",
    "wiki",
    "entities",
    "data/raw",
    "data/manifests",
    "scripts",
    "llm",
    "llm/providers/claude",
    ".claude/skills",
    ".claude/agents",
    "index",
    "templates",
]

RAW_FORBIDDEN_HINTS = {"normalized", "derived", "processed", "cleaned"}


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    missing = [item for item in REQUIRED if not (root / item).exists()]
    issues = []

    raw = root / "data" / "raw"
    if raw.exists():
        for p in raw.rglob("*"):
            if p.is_file() and any(h in p.name.lower() for h in RAW_FORBIDDEN_HINTS):
                issues.append(f"raw filename suggests transformed data: {p.relative_to(root)}")

    if missing:
        print("Missing required paths:")
        for item in missing:
            print(f" - {item}")
    if issues:
        print("Policy warnings:")
        for item in issues:
            print(f" - {item}")

    if missing:
        return 1
    print("OK: repository layout is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
