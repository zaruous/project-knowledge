---
title: 프로젝트 관리 템플릿 구조 개편 결정
type: base-decision
status: accepted
version: 1.1.0
updated_at: 2026-09-23
decided_at: 2026-09-23
decided_by:
  - Claude Code (claude-opus-5-5)
  - Codex CLI (gpt-6-astra)
delegated_by: 사용자 (두 모델이 합의해 결정하도록 위임)
target_base_version: 3.0.0
inputs:
  - "페르소나 검토 4건: PM/PMO, 개발·QA 리드, 데이터·AI 엔지니어, 템플릿 오너·도입 담당"
  - "참고 POC: home_finder_18p_project_2026-09-23.zip (평가형 프로젝트 예시, 구조의 정답 아님)"
  - "Claude-Astra 합의 논의 2라운드"
changelog:
  - version: 1.1.0
    date: 2026-09-23
    changes:
      - "GitHub 템플릿 저장소 지정에 따른 조건 추가 (템플릿 전용 경로 정리, main 브랜치 운영)"
  - version: 1.0.0
    date: 2026-09-23
    changes:
      - "2라운드 합의로 최초 결정"
---

# 프로젝트 관리 템플릿 구조 개편 결정

## 배경
이 저장소의 목표는 여러 프로젝트가 가져다 쓰는 프로젝트 관리용 템플릿입니다. 개발형(REQ→DEV→SCR/API/IF/DB→TC→BUG)과 평가·의사결정형(OBJ→CAND→EVD→CRIT/MET→EVAL→DEC→ACT)을 모두 담아야 합니다.

2.1.0 시점의 문제는 다음과 같았습니다.
- 템플릿이 관리하는 파일과 프로젝트가 채울 파일이 섞여 있습니다.
- 유형·ID·상태·필수 경로가 문서와 스크립트 여러 곳에 따로 정의되어 있습니다.
- 파일 209개 중 134개가 `.gitkeep`인 빈 폴더입니다.
- 버그 두 가지가 확인됐습니다. `.gitignore`가 `.gitkeep` 20개를 제외하고, `init_project.py`가 `project.yml`의 `repository:` 섹션을 지웁니다.

## 결정 사항
1. **템플릿 층 분리:** 공유 규칙·레지스트리·템플릿·스크립트는 `_base/`로 분리합니다. 루트에 있어야 하는 어댑터(`AGENTS.md`, `CLAUDE.md`, `.claude/`, `skills/`)는 파일별로 소유권을 적용합니다. base가 제공한 파일만 [M]이고, 프로젝트가 추가한 파일은 [P]입니다. `governance/`는 템플릿 저장소에만 둡니다.
2. **프로필과 모듈:** 프로필은 기본 선택값이며 core·dev·eval 모듈을 조합할 수 있습니다. monitor와 rag는 선택 경로와 최소 규약만 선언합니다. 이벤트 한 줄에는 이벤트 ID, 발생 시각, 유형, 대상 ID, 근거 스냅샷을 담고, 자동화는 넣지 않습니다.
3. **wiki 단계:** 개발형 단계는 연속 번호(`01_proposal`~`06_operation`)로 정리합니다.
   - 단계 README는 프로필(단계 목적·필수 산출물·게이트 기준)에서 초기화 때 생성합니다. 프로젝트 소유 시드[S]이며 다시 실행해도 덮어쓰지 않습니다.
   - `gate-review.md`는 게이트 시점에 템플릿으로 만듭니다.
   - 회의·주간보고·게이트·일정은 ID 없이 날짜 기반 wiki 문서로 관리합니다.
4. **entities와 wiki의 경계:** 독립 ID와 관계가 필요한 대상은 entities에 두고, 여러 대상을 종합해 설명하는 문서는 wiki에 둡니다. 작은 엔티티의 상세 내용은 엔티티 본문에 씁니다.
   - 공식 기록 위치는 레지스트리가 정의합니다. 그래서 AGENTS.md의 "공식 지식은 wiki/entities에만"을 "레지스트리에 등록된 권위 위치"로 바꿉니다.
   - 승인 여부(status)는 저장 위치와 별개로 관리합니다.
