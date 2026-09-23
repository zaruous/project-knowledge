---
title: Project Knowledge Repository
type: repository-guide
status: active
version: 3.0.0-alpha.1
updated_at: 2026-09-23
changelog:
  - version: 3.0.0-alpha.1
    date: 2026-09-23
    summary: 3.0.0 1단계 - 버그 수정과 중복 경로 정리 (구조 유지)
    decision: governance/decisions/2026-09-23-template-structure-redesign.md
    changes:
      - "`.gitignore`가 하위 폴더의 `.gitkeep`까지 제외하던 버그 수정. `.env.*`, `.claude/settings.local.json`, 스냅샷 payload 제외 추가"
      - "`.gitattributes`로 저장소 줄바꿈을 LF로 고정"
      - "`init_project.py`: 기존 설정 보존(PyYAML 직렬화), 재실행 안전, `--dry-run`, 저장소 루트 기본값. `init-project.ps1` 삭제"
      - "`requirements.txt` 추가 (PyYAML)"
      - "wiki에서 entities와 겹치는 폴더 9개 삭제 (requirements 3곳, test cases/defects, change-request, decisions, actions, 03_implementation/deployment)"
      - "`evaluation/criteria/` 삭제. 평가 기준 정의는 `entities/criteria/`"
      - "데이터셋 기록 위치를 `data/manifests/datasets/`로 단일화 (`entities/datasets/`, `datasets.yml` 삭제)"
      - "`data/samples/` 삭제(`tests/fixtures/` 사용), `llm/context/terminology.md` 삭제(`wiki/00_project/glossary.md` 사용)"
      - "`llm/providers/` 폐지: 컨텍스트 우선순위는 `_config/llm-policy.yml`, Claude 안내는 `.claude/README.md`, ChatGPT/Codex 안내는 `skills/README.md`"
      - "`CLAUDE.md`는 `@AGENTS.md`를 가져오고 Claude 전용 내용만 유지. 공통 규칙은 `AGENTS.md` 단일 원천"
  - version: 2.1.0
    date: 2026-09-23
    summary: 버전별로 분기된 파일과 섹션을 단일 구조로 통합
    changes:
      - "`CHANGELOG-v2.md`를 README.md front matter `changelog`로 통합하고 삭제"
      - "`STRUCTURE-v2.md`를 README.md `디렉터리 구조` 섹션으로 통합하고 삭제"
      - "README.md/AGENTS.md/CLAUDE.md 끝에 덧붙인 `Generic Base v2` 섹션을 본문 규칙으로 통합"
      - "`AGGENTS.md` 파일명 오타를 `AGENTS.md`로 정정"
      - "`scripts/governance/validate_base_structure.py`를 `scripts/validation/validate_structure.py`로 통합"
      - "개발/범용 ID 접두어를 `framework/standards/naming.md`로 단일화 (Dataset 접두어는 `DS`로 확정)"
      - "문서 버전은 파일명이 아닌 front matter로 관리하는 규칙 추가 (`framework/standards/metadata.md`)"
      - "`build_trace_matrix.py`가 범용 엔티티 ID와 YAML 엔티티를 함께 수집하도록 확장"
  - version: 2.0.0
    date: 2026-09-22
    summary: Generic Base - 특정 도메인에 종속되지 않는 범용 관리 포인트 추가
    added_concepts:
      - Objective / Subject / Candidate
      - Evidence
      - Snapshot
      - Confidence
      - Criterion / Metric / Evaluation
      - Data Lineage
      - Quality Gate
      - Adoption Governance
      - Self Check
    added_paths:
      - framework/
      - entities/objectives/
      - entities/subjects/
      - entities/candidates/
      - entities/criteria/
      - entities/metrics/
      - entities/evidence/
      - entities/evaluations/
      - entities/actions/
      - entities/datasets/
      - data/snapshots/
      - data/lineage/
      - evaluation/
      - governance/
      - tests/
  - version: 1.0.0
    date: 2026-09-21
    summary: Wiki 기반 멀티 LLM 프로젝트 지식 저장소 초기 구조
    changes:
      - "wiki/entities/data/attachments/llm/index/output 기본 구조"
      - "`AGENTS.md`(벤더 중립), `CLAUDE.md`/.claude/(Claude Code), skills/(ChatGPT) 진입점 분리"
      - "REQ → DEV → (SCR/API/IF/DB) → TC → BUG 추적성 체계"
