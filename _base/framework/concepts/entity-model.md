# Entity Model

## 엔티티와 wiki의 경계
독립 ID와 관계가 필요한 대상은 엔티티로, 여러 대상을 종합해 설명하는 문서는 wiki로 관리한다. 작은 엔티티의 상세 내용은 엔티티 본문에 쓴다. 공식 기록 위치는 레지스트리가 정의하고, 승인 여부는 위치가 아니라 `status`로 판단한다.

## 공통 엔티티
- Decision: 평가·변경·이슈를 근거로 한 의사결정
- Action: 결정·이슈·리스크·평가에서 나온 실행 항목
- Issue / Risk: 진행 중인 문제와 잠재 위험
- Change Request: 요구사항·범위·평가 정의의 변경 요청
- Deliverable: 고객 승인 산출물과 승인본 보존 기록
- Dataset / Snapshot / Lineage: 데이터 원천, 시점 상태, 변환 계보

## 개발 엔티티
- Requirement: 요구사항
- Feature: 요구사항을 구현하는 개발 기능
- Screen / API / Interface / Table: 기능이 사용하는 설계 객체
- Test Case: 기능과 설계 객체 검증
- Defect: 테스트에서 발견된 결함

## 평가 엔티티
- Objective: 달성하려는 목표
- Subject / Candidate: 관찰 대상 / 비교·선택 후보
- Evidence: 판단 근거
- Criterion / Metric: 평가 기준의 의미 / 측정 방법과 단위
- Evaluation Model: 기준과 지표를 조합한 가중치·필터·공식
- Evaluation: 평가 모델을 적용한 한 번의 실행 결과

유형, 접두어, 저장 위치는 `_base/registry/types.yml`이 정의한다 (`_base/framework/standards/naming.md`).
