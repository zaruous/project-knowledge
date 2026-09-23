# Monitor Workflow

시점에 따라 값이 변하는 대상은 Snapshot 기반으로 모니터링한다.
변경 감지 시 새 Snapshot을 생성하고 이전 데이터를 덮어쓰지 않는다.

## 이벤트 형식 (monitor 모듈)
스냅샷을 비교해 생긴 변화는 `data/events/<stream>/YYYY-MM.jsonl`에 한 줄씩 추가만 한다. 기존 줄은 고치지 않고, 정정은 새 이벤트로 남긴다.

```json
{"event_id": "price-2026-09-0001", "occurred_at": "2026-09-23T09:00:00+09:00", "type": "price-change", "subject_id": "CAND-0001", "snapshot_id": "SNAP-20260923-001"}
```

- `event_id`: 스트림 안에서 유일한 값
- `occurred_at`: 변화가 관측된 시각
- `type`: 이벤트 유형 (프로젝트가 정한다)
- `subject_id`: 대상 ID
- `snapshot_id`: 근거 스냅샷 (비교했다면 나중 스냅샷)

감지·누적·알림 자동화는 base에 포함하지 않는다.
