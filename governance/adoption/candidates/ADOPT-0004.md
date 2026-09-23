---
id: ADOPT-0004
type: adoption-proposal
title: "삭제 대신 상태 변경과 사유 기록"
status: candidate
source_project: home_finder_18p_project
source_finding: "3.0.0 수락 시험 A (home_finder 이관)"
proposed_at: "2026-09-24"
---

# ADOPT-0004 삭제 대신 상태 변경과 사유 기록

## Problem
후보나 레코드를 지우면 왜 제외했는지, 어떤 평가에서 빠졌는지 추적할 수 없다. POC는 후보를 삭제하지 않고 상태를 REJECTED로 바꾸고 사유를 남겼다.

## Generalizable Pattern
레코드는 지우지 않고 `status`를 rejected·deprecated 등으로 바꾸며 `reason` 필드에 사유를 남긴다. 레코드 파일 삭제는 검증기가 git 이력으로 경고한다.

## Why It Belongs in the Base
특정 도메인 개념이 아니라 근거·평가·기록을 다루는 방식이라 개발형과 평가형 프로젝트 모두에 적용된다.

## Expected Reuse
평가·의사결정형 프로젝트 전반, 개발형 프로젝트의 대안 평가와 AI 초안 검토.

## Impacted Structure
AGENTS.md 작업 우선순위, 템플릿의 `reason` 필드, 검증기(삭제된 ID를 참조하는 레코드 경고).

## Validation Plan
두 번째 프로젝트에서 같은 문제가 확인되면 채용을 검토한다. 채용 시 `_base/self-check/base-adoption-gate.yml` 기준을 통과하고 수락 시험을 추가한다.

## Decision
검토 전 (candidate).