---

# Project Knowledge Repository

Wiki 기반 프로젝트 산출물, 엔티티 추적성, Raw Data, 평가·의사결정, 자동화 스크립트, LLM/RAG 자산을 함께 관리하기 위한 공통 베이스 저장소입니다. ChatGPT/Codex와 Claude Code가 같은 지식 구조를 공유하도록 벤더 중립 규칙과 provider-specific 진입점을 분리합니다.

버전과 변경 내역은 이 문서의 front matter(`version`, `changelog`)에서 관리합니다. 파일명이나 섹션명에 버전을 붙이지 않습니다.

## 핵심 원칙

1. `wiki/`는 사람이 검토하고 승인한 공식 지식입니다.
2. `entities/`는 추적 가능한 원자 엔티티입니다. 개발 체인(REQ → DEV → API/IF/DB → TC → BUG)과 범용 평가 체인(Objective → Evidence → Evaluation → Decision → Action)을 함께 관리합니다.
3. `data/raw/`는 원본 불변 영역이며 직접 수정하지 않습니다.
4. `data/normalized/`, `data/derived/`는 스크립트로 재생성 가능한 가공 데이터이며, 변환 과정은 `data/lineage/`에 기록합니다.
5. `llm/generated/`는 AI 초안이며 승인 전에는 공식 산출물로 취급하지 않습니다.
6. `index/`는 RAG 검색 인덱스용 생성 데이터입니다.
7. 대용량 Raw/첨부파일은 Git 대신 MinIO/S3/NAS 사용을 권장합니다.
8. 모델별 규칙은 공통 지식 구조를 바꾸지 않고 provider adapter 형태로 추가합니다.
9. 이 베이스는 특정 POC의 실제 데이터나 도메인 전용 개념을 저장하지 않습니다. 실전 POC는 검증장이고, 재사용 가능한 관리 패턴만 `governance/adoption/` 절차를 거쳐 채용합니다.

## 관리 포인트

| 관리 포인트 | 의미 | 정의 문서 |
|---|---|---|
| Evidence | 평가 근거와 출처 | `framework/concepts/evidence-model.md` |
| Snapshot | 시점별 상태 보존 | `framework/workflows/monitor.md`, `templates/snapshot.yml` |
| Confidence | 근거 신뢰도와 평가 점수의 분리 | `framework/concepts/evaluation-model.md` |
| Evaluation | Criterion/Metric/Weight/Score/Gate | `framework/concepts/evaluation-model.md`, `evaluation/` |
| Data Lineage | Raw에서 Derived까지의 변환 추적 | `framework/workflows/normalize.md`, `templates/lineage.yml` |
| Adoption Governance | POC 아이디어의 공통 베이스 채용/기각 기록 | `governance/adoption/README.md` |
| Self Check | 구조와 정책의 자동 자가점검 | `evaluation/checklists/base-framework-self-check.md`, `scripts/evaluate/self_check_base.py` |

## Agent / LLM 진입점

- `AGENTS.md`: 모든 Agent가 공유하는 규칙의 단일 원천
- `CLAUDE.md`: Claude Code 진입점 (`AGENTS.md`를 가져오고 Claude 전용 내용만 추가)
- `.claude/`: Claude Code 스킬, 서브에이전트, 설정 예시, 사용 안내(`README.md`)
- `skills/`: ChatGPT/Codex Skill 소스와 사용 안내(`README.md`)

## 디렉터리 구조

