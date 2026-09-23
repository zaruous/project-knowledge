# _base (템플릿 엔진)

프로젝트 관리 템플릿이 관리하는 영역입니다. 새 프로젝트에서는 수정하지 않고, 템플릿이 업그레이드될 때 교체됩니다.

| 경로 | 내용 |
|---|---|
| `registry/types.yml` | 유형별 ID 형식, 모듈, 저장 위치, 형식, 템플릿, 상태 집합 |
| `registry/status-sets.yml` | status 값 집합과 결과 필드 값 집합 |
| `registry/relations.yml` | 관계 이름, 허용 유형, 역방향 이름, 누락 검사 규칙 |
| `templates/` | 유형별 템플릿 (entities, data, evaluation, wiki, llm, governance) |

프로젝트 전용 확장은 `_config/types.yml`과 루트 `templates/`에 둡니다. 검증은 `python scripts/validation/validate_structure.py`로 합니다.
