---
title: Claude Code Project Guide
type: agent-guide
status: active
version: 3.0.0-alpha.1
updated_at: 2026-09-23
changelog:
  - version: 3.0.0-alpha.1
    date: 2026-09-23
    changes:
      - "공통 규칙을 반복하지 않고 `@AGENTS.md`로 가져오도록 변경. 이 문서에는 Claude Code 전용 내용만 남김"
      - "Claude 사용 안내와 프롬프트 가이드를 `llm/providers/claude/`에서 `.claude/README.md`로 이동"
  - version: 2.1.0
    date: 2026-09-23
    changes:
      - "`Generic Base v2` section merged into `Repository model`, `Base framework rules`, and `Validation`"
      - "Validation now uses the single merged `scripts/validation/validate_structure.py` plus the self check"
      - "Added the front matter versioning rule"
  - version: 2.0.0
    date: 2026-09-22
    changes:
      - "Added Generic Base rules (no POC data, adoption procedure, Evidence/Snapshot/Confidence/Evaluation/Lineage/Self Check)"
  - version: 1.0.0
    date: 2026-09-21
    changes:
      - "Initial Claude Code project entry point"
---

# Claude Code Project Guide

공통 규칙은 `AGENTS.md`가 단일 원천이다. 아래 줄로 그대로 가져오며, 이 문서에서 다시 적지 않는다.

@AGENTS.md

## Claude Code 전용
- 프로젝트 스킬: `.claude/skills/` (project-status, register-artifact, impact-analysis, validate-project)
- 전문 서브에이전트: `.claude/agents/` (knowledge-curator, traceability-reviewer, data-governance-reviewer)
- 설정 예시: `.claude/settings.json.example` (검토 후 `settings.json`으로 복사)
- 사용 흐름과 프롬프트 가이드: `.claude/README.md`

작업이 스킬 설명과 맞으면 스킬을 쓰고, 집중 검토가 필요하면 서브에이전트에 맡긴다. 구조를 바꾼 뒤에는 `AGENTS.md`의 `검증` 명령을 실행한다.
