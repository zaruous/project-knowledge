# Evaluation Model

평가는 다음 요소를 분리해서 관리한다.

1. Criterion: 무엇을 평가하는가
2. Metric: 어떻게 측정하는가
3. Weight: 얼마나 중요한가
4. Evidence: 어떤 근거를 사용했는가
5. Score: 평가 결과
6. Confidence: 결과를 얼마나 신뢰할 수 있는가
7. Gate: 통과/실패를 결정하는 최소 조건

같은 데이터와 같은 규칙으로 재실행하면 동일한 결과가 나와야 한다.

## 레코드 역할
- Criterion(CRIT), Metric(MET): 기준의 의미와 측정 방법·단위를 정의한다.
- Evaluation Model(EVM, `evaluation/models/`): CRIT/MET를 참조해 가중치, 하드필터(Gate), 공식, 신뢰도 척도로 조합한다. 정의를 복사하지 않는다.
- Evaluation(EVAL): 한 번의 실행 기록이다. 후보별 점수, 근거, 신뢰도, 게이트 판정을 담는다.

## 재현성
- EVAL은 적용한 모델(`applies`), 입력(`based_on`), 사용한 정의의 버전(`pinned`), 계산 스크립트와 커밋·인자(`computed_by`)를 고정한다.
- `final` 상태의 EVAL은 고치지 않는다. 정의가 바뀌면 추적 매트릭스가 "재평가 필요"를 보고하고, 다시 평가하면 새 EVAL을 만들어 `supersedes`로 잇는다.
- 점수는 계산 스크립트가 EVM 파일을 읽어 구한다. 공식을 코드에 박아 두면 모델을 바꿔도 결과가 바뀌지 않는다.
- 조치(ACT)의 효과는 후속 EVAL의 `validates`로 확인한다.
