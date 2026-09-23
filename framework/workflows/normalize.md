# Normalize Workflow

`raw -> staging -> normalized -> derived`

- raw: 불변 원본
- staging: 파싱/정제 중간 상태
- normalized: 표준 스키마로 정리된 데이터
- derived: 계산/집계/분석 결과

각 단계는 `data/lineage/`에 입력과 출력을 기록한다.
