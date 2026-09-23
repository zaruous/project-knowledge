# Automation Scripts

프로젝트 지식 저장소를 생성, 검증, 변환, 추적, 평가, 인덱싱, 보고하기 위한 결정론적 도구를 둡니다.

## 주요 영역

- `bootstrap/`: 프로젝트 초기화 (`_config/project.yml` 기록, 기존 설정 보존)
- `ingest/`: 외부 데이터/문서 반입
- `transform/`: Raw → staging/normalized/derived 변환 (Lineage 기록 포함)
- `wiki/`: Wiki 문서 관리
- `lib/`: 공용 모듈 (`knowledge.py`: 레지스트리 로드, 레코드 스캔·검증, 역방향 관계 계산)
- `traceability/`: 추적 매트릭스와 커버리지·재평가 필요 보고 (`_base/registry/relations.yml` 기준)
- `evaluate/`: Evaluation, Quality Gate, Self Check 실행
- `governance/`: Adoption 등 베이스 거버넌스 자동화
- `monitor/`: Snapshot 기반 변화 감시
- `llm/`: provider-neutral LLM/RAG context 준비
- `rag/`: chunk/index/embedding 생성
- `validation/`: 구조/메타데이터 검증
- `reports/`: 상태/테스트/릴리즈 보고서 생성

Claude Code와 ChatGPT/Codex 모두 같은 스크립트를 호출하도록 유지하고, 모델별 차이는 `.claude/`, `skills/`에 둡니다.

## 기본 검증

```bash
pip install -r requirements.txt
python scripts/validation/validate_structure.py   # 필수 경로, README 버전 front matter, 버전 접미사 파일명 검사
python scripts/evaluate/self_check_base.py        # 구조 검증 + 핵심 관리 문서 자가점검
python scripts/traceability/build_trace_matrix.py # 추적 매트릭스(CSV), 요약은 stderr
python -m unittest discover -s tests              # 검증기 수락 시험 (tests/integration/)
```
