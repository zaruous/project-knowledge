---
id: ADOPT-0002
type: adoption-proposal
title: "신뢰도 등급 표준 척도 (A~D)"
status: candidate
source_project: home_finder_18p_project
source_finding: "3.0.0 수락 시험 A (home_finder 이관)"
proposed_at: "2026-09-24"
---

# ADOPT-0002 신뢰도 등급 표준 척도 (A~D)

## Problem
3.0.0의 신뢰도는 `level: unknown` 자유 값이라 프로젝트마다 기준이 다르고 평가 간 비교가 어렵다. POC는 A(구체 근거)~D(근거 부족, 중립값) 4등급을 정의해 점수와 따로 관리했다.

## Generalizable Pattern
신뢰도 기본 척도를 A~D로 두고, 평가 모델의 `confidence_scale`이 비어 있으면 이 척도를 쓴다. 프로젝트는 등급 정의를 바꿀 수 있지만 등급 이름은 유지한다.

## Why It Belongs in the Base
특정 도메인 개념이 아니라 근거·평가·기록을 다루는 방식이라 개발형과 평가형 프로젝트 모두에 적용된다.

## Expected Reuse
평가·의사결정형 프로젝트 전반, 개발형 프로젝트의 대안 평가와 AI 초안 검토.

## Impacted Structure
`status-sets.yml`에 `confidence` 결과 집합, 근거·평가 템플릿의 confidence 필드 검증.

## Validation Plan
두 번째 프로젝트에서 같은 문제가 확인되면 채용을 검토한다. 채용 시 `_base/self-check/base-adoption-gate.yml` 기준을 통과하고 수락 시험을 추가한다.

## Decision
검토 전 (candidate).