```text
project-knowledge/
├─ _config/        # 프로젝트, 문서 유형, 상태, LLM, 보존 및 보안 정책
├─ framework/      # 범용 개념(concepts) / 워크플로(workflows) / 표준(standards)
├─ wiki/           # 프로젝트 단계별 공식 문서 (00_project ~ 09_operation)
├─ entities/       # 추적성 원자 엔티티 (개발 엔티티 + 범용 평가 엔티티)
├─ data/           # incoming/raw/staging/normalized/derived + snapshots/lineage/manifests/schemas
├─ attachments/    # PDF, DOCX, XLSX, 이미지 등 원본 첨부물
├─ evaluation/     # 재사용 평가 규칙(scorecards/checklists/quality-gates)과 계산 결과(results)
├─ governance/     # 베이스 자체의 운영 기록 (adoption/decisions/changes/retrospectives)
├─ scripts/        # 초기화, 수집, 변환, 평가, 검증, 추적성, 모니터링, 보고, RAG 자동화
├─ llm/            # 공통 컨텍스트, 프롬프트, AI 생성물, LLM 평가
├─ index/          # chunk, metadata, embedding, graph
├─ templates/      # 표준 문서/메타데이터 템플릿
├─ tests/          # fixtures/integration
├─ output/         # 자동 생성 결과물
├─ archive/        # 과거 문서, 데이터셋, 릴리즈
├─ skills/         # ChatGPT Skill 패키지 소스
├─ .claude/        # Claude Code 프로젝트 설정/스킬/서브에이전트
├─ AGENTS.md       # ChatGPT/Codex 공통 운영 규칙
├─ CLAUDE.md       # Claude Code 운영 규칙
└─ README.md       # 저장소 안내 + 버전/변경 내역 (front matter)
```

### 비슷해 보이는 경로의 역할 구분

| 경로 | 담는 것 |
|---|---|
| `entities/decisions/` | 프로젝트 의사결정 레코드 (`DEC-####`) |
| `governance/decisions/` | 공통 베이스(템플릿) 자체의 구조·정책 결정 |
| `entities/criteria/`, `entities/metrics/` | 평가 기준·지표 정의 (`CRIT-####`, `MET-####`) |
| `entities/evaluations/` | 평가 실행 기록 (`EVAL-####`) |
| `evaluation/` | 재사용 평가 규칙 세트(scorecards, quality-gates, checklists)와 계산 결과(results) |
| `data/manifests/datasets/` | 데이터셋 기록 (`DS-####`). 이 한 곳에서만 관리 |

ID 접두어와 저장 위치의 전체 매핑은 `framework/standards/naming.md`를 따릅니다.

## 데이터 흐름

`incoming → raw → staging → normalized → derived → snapshot/evidence → evaluation`

## 빠른 시작

GitHub에서 이 저장소의 **Use this template**으로 새 프로젝트 저장소를 만든 뒤, 새 저장소 루트에서 실행합니다.

```bash
pip install -r requirements.txt
python scripts/bootstrap/init_project.py --name "MES 구축" --code MES-001 --dry-run   # 결과 미리보기
python scripts/bootstrap/init_project.py --name "MES 구축" --code MES-001
python scripts/validation/validate_structure.py
python scripts/evaluate/self_check_base.py
```

bash와 PowerShell에서 같은 명령을 사용합니다. `init_project.py`는 `_config/project.yml`의 다른 설정을 보존하므로 다시 실행해도 안전합니다.

Claude Code를 사용하는 경우 저장소 루트에서 실행하면 `CLAUDE.md`를 기준으로 프로젝트 규칙을 적용할 수 있습니다. `.claude/settings.json.example`은 필요한 경우 검토 후 `.claude/settings.json`으로 복사하여 사용합니다.

## 버전 관리

- 저장소(공통 베이스) 버전과 전체 변경 내역은 이 문서의 front matter가 단일 기준입니다.
- 버전을 올릴 때는 `version`, `updated_at`을 갱신하고 `changelog` 맨 위에 항목을 추가합니다.
- `AGENTS.md`, `CLAUDE.md`는 자기 문서의 변경 내역만 front matter에 기록합니다.
- `CHANGELOG-v2.md`, `STRUCTURE-v3.md`처럼 버전 접미사가 붙은 파일이나 `## ... v2` 같은 버전 섹션을 만들지 않습니다. 규칙은 `framework/standards/metadata.md`에 있습니다.
