# Traceability Standard

최소 추적 체인:

`Objective -> Subject/Candidate -> Evidence -> Metric/Criterion -> Evaluation -> Decision -> Action -> Validation`

개발 프로젝트에서는 다음 체인을 병행한다.

`REQ -> DEV -> (SCR/API/IF/DB) -> TC -> BUG`

- CR/DEC는 요구사항 해석이나 범위를 바꿀 때 해당 REQ에 연결한다.
- 중요한 Evaluation은 사용한 EVD, SNAP, LINEAGE ID를 남긴다.
- 관계는 파일명이 아니라 ID로 연결하며, ID 체계는 `naming.md`를 따른다.
- 추적 매트릭스: `python scripts/traceability/build_trace_matrix.py`
