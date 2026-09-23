# Project Scripts

이 프로젝트 전용 자동화 스크립트를 둡니다. base 스크립트(초기화, 검증, 추적, 자체 점검)는 `_base/scripts/`에 있으며 프로젝트에서 고치지 않습니다.

필요할 때 만드는 하위 폴더:
- `ingest/`: 외부 데이터·문서 반입
- `transform/`: raw → staging/normalized/derived 변환. 입력·출력·체크섬을 `data/lineage/`에 기록한다
- `evaluate/`: 평가 계산. 평가 모델 파일(`evaluation/models/EVM-####.yml`)을 읽어 계산하고, 공식을 코드에 박지 않는다
- `monitor/`: 스냅샷 비교와 이벤트 기록 (`data/events/`)
- `reports/`: 상태·테스트·릴리스 보고서 생성
- `rag/`: 청크·인덱스 생성 (`index/`)

Claude Code와 ChatGPT/Codex가 같은 스크립트를 호출하도록 하고, 모델별 차이는 `.claude/`, `skills/`에 둡니다.

## base 명령
```bash
python _base/scripts/validate.py                   # 구조·레코드 검증
python _base/scripts/trace.py > output/trace.csv   # 추적 매트릭스, 요약은 stderr
python _base/scripts/self_check.py                 # base 자체 점검
python -m unittest discover -s _base/tests         # 검증기·초기화 수락 시험
```
