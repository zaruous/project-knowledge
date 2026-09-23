# Naming Standard

ID 접두어의 단일 기준이다. `AGENTS.md`, 템플릿, 스크립트는 이 표를 따른다.

## 개발 엔티티

| 접두어 | 엔티티 | 형식 | 위치 |
|---|---|---|---|
| REQ | Requirement | `REQ-####` | `entities/requirements/` |
| DEV | Feature (개발 기능) | `DEV-####` | `entities/features/` |
| SCR | Screen | `SCR-####` | `entities/screens/` |
| API | API | `API-####` | `entities/apis/` |
| IF | Interface | `IF-####` | `entities/interfaces/` |
| DB | Table / Data object | `DB-####` | `entities/tables/` |
| TC | Test Case | `TC-####` | `entities/test-cases/` |
| BUG | Defect | `BUG-####` | `entities/defects/` |
| CR | Change Request | `CR-####` | `entities/change-requests/` |

## 범용 평가 엔티티

| 접두어 | 엔티티 | 형식 | 위치 |
|---|---|---|---|
| OBJ | Objective | `OBJ-####` | `entities/objectives/` |
| SUBJ | Subject | `SUBJ-####` | `entities/subjects/` |
| CAND | Candidate | `CAND-####` | `entities/candidates/` |
| EVD | Evidence | `EVD-####` | `entities/evidence/` |
| CRIT | Criterion | `CRIT-####` | `entities/criteria/` |
| MET | Metric | `MET-####` | `entities/metrics/` |
| EVAL | Evaluation | `EVAL-####` | `entities/evaluations/` |
| ACT | Action | `ACT-####` | `entities/actions/` |

## 공통 엔티티

| 접두어 | 엔티티 | 형식 | 위치 |
|---|---|---|---|
| DEC | Decision | `DEC-####` | `entities/decisions/` |
| DS | Dataset | `DS-####` | `data/manifests/datasets/` |
| SNAP | Snapshot | `SNAP-YYYYMMDD-###` | `data/snapshots/` |
| LINEAGE | Data Lineage | `LINEAGE-####` | `data/lineage/` |
| ADOPT | Adoption proposal | `ADOPT-####` | `governance/adoption/` |

## 규칙

- 같은 개념에 두 개의 접두어를 쓰지 않는다. Dataset은 `DS`만 사용한다.
- 도메인 전용 약어는 각 프로젝트에서 별도로 확장하고, 공통 베이스에는 Adoption 절차를 거쳐서만 추가한다.
- 파일명과 디렉터리명에 `-v2`, `_v3` 같은 버전 접미사를 붙이지 않는다. 버전은 `metadata.md`의 front matter 규칙을 따른다.