5. **레지스트리:** 유형, 저장 형식(md/yml), 문서 `status` 값 집합, 결과 필드(`result`, `gate` 등) 값 집합, 관계 계약을 `_base/registry/`로 통합합니다. 프로젝트 확장은 `_config/types.yml`에 두며, base 접두어를 덮어쓰면 오류로 처리합니다.
6. **관계:** 관계는 한 번만 기록하고 역참조는 스크립트가 계산합니다.
   - 관계마다 출발·도착 유형을 검증합니다.
   - 누락 검사는 단계와 상태에 따라 경고 또는 오류로 나눕니다.
   - ACT의 결과 검증은 후속 EVAL로 연결합니다.
7. **신규 ID와 템플릿:** 신규 ID는 ISS, RISK, DLV, EVM 4종만 추가합니다. 템플릿은 다음과 같이 둡니다.
   - 전용 템플릿: requirement, feature, test-case, defect, change-request, decision, issue, risk, action, deliverable, objective, criterion
   - 전용 yml 템플릿: metric, evidence, evaluation, evaluation-model, dataset, snapshot, lineage
   - 공용 템플릿: `design-object.md`(screen/api/interface/table), `candidate.md`(SUBJ/CAND 공유, `type`과 접두어는 각각 유지)
   - wiki 템플릿: `wiki-document.md`, `meeting-minutes.md`, `weekly-report.md`, `gate-review.md`
8. **평가:** CRIT와 MET는 의미·단위·측정 방법을 정의하고, EVM은 이를 참조해 가중치·필터·적용 규칙으로 조합합니다. EVAL은 실행당 1파일이며 후보×기준별 근거를 가진 불변 기록입니다.
   - EVAL에는 입력 버전·체크섬·스냅샷·계산기 커밋·실행 인자를 고정합니다.
   - 기준이 바뀌면 과거 EVAL은 고치지 않고 재평가 필요 보고로 알립니다.
   - 범용 수식 엔진은 만들지 않고, 계산은 프로젝트 스크립트가 합니다.
9. **데이터:**
   - DS 기록의 기준 위치는 `data/manifests/datasets/`입니다.
   - payload는 기본적으로 Git에서 제외합니다. Git에 올릴 수 있는 크기·보안 등급 기준은 `_config/security-policy.yml`, 보존 기간은 `retention-policy.yml` 한 곳에 둡니다.
   - `.gitignore`는 기본 제외와 명시적 경로 예외만 맡고, 정책 준수 여부는 검증기가 확인합니다.
   - 승인된 산출물은 `archive/deliverables/<DLV-ID>/`에 보존합니다. 외부에 보존할 때는 불변 객체 버전을 가리키는 포인터를 둡니다. 승인 후 수정본은 새 DLV로 등록하고 이전 DLV와 연결합니다.
10. **초기화:** PyYAML을 쓰는 Python 단일 구현으로 통일하고 `init-project.ps1`은 삭제합니다.
    - 기존 설정 보존, 재실행 비파괴, `--root`, `--dry-run`을 지원합니다.
    - 모든 어댑터(Claude 스킬, ChatGPT Skill)가 공통 검증기 `_base/scripts/validate.py`를 호출합니다.
11. **버전의 의미:** 템플릿 README는 base 릴리스 버전, 프로젝트 README는 프로젝트 문서 버전, `_config/project.yml`의 `base.version`은 설치된 base 버전을 나타냅니다. Markdown은 front matter로, YAML은 최상위 메타데이터 키로 버전을 관리합니다.
12. **실행 순서:** 버그 수정 → 레지스트리 → 물리 분리 → 수락 시험 순서로 진행해 3.0.0으로 배포합니다.

