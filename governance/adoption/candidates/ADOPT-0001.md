---
id: ADOPT-0001
type: adoption-proposal
title: "근거 주장의 FACT / ANALYSIS / UNKNOWN 분류"
status: candidate
source_project: home_finder_18p_project
source_finding: "3.0.0 수락 시험 A (home_finder 이관)"
proposed_at: "2026-09-24"
---

# ADOPT-0001 근거 주장의 FACT / ANALYSIS / UNKNOWN 분류

## Problem
확인된 사실, 분석·추정, 미확인 값이 한 문서에 섞이면 사람과 LLM이 추정을 사실처럼 인용한다. POC는 모든 데이터를 FACT/ANALYSIS/UNKNOWN으로 구분하고, 미확인 값은 임의로 채우지 않고 중립값과 낮은 신뢰도로 다뤘다.

## Generalizable Pattern
근거(EVD)와 AI 초안의 주장에 `claim: fact | analysis | unknown`을 표시한다. unknown은 값을 채우지 않고 평가에서 중립값을 쓰며 신뢰도를 낮춘다.

## Why It Belongs in the Base
특정 도메인 개념이 아니라 근거·평가·기록을 다루는 방식이라 개발형과 평가형 프로젝트 모두에 적용된다.

## Expected Reuse
평가·의사결정형 프로젝트 전반, 개발형 프로젝트의 대안 평가와 AI 초안 검토.

## Impacted Structure
`status-sets.yml`에 `claim` 결과 집합, `evidence.yml`·`llm/draft.md` 템플릿에 필드 추가, 평가 모델에 unknown 처리 규칙.

## Validation Plan
두 번째 프로젝트에서 같은 문제가 확인되면 채용을 검토한다. 채용 시 `_base/self-check/base-adoption-gate.yml` 기준을 통과하고 수락 시험을 추가한다.

## Decision
검토 전 (candidate).
