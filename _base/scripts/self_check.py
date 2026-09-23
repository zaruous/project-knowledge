#!/usr/bin/env python3
"""base 자체 점검: 구조 검증을 실행하고 핵심 관리 문서가 _base에 있는지 확인한다."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_DOCS = [
    "_base/manifest.yml",
    "_base/framework/concepts/evidence-model.md",
    "_base/framework/concepts/evaluation-model.md",
    "_base/self-check/base-framework-self-check.md",
    "_base/self-check/base-framework-scorecard.yml",
]


def main():
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    proc = subprocess.run([sys.executable, str(ROOT / "_base/scripts/validate.py"), str(root)],
                          capture_output=True, encoding="utf-8")
    checks = [
        ("structure", proc.returncode == 0, proc.stdout.strip() or proc.stderr.strip()),
        ("management_points", all((root / p).exists() for p in REQUIRED_DOCS), "core management documents present"),
    ]
    score = round(sum(1 for _, ok, _ in checks if ok) / len(checks) * 100)
    for name, ok, msg in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {msg}")
    print(f"SELF_CHECK_SCORE={score}")
    sys.exit(0 if score == 100 else 1)


if __name__ == "__main__":
    main()
