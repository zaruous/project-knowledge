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
- evidence
- confidence
- snapshot_id

관계는 공통 필드가 아니라 `_base/registry/relations.yml`에 정의된 관계 필드로 쓴다 (`traceability.md`).

## 형식
- 사람이 쓰고 승인하는 레코드는 Markdown + front matter, 스크립트가 만들거나 다시 계산하는 레코드는 YAML(최상위 키)로 둔다. 유형별 형식은 `_base/registry/types.yml`에 고정되어 있다.
- 새 레코드는 레지스트리에 등록된 템플릿(`_base/templates/`)에서 시작한다. 프로젝트 전용 템플릿은 `templates/`에 둔다.

## status와 결과 필드
- `status`는 레코드의 수명주기다. 유형별 값 집합은 `_base/registry/status-sets.yml`의 `status_sets`에 있다.
- 테스트 결과(`result`), 게이트 판정(`gate`)처럼 수명주기가 아닌 값은 `result_sets`로 따로 관리하고 status에 섞지 않는다.
- 값은 kebab-case로 쓴다 (예: `in-progress`, `not-run`).

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
- 평가가 고정해서 쓰는 정의(CRIT, MET, EVM)는 `version`을 가진다. 정의를 바꾸면 version을 올린다.
- YAML 레코드는 같은 키(`version`, `updated_at`, `changelog`)를 최상위에 둔다.
- 금지: `CHANGELOG-v2.md`, `STRUCTURE-v2.md` 같은 버전 접미사 파일, 본문 끝에 `## ... v2` 섹션을 덧붙이는 방식.
