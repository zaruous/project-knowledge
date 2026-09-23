# Naming Standard

ID 접두어, 형식, 저장 위치의 원천은 `_base/registry/types.yml`이다. 이 문서는 규칙을 설명하고, 접두어 목록은 모듈별 요약만 둔다(레지스트리와 일치하는지 테스트가 확인한다). 프로젝트 전용 유형은 `_config/types.yml`에 추가한다.

## ID 형식
- `PREFIX-####`: 숫자 4자리 일련번호 (예: `REQ-0001`)
- 스냅샷은 날짜를 담는다: `SNAP-YYYYMMDD-###`
- 회의록·주간보고·게이트 검토 같은 wiki 문서는 ID 없이 날짜 기반 파일 이름을 쓴다 (`YYYY-MM-DD-주제.md`, `YYYY-Www.md`)

## 모듈별 접두어
- core: DEC, ACT, ISS, RISK, CR, DLV, DS, SNAP, LINEAGE
- dev: REQ, DEV, SCR, API, IF, DB, TC, BUG
- eval: OBJ, SUBJ, CAND, CRIT, MET, EVD, EVAL, EVM
- governance: ADOPT (템플릿 저장소 전용)

## 규칙
- 레코드 파일 이름은 ID와 같다 (예: `entities/requirements/REQ-0001.md`). 스냅샷은 `data/snapshots/<SNAP-ID>/snapshot.yml`이다.
- 같은 개념에 두 개의 접두어를 쓰지 않는다. Dataset은 `DS`만 사용한다.
- 프로젝트 확장은 base 유형 이름과 접두어를 덮어쓸 수 없다. 덮어쓰면 검증 오류다.
- 도메인 전용 약어는 각 프로젝트의 `_config/types.yml`에서 확장하고, 공통 베이스에는 Adoption 절차를 거쳐서만 추가한다.
- 파일명과 디렉터리명에 `-v2`, `_v3` 같은 버전 접미사를 붙이지 않는다. 버전은 `metadata.md`의 front matter 규칙을 따른다.
