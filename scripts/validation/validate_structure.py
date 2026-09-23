#!/usr/bin/env python3
from pathlib import Path
import re
import sys

REQUIRED = [
    # entry points / policy
    "README.md", "AGENTS.md", "CLAUDE.md",
    "_config/project.yml",
    # multi-LLM adapters
    "llm", "llm/providers/claude",
    ".claude/skills", ".claude/agents",
    "skills/project-knowledge-manager",
    # knowledge
    "wiki", "entities", "templates", "index", "scripts",
    "framework/concepts", "framework/workflows", "framework/standards",
    "entities/objectives", "entities/subjects", "entities/candidates",
    "entities/evidence", "entities/evaluations",
    # data
    "data/raw", "data/manifests", "data/normalized", "data/derived",
    "data/snapshots", "data/lineage",
    # evaluation / governance
    "evaluation/criteria", "evaluation/scorecards",
    "evaluation/checklists", "evaluation/quality-gates",
    "governance/adoption/candidates", "governance/adoption/adopted",
    "governance/adoption/rejected",
]

# 버전은 front matter로 관리한다 (framework/standards/metadata.md)
VERSIONED_NAME = re.compile(r"[-_.]v\d+(\.\d+)*$", re.IGNORECASE)
VERSION_SCAN_SKIP = {"data", "attachments", "archive", "output", "index", ".git", ".venv", "__pycache__"}


def versioned_names(root: Path):
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if rel.parts[0] in VERSION_SCAN_SKIP:
            continue
        stem = p.stem if p.is_file() else p.name
        if VERSIONED_NAME.search(stem):
            yield rel


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    missing = [p for p in REQUIRED if not (root / p).exists()]
    versioned = list(versioned_names(root))
    readme = root / "README.md"
    if readme.exists() and not re.match(r"---\r?\n(.*\r?\n)*?version:", readme.read_text(encoding="utf-8")):
        missing.append("README.md front matter `version`")
    if missing or versioned:
        if missing:
            print("MISSING")
            for p in missing:
                print(f" - {p}")
        if versioned:
            print("VERSION-SUFFIXED NAMES (use front matter version/changelog instead)")
            for p in versioned:
                print(f" - {p}")
        raise SystemExit(1)
    print(f"OK: {len(REQUIRED)} required paths present, no version-suffixed names")


if __name__ == "__main__":
    main()
