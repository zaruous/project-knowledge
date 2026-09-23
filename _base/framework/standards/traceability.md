# Traceability Standard

관계의 원천은 `_base/registry/relations.yml`이다. 관계 이름, 값을 읽는 필드, 허용되는 출발·도착 유형, 역방향 이름이 모두 그 파일에 있다.

## 추적 체인
- 개발: `REQ -> DEV -> (SCR/API/IF/DB) -> TC -> BUG`
- 평가: `OBJ -> SUBJ/CAND -> EVD -> CRIT/MET -> EVM -> EVAL -> DEC -> ACT -> 후속 EVAL`
- 공통: CR은 `changes`로 변경 대상을, ISS·RISK·BUG는 `affects`로 영향 대상을 가리킨다.

## 기록 규칙
- 관계는 출발 레코드에 한 번만 기록한다. 예: 기능은 `implements: [REQ-0001]`, 테스트는 `verifies: [DEV-0001]`.
- 역방향(`implemented_by`, `verified_by` 등)은 스크립트가 계산한다. 직접 쓰면 검증 오류다.
- 값은 ID 목록이다. 파일명이나 경로로 연결하지 않는다.
- 관계마다 허용된 출발·도착 유형만 쓸 수 있다.
- 공유 설계 객체(API 등)는 기능이 `uses`로 가리킨다. 공유 파일을 기능마다 고치지 않기 위해서다.
- wiki 문서는 `describes`로 설명하는 엔티티를 가리킨다.

## 누락 검사
누락 규칙은 `relations.yml`의 `coverage`에 있다. 오류와 경고를 나누고, 일부는 특정 상태에서만 검사한다. 예: 테스트 케이스에 `verifies`가 없으면 오류, 승인된 요구사항을 구현하는 기능이 없으면 경고.

## 도구
- 검증: `python _base/scripts/validate.py`
- 추적 매트릭스: `python _base/scripts/trace.py` (CSV는 stdout, 커버리지 요약과 재평가 필요 목록은 stderr)
