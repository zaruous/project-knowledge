# Adoption Governance

실전 POC에서 발견한 아이디어를 공통 베이스에 반영하는 절차다.

## 원칙

- 특정 도메인 데이터와 업무용어 자체는 베이스에 넣지 않는다.
- 최소 두 개 이상의 프로젝트에 재사용 가능하거나, 하나의 POC에서 명확한 구조적 효과가 검증된 패턴을 후보로 등록한다.
- 후보는 `candidates/`에서 검토한다.
- 채용 시 `adopted/`, 미채용 시 `rejected/`로 결정 기록을 이동한다.
- 실제 파일 구조/템플릿/스크립트 변경과 Adoption ID를 연결한다.
- 이 폴더는 템플릿 저장소에만 있다. 프로젝트에서는 `wiki/90_management/base-feedback/`에 먼저 적고, 템플릿 저장소에 후보로 등록한다.

## 흐름

`POC Finding -> Adoption Candidate -> Review -> Adopt/Reject -> Base Change -> Self Check`
