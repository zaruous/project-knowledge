#!/usr/bin/env python3
"""_config/project.yml에 프로젝트 정보를 기록한다.

기존 파일의 다른 섹션과 값은 보존하고 넘겨받은 값만 갱신하므로 다시 실행해도 안전하다.
"""
import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--name", required=True)
    p.add_argument("--code", required=True)
    p.add_argument("--owner")
    p.add_argument("--root", default=str(ROOT), help="저장소 루트 (기본: 이 스크립트가 속한 저장소)")
    p.add_argument("--dry-run", action="store_true", help="파일을 쓰지 않고 결과만 출력")
    args = p.parse_args()

    path = Path(args.root) / "_config" / "project.yml"
    config = (yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else None) or {}
    project = config.setdefault("project", {})
    project.update(code=args.code, name=args.name)
    if args.owner:
        project["owner"] = args.owner
    for key, default in (("phase", "proposal"), ("status", "active"), ("owner", "TBD")):
        project.setdefault(key, default)

    text = yaml.safe_dump(config, allow_unicode=True, sort_keys=False)
    if args.dry_run:
        print(text, end="")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"initialized: {path}")


if __name__ == "__main__":
    main()
