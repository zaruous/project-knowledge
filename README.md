---
title: Project Knowledge Repository
type: repository-guide
status: active
version: 3.0.0-alpha.3
updated_at: 2026-09-23
changelog:
  - version: 3.0.0-alpha.3
    date: 2026-09-23
    summary: 3.0.0 3단계 - 템플릿 층 분리, 프로필·모듈, 부트스트랩
    decision: governance/decisions/2026-09-23-template-structure-redesign.md
    changes:
      - "`framework/`, base 스크립트, 템플릿 자체 점검, base 테스트를 `_base/`로 이동. 스크립트 이름을 `init_project`·`validate`·`trace`·`self_check`로 정리"
      - "`_base/manifest.yml`: base 버전, 모듈(core/dev/eval/monitor/rag/governance)별 폴더, 프로필(development/evaluation)별 wiki 단계와 필수 산출물, 경로 소유권"
      - "템플릿 저장소에는 core·governance 폴더만 둔다 (`.gitkeep` 134개 → 27개). 개발·평가 모듈 폴더와 단계 README는 초기화 때 생성"
      - "`init_project.py`: 프로필·모듈 선택, 폴더·단계 README 생성, README를 프로젝트 시드로 교체, `governance/` 정리, `base.version` 기록. 재실행 안전, 템플릿 저장소 자체에서는 실행 차단"
      - "wiki 단계를 프로필별 연속 번호로 재정의. 회의·보고는 `wiki/90_management/`, 이슈·리스크·변경·결정은 엔티티로 관리"
      - "`AGENTS.md`를 base 블록과 프로젝트 규칙 블록으로 분리"
      - "`validate.py`: 역할(template/project)과 켠 모듈 기준으로 검사, README·manifest 버전 일치와 AGENTS 블록 표시 확인"
      - "ChatGPT Skill 전용 검증기 삭제 (공통 `_base/scripts/validate.py` 사용), `_config/project.yml`의 사용하지 않는 `repository:` 섹션 삭제"
      - "monitor 모듈의 이벤트 최소 형식과 수동 업그레이드 절차 문서화"
  - version: 3.0.0-alpha.2
    date: 2026-09-23
    summary: 3.0.0 2단계 - 레지스트리, 유형별 템플릿, 레지스트리 기반 검증
    decision: governance/decisions/2026-09-23-template-structure-redesign.md
    changes:
      - "`_base/registry/`에 유형(`types.yml`), 상태(`status-sets.yml`), 관계(`relations.yml`) 레지스트리 추가. `_config/document-types.yml`, `status-codes.yml` 삭제"
      - "신규 ID ISS(이슈), RISK(리스크), DLV(승인 산출물), EVM(평가 모델)과 저장 위치 추가"
      - "템플릿을 `_base/templates/`로 옮기고 27종으로 확장 (공용 design-object·candidate, wiki 4종, AI 초안). 루트 `templates/`는 프로젝트 전용"
      - "관계 필드 표준화: 출발 레코드에만 기록하고 역방향은 계산. `related_features`, `related_tests`, `subject_id` 등 폐지"
      - "`scripts/lib/knowledge.py`: ID·파일명·위치·상태·결과값·관계·누락 규칙·확장 덮어쓰기·템플릿 정합성 검증"
      - "`build_trace_matrix.py`: 관계와 역방향 CSV, 커버리지 요약, 평가 정의 버전이 바뀌면 재평가 필요 보고"
      - "`tests/integration/test_registry.py`: 올바른 체인 통과, 잘못된 레코드 실패를 확인하는 수락 시험"
      - "`_config/types.yml`: 프로젝트 전용 유형 확장 파일"
      - "AGENTS.md의 공식 기록 위치를 레지스트리 기준으로 변경"
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

# Project Knowledge Template

Wiki 기반 프로젝트 산출물, 추적 가능한 엔티티, 데이터, 평가·의사결정, LLM 에이전트 규칙을 함께 관리하는 **프로젝트 관리 템플릿**입니다. 개발형(SI·시스템 구축)과 평가·의사결정형 프로젝트를 같은 뼈대로 시작하고, 필요한 모듈만 켭니다. ChatGPT/Codex와 Claude Code가 같은 규칙(`AGENTS.md`)을 읽습니다.

이 README는 템플릿 저장소의 안내이며, front matter가 base 버전과 변경 내역의 기준입니다. 새 프로젝트를 초기화하면 이 파일은 프로젝트용 README로 바뀝니다.

