# Metadata Standard

공통 권장 필드:
- id
- type
- title/name
- status
- owner
- created_at
- updated_at
- observed_at
- collected_at
- source
- tags
- related_entities
- evidence
- confidence
- snapshot_id

## 문서 버전 관리

버전과 변경 내역은 문서 자체의 YAML front matter로 관리한다. 파일명, 디렉터리명, 섹션명으로 버전을 분기하지 않는다.

```yaml
---
title: 문서 제목
version: 2.1.0
updated_at: 2026-09-23
changelog:
  - version: 2.1.0
    date: 2026-09-23
    summary: 한 줄 요약
    changes:
      - "변경 내용"
---
```

- `version`: Semantic Versioning(`MAJOR.MINOR.PATCH`)을 따른다. 구조/개념 추가는 MAJOR 또는 MINOR, 문구 정정은 PATCH.
- `changelog`: 최신 항목을 맨 위에 추가한다. 이전 항목은 삭제하지 않는다.
- 저장소(공통 베이스) 전체 버전과 변경 내역은 `README.md` front matter가 단일 기준이다.
- `AGENTS.md`, `CLAUDE.md` 등 주요 문서는 자기 문서의 변경 내역만 기록한다.
- 금지: `CHANGELOG-v2.md`, `STRUCTURE-v2.md` 같은 버전 접미사 파일, 본문 끝에 `## ... v2` 섹션을 덧붙이는 방식.
