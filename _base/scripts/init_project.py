#!/usr/bin/env python3
"""새 프로젝트를 초기화한다. GitHub "Use this template"으로 만든 저장소 루트에서 실행한다.

- _config/project.yml에 프로젝트 정보, 프로필, 모듈, base 버전을 기록한다 (다른 설정은 보존)
- 켠 모듈의 폴더와 프로필의 wiki 단계 폴더·README를 만든다 (이미 있으면 건드리지 않는다)
- 템플릿에서 처음 초기화할 때만 README.md를 프로젝트용으로 바꾸고 템플릿 전용 경로를 정리한다

다시 실행하면 빠진 폴더만 추가하므로 모듈을 나중에 켤 때도 쓴다 (예: --modules +monitor).
--dry-run은 할 일만 출력한다.
"""
import argparse
from datetime import date
import json
from pathlib import Path
import shutil
from string import Template
import subprocess
import sys

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import knowledge  # noqa: E402


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def resolve_modules(manifest, base_modules, spec):
    """'+monitor,-dev'는 기본 모듈에 더하고 빼며, 'core,dev,eval'은 그대로 쓴다. core는 항상 켠다."""
    modules = manifest["modules"]
    tokens = [t.strip() for t in (spec or "").split(",") if t.strip()]
    signed = [t[0] in "+-" for t in tokens]
    if any(signed) and not all(signed):
        fail("--modules에 모듈 이름과 +/- 표기를 섞어 쓸 수 없다")
    if tokens and all(signed):
        chosen = list(base_modules)
        for t in tokens:
            if t[0] == "+" and t[1:] not in chosen:
                chosen.append(t[1:])
            elif t[0] == "-" and t[1:] in chosen:
                chosen.remove(t[1:])
    else:
        chosen = tokens or list(base_modules)
    if "core" not in chosen:
        chosen.insert(0, "core")
    for name in chosen:
        if name not in modules:
            available = ", ".join(n for n, m in modules.items() if not m.get("template_only"))
            fail(f"알 수 없는 모듈 '{name}' (가능: {available})")
        if modules[name].get("template_only"):
            fail(f"'{name}'은 템플릿 저장소 전용 모듈이라 프로젝트에서 켤 수 없다")
    order = list(modules)
    return sorted(dict.fromkeys(chosen), key=order.index)


def is_template_origin(root, slug):
    try:
        url = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"],
                             capture_output=True, encoding="utf-8").stdout
    except OSError:
        return False
    return bool(slug) and slug.lower() in url.lower()


