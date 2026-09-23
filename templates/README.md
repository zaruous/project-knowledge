# Project Templates

이 프로젝트에서만 쓰는 템플릿을 둡니다. base 템플릿은 `_base/templates/`에 있으며 프로젝트에서 고치지 않습니다.

프로젝트 전용 유형을 추가할 때는 `_config/types.yml`에 유형을 등록하고, `template`에 이 폴더의 경로(저장소 루트 기준, 예: `templates/inspection.md`)를 적습니다. 템플릿의 `type`과 `id` 형식은 등록한 유형과 맞아야 합니다(검증기가 확인).