## 새 프로젝트 시작

1. GitHub에서 **Use this template**으로 새 저장소를 만들고 clone합니다.
2. 새 저장소 루트에서 초기화합니다. bash와 PowerShell에서 같은 명령을 씁니다.

```bash
pip install -r requirements.txt
python _base/scripts/init_project.py --name "MES 구축" --code MES-001 --profile development --dry-run   # 할 일 미리보기
python _base/scripts/init_project.py --name "MES 구축" --code MES-001 --profile development
python _base/scripts/validate.py
```

초기화는 다음을 합니다.
- 켠 모듈의 폴더와 프로필의 wiki 단계 폴더를 만들고, 단계마다 목적·필수 산출물·게이트를 적은 `README.md`를 둡니다.
- 이 README를 프로젝트 README로 바꾸고, 템플릿 전용인 `governance/`를 정리합니다.
- `_config/project.yml`에 프로젝트 정보, 프로필, 모듈, 설치한 base 버전을 기록합니다. 다른 설정은 보존합니다.

다시 실행하면 빠진 폴더만 추가하고 기존 파일은 바꾸지 않습니다. 모듈은 나중에도 켤 수 있습니다(예: `--modules +monitor`). 이 템플릿 저장소 자체에서는 실행되지 않습니다.

## 프로필과 모듈

| 프로필 | 모듈 | wiki 단계 |
|---|---|---|
| development | core, dev | 01_proposal · 02_analysis-design · 03_implementation · 04_test · 05_release · 06_operation |
| evaluation | core, eval | 01_scope · 02_collect · 03_evaluate · 04_decide · 05_act-monitor |

| 모듈 | 내용 |
|---|---|
| core | 결정·조치·이슈·리스크·변경 요청·승인 산출물, 데이터 생명주기, wiki 관리 문서(회의·보고), LLM 초안 |
| dev | 요구사항 → 기능 → 화면·API·인터페이스·테이블 → 테스트 → 결함 |
| eval | 목표 → 대상·후보 → 근거 → 기준·지표 → 평가 모델 → 평가 |
| monitor (선택) | `data/events/`: 스냅샷 비교 이벤트를 추가만 하며 쌓는다 |
| rag (선택) | `index/`: RAG 인덱스 생성물 |

단계 이름과 필수 산출물은 `_base/manifest.yml`의 데이터라서 회사 산출물 표준에 맞게 고칠 수 있습니다. 개발형 프로젝트에서도 대안 평가가 필요하면 `--modules +eval`로 평가 모듈을 함께 켭니다.

## 핵심 원칙

1. 유형·ID·저장 위치·상태·관계의 원천은 `_base/registry/`입니다. 공식 기록은 등록된 위치에만 두고, 승인 여부는 `status`로 판단합니다.
2. 관계는 출발 레코드에 한 번만 기록하고, 역방향은 스크립트가 계산합니다.
3. `data/raw/`는 원본 불변 영역이며, 가공 과정은 `data/lineage/`에, 시점 상태는 `data/snapshots/`에 남깁니다.
4. `llm/generated/`는 AI 초안이며 승인 전에는 공식 산출물로 취급하지 않습니다.
5. 대용량 Raw·첨부파일은 Git 대신 MinIO/S3/NAS 사용을 권장하고, 위치와 체크섬만 Git에 둡니다.
6. `_base/`는 프로젝트에서 고치지 않습니다. 프로젝트 전용 확장은 `_config/types.yml`, `templates/`, `scripts/`에 둡니다.
7. 이 베이스에는 특정 POC의 실제 데이터나 도메인 전용 개념을 넣지 않습니다. 재사용 가능한 관리 패턴만 `governance/adoption/` 절차를 거쳐 채용합니다.

## 관리 포인트

| 관리 포인트 | 의미 | 정의 문서 |
|---|---|---|
| Evidence | 평가 근거와 출처 | `_base/framework/concepts/evidence-model.md` |
| Snapshot | 시점별 상태 보존 | `_base/framework/workflows/monitor.md`, `_base/templates/data/snapshot.yml` |
| Confidence | 근거 신뢰도와 평가 점수의 분리 | `_base/framework/concepts/evaluation-model.md` |
| Evaluation | Criterion/Metric/Weight/Score/Gate | `_base/framework/concepts/evaluation-model.md`, `evaluation/models/` |
| Data Lineage | Raw에서 Derived까지의 변환 추적 | `_base/framework/workflows/normalize.md`, `_base/templates/data/lineage.yml` |
| Adoption Governance | POC 아이디어의 공통 베이스 채용/기각 기록 | `governance/adoption/README.md` |
| Self Check | 구조와 정책의 자동 자가점검 | `_base/self-check/`, `_base/scripts/self_check.py` |

