#!/usr/bin/env python3
"""저장소 구조와 레코드를 검증한다. 오류가 있으면 1로 끝나고, 경고만 있으면 통과한다.

필수 경로는 _base/manifest.yml의 required와, _config/project.yml에서 켠 모듈의 폴더다.
"""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import knowledge  # noqa: E402

# 버전은 front matter로 관리한다 (_base/framework/standards/metadata.md)
VERSIONED_NAME = re.compile(r"[-_.]v\d+(\.\d+)*$", re.IGNORECASE)
VERSION_SCAN_SKIP = {"data", "attachments", "archive", "output", "index", ".git", ".venv", "__pycache__"}
AGENTS_MARKERS = ("<!-- base:begin -->", "<!-- base:end -->", "<!-- project:begin -->", "<!-- project:end -->")


def versioned_names(root: Path):
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if rel.parts[0] in VERSION_SCAN_SKIP:
            continue
        stem = p.stem if p.is_file() else p.name
        if VERSIONED_NAME.search(stem):
            yield rel.as_posix()


def report(title, items):
    if items:
        print(title)
        for item in items:
            print(f" - {item}")


def main():
    knowledge.utf8_stdio()
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else knowledge.ROOT
    manifest = knowledge.load_manifest(root)
    project = knowledge.load_project(root)
    base = project.get("base") or {}
    role = base.get("role", "project")
    enabled = project.get("modules") or ["core"]
    errors, warnings = [], []

    unknown = [m for m in enabled if m not in (manifest.get("modules") or {})]
    errors += [f"_config/project.yml: manifest에 없는 모듈 '{m}'" for m in unknown]
    required = list(manifest.get("required", [])) + knowledge.module_dirs(manifest, enabled)
    profile = (manifest.get("profiles") or {}).get(project.get("profile") or "")
    if role == "project":
        if project.get("profile") and profile is None:
            errors.append(f"_config/project.yml: manifest에 없는 프로필 '{project.get('profile')}'")
        required += [f"wiki/{ph['dir']}" for ph in (profile or {}).get("phases", [])]
    missing = [p for p in dict.fromkeys(required) if not (root / p).exists()]

    readme = knowledge.read_meta(root / "README.md") if (root / "README.md").exists() else None
    if not readme or not readme.get("version"):
        missing.append("README.md front matter `version`")
    if role == "template":
        if readme and str(readme.get("version")) != str(manifest.get("version")):
            errors.append(f"README.md version {readme.get('version')}과 _base/manifest.yml version {manifest.get('version')}이 다르다")
    elif str(base.get("version")) != str(manifest.get("version")):
        warnings.append(f"_config/project.yml base.version {base.get('version')}이 설치된 base {manifest.get('version')}와 다르다 "
                        "(업그레이드했다면 base.version을 갱신한다)")
    agents = root / "AGENTS.md"
    if agents.exists():
        text = agents.read_text(encoding="utf-8")
        errors += [f"AGENTS.md: 블록 표시 {m}가 없다" for m in AGENTS_MARKERS if m not in text]

    result = knowledge.validate(root)
    errors += result.errors
    warnings += result.warnings
    missing += knowledge.missing_type_paths(root, result.registry, enabled)
    versioned = list(versioned_names(root))

    report("MISSING", sorted(set(missing)))
    report("VERSION-SUFFIXED NAMES (use front matter version/changelog instead)", versioned)
    report("ERRORS", errors)
    report("WARNINGS", warnings)
    if missing or versioned or errors:
        raise SystemExit(1)
    records = sum(1 for r in result.records if r.id)
    print(f"OK: {role}, modules {', '.join(enabled)}, {len(result.registry.types)} registered types, "
          f"{records} records, {len(result.edges)} relations, {len(warnings)} warnings")


if __name__ == "__main__":
    main()
