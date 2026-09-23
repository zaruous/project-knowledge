# Collect Workflow

1. 신규 입력을 `data/incoming/`에 둔다.
2. 형식, 출처, 보안등급을 확인한다.
3. 원본을 `data/raw/<DS-ID>/<수집 단위>/`에 보존한다 (예: `data/raw/DS-0001/2026-09-24/`). 가공 단계(staging, normalized, derived)도 같은 `<DS-ID>/` 규칙을 따른다.
4. Manifest와 checksum을 생성한다.
5. 원본은 이후 직접 수정하지 않는다.
6. payload는 기본적으로 Git에 두지 않는다. 작은 비민감 데이터만 `.gitignore`에 명시 예외를 두고, 검증기가 `_config/security-policy.yml`의 `git_payload` 기준(크기, 데이터셋 보안 등급)으로 확인한다.
