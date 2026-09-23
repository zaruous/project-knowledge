#!/usr/bin/env python3
"""저장소 구조와 레코드를 검증한다. 오류가 있으면 1로 끝나고, 경고만 있으면 통과한다.

필수 경로는 _base/manifest.yml의 required와, _config/project.yml에서 켠 모듈의 폴더다.
"""
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import knowledge  # noqa: E402

# 버전은 front matter로 관리한다 (_base/framework/standards/metadata.md)
VERSIONED_NAME = re.compile(r"[-_.]v\d+(\.\d+)*$", re.IGNORECASE)
VERSION_SCAN_SKIP = {"data", "attachments", "archive", "output", "index", ".git", ".venv", "__pycache__"}
VERSION_HEADING = re.compile(r"^#{1,6}\s.*(?<![\w.])v\d+(\.\d+)*(?![\w.])", re.M | re.I)
PAYLOAD_AREAS = ("data/incoming/", "data/raw/", "data/staging/", "data/normalized/", "data/derived/",
                 "attachments/", "output/", "index/")
SNAPSHOT_PAYLOAD = re.compile(r"data/snapshots/([^/]+)/payload/")
DATASET_PAYLOAD = re.compile(r"data/(?:raw|staging|normalized|derived)/(DS-\d{4})/")  # 데이터는 <단계>/<DS-ID>/ 아래에 둔다
AGENTS_MARKERS = ("<!-- base:begin -->", "<!-- base:end -->", "<!-- project:begin -->", "<!-- project:end -->")


def versioned_names(root: Path):
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if rel.parts[0] in VERSION_SCAN_SKIP:
            continue
        stem = p.stem if p.is_file() else p.name
        if VERSIONED_NAME.search(stem):
            yield rel.as_posix()


def version_headings(root: Path):
    for p in root.rglob("*.md"):
        rel = p.relative_to(root)
        if rel.parts[0] in VERSION_SCAN_SKIP:
            continue
        for m in VERSION_HEADING.finditer(p.read_text(encoding="utf-8", errors="ignore")):
            yield f"{rel.as_posix()}: '{m.group(0).strip()}' (버전은 front matter changelog로 관리한다)"


def payload_problems(root: Path, by_id):
    """Git에 올라가는(추적 중이거나 무시되지 않은) payload가 보안 정책을 지키는지 검사한다. git 저장소가 아니면 건너뛴다."""
    policy = knowledge.load_yaml(root / "_config/security-policy.yml") if (root / "_config/security-policy.yml").exists() else {}
    rule = policy.get("git_payload")
    if not rule:
        return []
    try:
        proc = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                              capture_output=True)
    except OSError:
        return []
    if proc.returncode != 0:
        return []
    max_mb = float(rule.get("max_file_mb", 5))
    allowed = set(rule.get("allowed_classifications") or [])
    problems = []
    for rel in filter(None, proc.stdout.decode("utf-8").split("\0")):
        snap = SNAPSHOT_PAYLOAD.match(rel)
        path = root / rel
        if not (rel.startswith(PAYLOAD_AREAS) or snap) or path.name == ".gitkeep" or not path.is_file():
            continue
        if path.stat().st_size > max_mb * 1024 * 1024:
            problems.append(f"{rel}: Git에 올리는 payload가 {max_mb:g}MB를 넘는다 (_config/security-policy.yml git_payload)")
        owner = DATASET_PAYLOAD.match(rel)
        if snap:
            record = by_id.get(snap.group(1))
            datasets = knowledge.values(record.meta, "datasets") if record else []
        else:
            datasets = [owner.group(1)] if owner else []
        for ds in datasets:
            dataset = by_id.get(ds)
            level = ((dataset.meta.get("security") or {}).get("classification")) if dataset else None
            if level not in allowed:
                problems.append(f"{rel}: 데이터셋 {ds}의 보안 등급 '{level}'은 Git에 둘 수 없다 (허용: {', '.join(sorted(allowed))})")
    return problems


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
    errors += result.errors + payload_problems(root, result.by_id)
    warnings += result.warnings + list(version_headings(root))
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
