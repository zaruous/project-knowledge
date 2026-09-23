# Lifecycle

프로젝트 단계는 프로필마다 다르며 `_base/manifest.yml`의 `profiles.<이름>.phases`가 정의한다. 초기화하면 단계마다 `wiki/<단계>/README.md`(목적, 필수 산출물, 게이트)가 만들어진다. 단계 이름과 산출물은 데이터라서 회사 산출물 표준에 맞게 고칠 수 있다. 프로필별 단계 목록은 `README.md`의 `프로필과 모듈`에 있다.

단계와 무관하게 전 기간에 걸쳐 관리하는 것:
- `wiki/00_project/`: 개요, 용어
- `wiki/90_management/`: 회의록(`meetings/`), 주간·월간 보고(`reports/`), base 개선 제안(`base-feedback/`)
- 이슈·리스크·변경 요청·결정·조치·승인 산출물은 엔티티(ISS, RISK, CR, DEC, ACT, DLV)로 관리한다. 변경 영향 분석은 CR 본문에 적는다.
- 단계 전환은 게이트 검토 문서(`_base/templates/wiki/gate-review.md`)로 기록한다.

평가 중심 프로젝트의 범용 판단 흐름:

`Objective -> Collect -> Normalize -> Evaluate -> Decide -> Act -> Validate -> Monitor`
