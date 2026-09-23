#!/usr/bin/env python3
import argparse
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--code", required=True)
    p.add_argument("--root", default=".")
    args = p.parse_args()
    path = Path(args.root) / "_config" / "project.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"project:\n  code: {args.code}\n  name: {args.name}\n  phase: proposal\n  status: active\n  owner: TBD\n",
        encoding="utf-8",
    )
    print(f"initialized: {path}")

if __name__ == "__main__":
    main()
