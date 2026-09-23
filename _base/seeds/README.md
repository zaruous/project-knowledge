---
title: $name
type: project-readme
status: active
version: 0.1.0
updated_at: $date
changelog:
  - version: 0.1.0
    date: $date
    changes:
      - "프로젝트 초기화 (base $base_version, 프로필 $profile, 모듈 $modules)"
---

# $name ($code)

이 저장소는 프로젝트 관리 템플릿 base $base_version(프로필 `$profile`)으로 시작했습니다. 공통 규칙은 `AGENTS.md`, 템플릿 구조는 `_base/README.md`에 있습니다.

## 구성
- 모듈: $modules
- wiki 단계:
$phases

## 자주 쓰는 명령
```bash
pip install -r requirements.txt
python _base/scripts/validate.py                       # 구조·레코드 검증
python _base/scripts/trace.py > output/trace.csv       # 추적 매트릭스
python _base/scripts/init_project.py --name "$name" --code $code --modules +monitor   # 모듈 추가
```

## 버전
이 문서의 front matter가 프로젝트 문서 버전입니다. 설치된 base 버전은 `_config/project.yml`의 `base.version`입니다.