## GitHub 템플릿 저장소 조건 (1.1.0 추가)
2026-09-23에 원격 저장소 `zaruous/project-knowledge`가 GitHub 템플릿 저장소로 지정되었습니다. 이에 따라 결정 1, 10을 다음 조건으로 구현합니다.
- "Use this template"은 기본 브랜치의 파일을 모두 복사합니다. 따라서 `governance/`, `_base/self-check/` 같은 템플릿 전용 경로는 복사를 막을 수 없습니다. 새 프로젝트에서 `init_project.py`가 이런 경로를 정리하고 `base.version`을 기록합니다.
- `main`이 새 프로젝트의 출발점이므로, 단계별 작업은 브랜치에서 진행하고 검증을 통과한 뒤에만 `main`에 합칩니다.

## 위 결정 중 사용자 확인 항목 (D1~D4)

| 항목 | 결정 |
|---|---|
| D1 `_base/` 물리 이동 여부 | 물리 분리, 루트 어댑터는 파일별 소유권 |
| D2 개발형 단계 번호 | 연속 번호로 재정의. 단계 정의는 프로필 yml의 데이터라 회사 표준에 맞게 바꿀 수 있음 |
| D3 고객 승인 산출물 보관 | `archive/deliverables/<DLV-ID>/` 또는 외부 불변 저장소, DLV에 URI·sha256·원문 버전·승인자·승인시각 기록 |
| D4 진행 범위 | 1~4단계 전체를 축소된 범위로 진행 |

## 범위에서 제외
- POC 실제 데이터와 도메인 개념(채광, 호가, 통근 등)
- monitor·rag 자동화(감지·누적·인덱싱 스크립트)
- 범용 수식 엔진
- 자동 업그레이드·병합 엔진과 stale 자동 전파. 입력 버전 비교 보고와 수동 업그레이드 절차만 둠
- 신규 ID MTG·WR·GATE·MS

## 수락 시험 (3.0.0 배포 조건)
- 개발형 프로필과 평가형 프로필로 각각 부트스트랩이 성공해야 합니다.
- core+dev+eval 조합으로 부트스트랩이 성공해야 합니다.
- `init_project.py`를 다시 실행해도 기존 파일이 바뀌지 않아야 합니다.
- Git이 추적하는 파일만으로 구조를 복원했을 때 검증을 통과해야 합니다.
- 잘못된 fixture는 반드시 실패해야 합니다: 중복 ID, 잘못된 관계 대상, 미등록 상태, 레지스트리와 템플릿 불일치, base 접두어 덮어쓰기.
- 평가 모델 설정을 바꾸면 계산 결과가 바뀌어야 합니다. home_finder는 공식이 코드에 박혀 있어 이 조건을 만족하지 못했습니다.

## 논의 경과
- Claude는 페르소나 4건을 종합해 제안을 냈습니다: `_base/` 분리, 레지스트리, 프로필·모듈, "닫히는 건은 entities" 기준, 신규 ID 8종, 전 유형 전용 템플릿.
- Astra의 1라운드(저장소 직접 검토)에서 다음이 바뀌었습니다.
  - entities 기준을 "독립 ID와 관계가 필요한 대상"으로 교체
  - 신규 ID를 8종에서 4종으로 축소
  - 템플릿을 공용과 전용으로 묶음
  - EVM이 CRIT/MET를 흡수하지 않고 참조만 하도록 정리
  - EVAL 재현성 조건 추가
  - 공식 지식 위치 정책과의 충돌을 지적
  - 수락 시험에 잘못된 fixture와 "설정 변경 시 계산 반영" 항목 추가
- 2라운드에서 Claude가 쟁점 6개(단계 README 생성, ps1 삭제, monitor·rag 선언, 템플릿 묶음, 승인본 위치, payload 기준)를 제시했고, Astra가 모두 수용하며 조건을 보탰습니다.
  - SUBJ/CAND는 템플릿만 공유하고 접두어는 유지
  - MET는 별도 yml 템플릿, ACT·DLV 최소 템플릿 추가
  - 승인 후 수정본은 새 DLV로 등록
  - 크기·보안 등급 정책은 `security-policy.yml` 한 곳에 둠
- 남은 이견은 없습니다.
