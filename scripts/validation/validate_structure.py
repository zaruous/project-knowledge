#!/usr/bin/env python3
"""저장소 구조와 레코드를 검증한다. 오류가 있으면 1로 끝나고, 경고만 있으면 통과한다."""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import knowledge  # noqa: E402

# 레지스트리에 등록된 유형의 저장 위치는 knowledge.missing_type_paths()가 따로 검사한다.
REQUIRED = [
    # entry points / policy
    "README.md", "AGENTS.md", "CLAUDE.md", "requirements.txt",
    "_config/project.yml", "_base/registry", "_base/templates",
    # multi-LLM adapters
    ".claude/skills", ".claude/agents", "skills/project-knowledge-manager",
    # knowledge
    "framework/concepts", "framework/workflows", "framework/standards",
    "wiki", "entities", "templates", "llm", "index", "scripts",
    # data
    "data/raw", "data/manifests", "data/normalized", "data/derived",
    # 템플릿 자체 점검·거버넌스 (3단계에서 _base/로 이동)
    "evaluation/scorecards", "evaluation/results", "evaluation/checklists", "evaluation/quality-gates",
    "governance/adoption/candidates", "governance/adoption/adopted", "governance/adoption/rejected",
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


def report(title, items):
    if items:
        print(title)
        for item in items:
            print(f" - {item}")


def main():
    knowledge.utf8_stdio()
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else knowledge.ROOT
    missing = [p for p in REQUIRED if not (root / p).exists()]
    readme = root / "README.md"
    if readme.exists() and not re.match(r"---\r?\n(.*\r?\n)*?version:", readme.read_text(encoding="utf-8")):
        missing.append("README.md front matter `version`")
    result = knowledge.validate(root)
    missing += knowledge.missing_type_paths(root, result.registry)
    versioned = [p.as_posix() for p in versioned_names(root)]

    report("MISSING", missing)
    report("VERSION-SUFFIXED NAMES (use front matter version/changelog instead)", versioned)
    report("ERRORS", result.errors)
    report("WARNINGS", result.warnings)
    if missing or versioned or result.errors:
        raise SystemExit(1)
    records = sum(1 for r in result.records if r.id)
    print(f"OK: {len(REQUIRED)} required paths, {len(result.registry.types)} registered types, "
          f"{records} records, {len(result.edges)} relations, {len(result.warnings)} warnings")


if __name__ == "__main__":
    main()
