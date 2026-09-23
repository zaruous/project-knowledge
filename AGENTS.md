---
title: Project Knowledge Agent Guide
type: agent-guide
status: active
version: 3.0.0-alpha.1
updated_at: 2026-09-23
changelog:
  - version: 3.0.0-alpha.1
    date: 2026-09-23
    changes:
      - "모든 provider 공통 규칙의 단일 원천으로 지정 (`CLAUDE.md`는 이 문서를 가져옴)"
      - "`CLAUDE.md`에만 있던 공통 내용(시작하기 순서, 영향도 선보고, 검증 명령)을 이 문서로 이동"
      - "`llm/providers/` 폐지에 맞춰 provider 진입점 갱신"
      - "공식 기록 위치에 데이터셋 기록(`data/manifests/`) 포함"
  - version: 2.1.0
    date: 2026-09-23
    changes:
      - "파일명 오타 `AGGENTS.md`를 `AGENTS.md`로 정정"
      - "`Generic Base v2 rules` 섹션을 `공통 베이스 규칙`, `작업 우선순위`, `LLM 사용 규칙` 본문으로 통합"
      - "ID 규칙을 `framework/standards/naming.md` 단일 기준으로 연결"
      - "문서 버전을 front matter로 관리하는 규칙 추가"
  - version: 2.0.0
    date: 2026-09-22
    changes:
      - "범용 베이스 규칙 추가 (POC 데이터 배제, Adoption 절차, Evidence/Snapshot/Confidence/Lineage 연결)"
  - version: 1.0.0
    date: 2026-09-21
    changes:
      - "벤더 중립 Agent 운영 규칙 최초 작성"
---

# Project Knowledge Agent Guide

## 목적
이 저장소는 프로젝트 산출물과 실제 데이터를 Wiki/Entity/LLM 구조로 관리하는 프로젝트 관리 템플릿이다. 이 문서는 ChatGPT/Codex, Claude Code 및 기타 Agent가 공유하는 벤더 중립 규칙의 **단일 원천**이다. provider별 파일은 이 규칙을 반복하거나 완화하지 않는다.

## 시작하기
프로젝트 지식을 바꾸기 전에 다음 순서로 읽는다.
1. `AGENTS.md` (이 문서)
2. `README.md`: 디렉터리 구조, 경로별 역할, 저장소 버전
3. `_config/`: 프로젝트, 보안, 보존, 문서 유형, LLM 정책
4. `framework/`: 범용 개념, 워크플로, 표준 (ID는 `framework/standards/naming.md`)
5. 필요할 때 `llm/context/`(도메인, 아키텍처, 코딩 규칙)와 `wiki/00_project/glossary.md`(용어)

## Provider 진입점
- 공통 규칙: `AGENTS.md`
- Claude Code: `CLAUDE.md`(이 문서를 가져옴), `.claude/`(스킬, 서브에이전트, 설정 예시, 사용 안내)
- ChatGPT/Codex: `skills/`(Skill 소스와 사용 안내)

## 작업 우선순위
1. 기존 문서와 엔티티를 먼저 검색한다.
2. 중복 ID나 중복 문서를 생성하지 않는다.
3. 공식 기록은 `wiki/`, `entities/`, 데이터 기록(`data/manifests/`)에만 반영한다.
4. AI가 만든 초안은 우선 `llm/generated/`에 저장한다.
5. `data/raw/` 파일은 수정하거나 덮어쓰지 않는다.
6. Raw Data를 가공할 때 source, checksum, 생성일, 처리 스크립트를 Manifest와 `data/lineage/`에 기록한다.
7. 요구사항이 바뀌면 관련 DEV/API/IF/DB/TC/BUG 영향도를 먼저 확인해 보고한 뒤 관련 산출물을 수정한다.
8. 중요한 평가 결과는 Evidence, Snapshot, Confidence, Lineage 중 필요한 항목과 연결한다.
9. 모델별 설정은 `.claude/`, `skills/` 등 provider-specific 영역에 둔다.

## 공통 베이스 규칙
- 공통 영역에는 특정 POC의 실제 데이터와 도메인 전용 구조를 추가하지 않는다.
- POC에서 발견한 개선 아이디어는 `governance/adoption/candidates/`에 먼저 등록한다.
- 채용된 패턴만 `framework/`, `entities/`, `evaluation/`, `data/`, `scripts/`의 공통 구조에 반영한다.
- 구조나 정책을 바꾼 뒤에는 `검증`의 명령을 모두 통과해야 한다. 실패하면 검사를 우회하지 말고 구조를 고친다.

## ID 규칙
ID 접두어, 형식, 저장 위치는 `framework/standards/naming.md`를 단일 기준으로 따른다.

- 개발 엔티티: REQ, DEV, SCR, API, IF, DB, TC, BUG, CR, DEC, DS
- 범용 평가 엔티티: OBJ, SUBJ, CAND, EVD, CRIT, MET, EVAL, ACT, SNAP, LINEAGE, ADOPT

## 문서 관계
- 개발 체인: `REQ → DEV → (SCR/API/IF/DB) → TC → BUG`
- 범용 평가 체인: `Objective → Subject/Candidate → Evidence → Metric/Criterion → Evaluation → Decision → Action → Validation`

상세 기준은 `framework/standards/traceability.md`를 따른다.

## 데이터 흐름
`incoming → raw → staging → normalized → derived → snapshot/evidence → evaluation`

## 문서 버전 규칙
- 버전과 변경 내역은 문서 front matter의 `version`, `updated_at`, `changelog`로 관리한다.
- 파일명, 디렉터리명, 섹션명에 `-v2`, `v3` 같은 버전 표기를 붙여 분기하지 않는다.
- 저장소 전체 버전은 `README.md` front matter가 기준이다. 상세 규칙은 `framework/standards/metadata.md`를 따른다.

## LLM 사용 규칙
- 컨텍스트는 `_config/llm-policy.yml`의 `context_priority` 순서로 사용한다.
- 대용량 Raw Data를 무조건 LLM 컨텍스트에 넣지 않는다. 먼저 Parser/Normalizer로 구조화하고 필요한 범위만 Chunk한다.
- 생성물에는 근거 문서/엔티티/데이터셋 ID를 남긴다.
- 사람이 승인하기 전 AI 생성물은 공식 상태로 승격하지 않는다.
- API key, password, access token, `.env` 비밀값을 Wiki/LLM 컨텍스트에 저장하지 않는다.

## 검증
구조나 정책을 바꾼 뒤 저장소 루트에서 실행한다. bash와 PowerShell에서 같은 명령을 쓴다.

```bash
pip install -r requirements.txt
python scripts/validation/validate_structure.py
python scripts/evaluate/self_check_base.py
python scripts/traceability/build_trace_matrix.py   # 추적 매트릭스(CSV)
```