## 디렉터리 구조

```text
project-knowledge/
├─ _base/            [M] 템플릿 엔진 (manifest, registry, templates, framework, scripts, self-check, seeds, tests)
├─ AGENTS.md         [M+P] 공통 규칙 (base 블록 + 프로젝트 규칙 블록)
├─ CLAUDE.md         [M] Claude Code 진입점 (@AGENTS.md)
├─ .claude/ skills/  [M] Claude Code / ChatGPT·Codex 어댑터
├─ _config/          [S] 프로젝트 설정, 프로젝트 전용 유형(types.yml), 보안·보존·LLM 정책
├─ wiki/             [P] 00_project · 프로필 단계 폴더 · 90_management(회의·보고·base 피드백)
├─ entities/         [P] 켠 모듈의 엔티티
├─ evaluation/       [P, eval] models/ · results/
├─ data/             [P] incoming · raw · staging · normalized · derived · snapshots · lineage · manifests · schemas (+ events)
├─ llm/              [P] context · prompts · generated · evals
├─ templates/ scripts/ tests/   [P] 프로젝트 전용 추가분
├─ attachments/ output/ archive/  [P] 첨부 원본, 생성 결과, 승인 산출물 보존(archive/deliverables)
├─ index/            [P, rag] RAG 인덱스
└─ governance/       [템플릿 저장소 전용] adoption · decisions (초기화 때 정리)
```

[M]은 템플릿이 관리해 업그레이드로만 바뀌는 경로, [S]는 초기화 때 한 번 만들어진 뒤 프로젝트가 소유하는 경로, [P]는 프로젝트 소유 경로입니다. 전체 목록은 `_base/manifest.yml`의 `ownership`에 있고, 업그레이드 절차는 `_base/README.md`에 있습니다.

### 비슷해 보이는 경로의 역할 구분

| 경로 | 담는 것 |
|---|---|
| `entities/decisions/` | 프로젝트 의사결정 레코드 (`DEC-####`) |
| `governance/decisions/` | 템플릿(base) 자체의 구조·정책 결정 |
| `entities/criteria/`, `entities/metrics/` | 평가 기준·지표 정의 (`CRIT-####`, `MET-####`) |
| `evaluation/models/` | 평가 모델 (`EVM-####`). 기준·지표를 참조해 가중치·필터·공식으로 조합 |
| `entities/evaluations/`, `evaluation/results/` | 평가 실행 기록 (`EVAL-####`) / 계산 결과 파일 |
| `data/manifests/datasets/` | 데이터셋 기록 (`DS-####`). 이 한 곳에서만 관리 |
| `entities/deliverables/`, `archive/deliverables/` | 승인 산출물 기록 (`DLV-####`) / 승인본 보존 |

## 데이터 흐름

`incoming → raw → staging → normalized → derived → snapshot/evidence → evaluation`

## Agent / LLM 진입점

- `AGENTS.md`: 모든 Agent가 공유하는 규칙의 단일 원천
- `CLAUDE.md`: Claude Code 진입점 (`AGENTS.md`를 가져오고 Claude 전용 내용만 추가)
- `.claude/`: Claude Code 스킬, 서브에이전트, 설정 예시, 사용 안내(`README.md`)
- `skills/`: ChatGPT/Codex Skill 소스와 사용 안내(`README.md`)

## 템플릿 유지보수 (이 저장소)

```bash
python _base/scripts/validate.py
python _base/scripts/self_check.py
python -m unittest discover -s _base/tests
```

- base 버전을 올릴 때는 이 README front matter와 `_base/manifest.yml`의 `version`을 함께 올립니다. 검증기가 두 값이 같은지 확인합니다.
- `changelog` 맨 위에 항목을 추가하고 이전 항목은 지우지 않습니다. `AGENTS.md`, `CLAUDE.md`는 자기 문서의 변경 내역만 기록합니다.
- `CHANGELOG-v2.md`처럼 버전 접미사가 붙은 파일이나 `## ... v2` 같은 버전 섹션을 만들지 않습니다. 규칙은 `_base/framework/standards/metadata.md`에 있습니다.
- 구조 결정은 `governance/decisions/`, 채용 후보는 `governance/adoption/`에 기록합니다.
