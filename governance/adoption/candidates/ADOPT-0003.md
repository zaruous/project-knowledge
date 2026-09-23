---
id: ADOPT-0003
type: adoption-proposal
title: "점수는 코드가 계산하고 LLM은 설명만 한다"
status: candidate
source_project: home_finder_18p_project
source_finding: "3.0.0 수락 시험 A (home_finder 이관)"
proposed_at: "2026-09-24"
---

# ADOPT-0003 점수는 코드가 계산하고 LLM은 설명만 한다

## Problem
LLM이 종합 점수를 임의로 바꾸면 같은 입력으로 다시 계산해도 결과가 달라진다. POC는 종합 점수를 정해진 계산식으로만 산출하고 LLM은 근거 설명과 누락 탐지에만 썼다.

## Generalizable Pattern
평가(EVAL)의 점수는 `computed_by.script`가 있는 계산으로만 기록하고, LLM 설명은 `explanation` 필드나 AI 초안으로 분리한다.

## Why It Belongs in the Base
특정 도메인 개념이 아니라 근거·평가·기록을 다루는 방식이라 개발형과 평가형 프로젝트 모두에 적용된다.

## Expected Reuse
평가·의사결정형 프로젝트 전반, 개발형 프로젝트의 대안 평가와 AI 초안 검토.

## Impacted Structure
AGENTS.md LLM 사용 규칙, `evaluation.yml` 템플릿(`explanation`), 검증기(final EVAL에 `computed_by.script` 필수).

## Validation Plan
두 번째 프로젝트에서 같은 문제가 확인되면 채용을 검토한다. 채용 시 `_base/self-check/base-adoption-gate.yml` 기준을 통과하고 수락 시험을 추가한다.

## Decision
검토 전 (candidate).
