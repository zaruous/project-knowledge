#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
checks = []

proc = subprocess.run(
    [sys.executable, str(ROOT / "scripts/validation/validate_structure.py")],
    capture_output=True,
    text=True,
)
checks.append(("structure", proc.returncode == 0, proc.stdout.strip() or proc.stderr.strip()))

required_docs = [
    ROOT / "framework/concepts/evidence-model.md",
    ROOT / "framework/concepts/evaluation-model.md",
    ROOT / "governance/adoption/README.md",
    ROOT / "evaluation/scorecards/base-framework-scorecard.yml",
]
checks.append(("management_points", all(p.exists() for p in required_docs), "core management documents present"))

score = round(sum(1 for _, ok, _ in checks if ok) / len(checks) * 100)
for name, ok, msg in checks:
    print(f"{'PASS' if ok else 'FAIL'} {name}: {msg}")
print(f"SELF_CHECK_SCORE={score}")
sys.exit(0 if score == 100 else 1)
