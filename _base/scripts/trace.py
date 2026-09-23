#!/usr/bin/env python3
"""레코드 추적 매트릭스를 CSV로 출력한다.

CSV는 stdout으로, 커버리지 요약·재평가 필요 목록·검증 오류는 stderr로 나간다.
관계는 레지스트리(_base/registry/relations.yml)를 따르며 역방향(incoming)은 계산한 값이다.
검증 오류가 있으면 1로 끝난다.
"""
from collections import defaultdict
import csv
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import knowledge  # noqa: E402


def note(text):
    print(f"# {text}", file=sys.stderr)


def main():
    knowledge.utf8_stdio()
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else knowledge.ROOT
    res = knowledge.validate(root)

    outgoing = defaultdict(list)
    for src, name, tgt in res.edges:
        outgoing[src.key].append(f"{name}={tgt.id}")
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["id", "type", "status", "path", "outgoing", "incoming"])
    for r in sorted((r for r in res.records if r.id), key=lambda r: r.id):
        incoming = [f"{inv}={key}" for inv, keys in sorted(res.inverse[r.id].items()) for key in keys]
        writer.writerow([r.id, r.type, r.meta.get("status", ""), r.path.as_posix(),
                         ";".join(outgoing[r.key]), ";".join(incoming)])

    reqs = [r for r in res.records if r.type == "requirement"]
    if reqs:
        implemented = [r for r in reqs if res.inverse[r.id]["implemented_by"]]
        verified = [r for r in reqs if res.inverse[r.id]["verified_by"] or any(
            res.inverse[dev]["verified_by"] for dev in res.inverse[r.id]["implemented_by"])]
        note(f"REQ → DEV 구현 {len(implemented)}/{len(reqs)}, REQ → TC 검증(기능 경유 포함) {len(verified)}/{len(reqs)}")
    for ev in (r for r in res.records if r.type == "evaluation" and not res.inverse[r.id]["superseded_by"]):
        for ref, pinned in (ev.meta.get("pinned") or {}).items():
            current = res.by_id.get(ref)
            if current and str(current.meta.get("version")) != str(pinned):
                note(f"재평가 필요: {ev.id}는 {ref} {pinned}을 썼지만 현재 {current.meta.get('version')}")
    for w in res.warnings:
        note(f"WARN {w}")
    for e in res.errors:
        note(f"ERROR {e}")
    if res.errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
