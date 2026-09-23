# _base (템플릿 엔진)

프로젝트 관리 템플릿이 관리하는 영역입니다. 새 프로젝트에서는 고치지 않고, 템플릿이 업그레이드될 때 통째로 교체합니다. 프로젝트 전용 확장은 `_config/types.yml`, 루트 `templates/`·`scripts/`에 둡니다.

| 경로 | 내용 |
|---|---|
| `manifest.yml` | base 버전, 모듈별 폴더, 프로필별 wiki 단계, 경로 소유권 |
| `registry/` | 유형(`types.yml`), 상태(`status-sets.yml`), 관계(`relations.yml`) |
| `templates/` | 유형별 템플릿 |
| `framework/` | 범용 개념·워크플로·표준 문서 |
| `scripts/` | `init_project.py`(초기화), `validate.py`(검증), `trace.py`(추적 매트릭스), `self_check.py`(자체 점검), `knowledge.py`(공용 모듈) |
| `self-check/` | 템플릿 자체 점검 체크리스트, 점수표, 채용 기준 |
| `seeds/` | 초기화 때 쓰는 프로젝트 README 시드 |
| `tests/` | 검증기와 초기화 수락 시험 (`python -m unittest discover -s _base/tests`) |

## 업그레이드 (수동)
자동 업그레이드 도구는 아직 없습니다. 다음 순서로 반영합니다.
1. 새 base 버전의 `_base/`로 통째로 교체합니다.
2. `AGENTS.md`는 `<!-- base:begin -->`부터 `<!-- base:end -->`까지만 교체하고 프로젝트 규칙 블록은 그대로 둡니다. `manifest.yml`의 `ownership.managed`에 있는 나머지 파일도 교체합니다.
3. 새로 생긴 모듈 폴더가 있으면 `python _base/scripts/init_project.py --name <이름> --code <코드>`를 다시 실행합니다. 기존 파일은 바뀌지 않습니다.
4. `_config/project.yml`의 `base.version`을 새 버전으로 고치고 `python _base/scripts/validate.py`로 확인합니다.