def phase_readme(phase):
    items = "\n".join(f"- {d}" for d in phase["deliverables"])
    return (f"# {phase['dir']} {phase['name']}\n\n{phase['purpose']}\n\n"
            f"## 필수 산출물\n{items}\n\n"
            "산출물은 DLV 엔티티(`entities/deliverables/`)로 등록해 승인 이력을 남기고, 이 폴더에는 단계 문서를 둔다.\n\n"
            f"## 게이트\n- {phase['gate']}: 게이트 시점에 `_base/templates/wiki/gate-review.md`로 검토 문서를 만든다.\n")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def make_dir(path):
    path.mkdir(parents=True, exist_ok=True)
    (path / ".gitkeep").touch()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--name", required=True)
    p.add_argument("--code", required=True)
    p.add_argument("--owner")
    p.add_argument("--profile", help="development | evaluation (처음 초기화할 때 기본값 development)")
    p.add_argument("--modules", help="예: +monitor,+rag 또는 core,dev,eval")
    p.add_argument("--root", default=str(knowledge.ROOT), help="저장소 루트 (기본: 이 스크립트가 속한 저장소)")
    p.add_argument("--dry-run", action="store_true", help="파일을 바꾸지 않고 할 일만 출력")
    p.add_argument("--force", action="store_true", help="템플릿 저장소 자체에서도 실행한다 (템플릿 전용 경로가 삭제된다)")
    args = p.parse_args()
    knowledge.utf8_stdio()

    root = Path(args.root)
    manifest = knowledge.load_manifest(root)
    if not manifest:
        fail("_base/manifest.yml이 없다")
    config = knowledge.load_project(root)
    base = config.setdefault("base", {})
    first = base.get("role") == "template"
    if first and not args.force and is_template_origin(root, manifest.get("template_repository")):
        fail("이 저장소는 템플릿 저장소다. GitHub의 'Use this template'으로 새 저장소를 만든 뒤 그 저장소에서 실행한다")

    profiles = manifest["profiles"]
    current = None if first else config.get("profile")
    if args.profile and current and args.profile != current:
        fail(f"프로필은 바꿀 수 없다 (현재 {current}). 단계 폴더 구성이 달라지기 때문이다")
    profile_name = current or args.profile or "development"
    if profile_name not in profiles:
        fail(f"알 수 없는 프로필 '{profile_name}' (가능: {', '.join(profiles)})")
    profile = profiles[profile_name]
    modules = resolve_modules(manifest, profile["modules"] if first else (config.get("modules") or profile["modules"]),
                              args.modules)

    today = date.today().isoformat()
    project = config.setdefault("project", {})
    project.update(code=args.code, name=args.name)
    if args.owner:
        project["owner"] = args.owner
    if not project.get("phase"):
        project["phase"] = profile["phases"][0]["dir"]
    project.setdefault("status", "active")
    project.setdefault("owner", "TBD")
    config["profile"] = profile_name
    config["modules"] = modules
    if first:
        base.update(role="project", version=manifest.get("version"),
                    source=manifest.get("template_repository"), bootstrapped_at=today)

    actions = []
    for d in knowledge.module_dirs(manifest, modules):
        if not (root / d).exists():
            actions.append((f"mkdir {d}/", lambda d=d: make_dir(root / d)))
    for ph in profile["phases"]:
        readme = root / "wiki" / ph["dir"] / "README.md"
        if not readme.exists():
            actions.append((f"write wiki/{ph['dir']}/README.md", lambda r=readme, ph=ph: write(r, phase_readme(ph))))
    if first:
        seed = (root / "_base/seeds/README.md").read_text(encoding="utf-8")
        text = Template(seed).safe_substitute(
            name=args.name, code=args.code, profile=profile_name, modules=", ".join(modules),
            base_version=manifest.get("version"), date=today,
            phases="\n".join(f"  - `wiki/{ph['dir']}/` {ph['name']}" for ph in profile["phases"]))
        # front matter의 title은 YAML 문자열로 감싼다 (이름에 ':' 등이 있어도 깨지지 않게)
        text = text.replace(f"title: {args.name}\n", f"title: {json.dumps(args.name, ensure_ascii=False)}\n", 1)
        actions.append(("replace README.md (project seed)", lambda: write(root / "README.md", text)))
        template_only = sorted({Path(d).parts[0] for m in manifest["modules"].values() if m.get("template_only")
                                for d in m.get("dirs", [])})
        for top in template_only:
            if (root / top).exists():
                actions.append((f"remove {top}/ (template only)", lambda top=top: shutil.rmtree(root / top)))
    config_path = root / knowledge.PROJECT_CONFIG
    new_config = yaml.safe_dump(config, allow_unicode=True, sort_keys=False)
    if not config_path.exists() or config_path.read_text(encoding="utf-8") != new_config:
        actions.append((f"write {knowledge.PROJECT_CONFIG.as_posix()}", lambda: write(config_path, new_config)))

    if not actions:
        print("변경 없음: 이미 초기화되어 있다")
        return
    for desc, run in actions:
        print(("[dry-run] " if args.dry_run else "") + desc)
        if not args.dry_run:
            run()
    if not args.dry_run:
        print(f"initialized: profile {profile_name}, modules {', '.join(modules)}, base {base.get('version')}")
        print("다음: python _base/scripts/validate.py")


if __name__ == "__main__":
    main()
