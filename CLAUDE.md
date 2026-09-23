---
title: Claude Code Project Guide
type: agent-guide
status: active
version: 2.1.0
updated_at: 2026-09-23
changelog:
  - version: 2.1.0
    date: 2026-09-23
    changes:
      - "`Generic Base v2` section merged into `Repository model`, `Base framework rules`, and `Validation`"
      - "Validation now uses the single merged `scripts/validation/validate_structure.py` plus the self check"
      - "Added the front matter versioning rule"
  - version: 2.0.0
    date: 2026-09-22
    changes:
      - "Added Generic Base rules (no POC data, adoption procedure, Evidence/Snapshot/Confidence/Evaluation/Lineage/Self Check)"
  - version: 1.0.0
    date: 2026-09-21
    changes:
      - "Initial Claude Code project entry point"
---

# Claude Code Project Guide

## Purpose
This repository is a generic base that manages project deliverables, traceable entities, raw/processed data, evaluations and decisions, automation scripts, and LLM/RAG assets as a Wiki-based knowledge base.

## Start here
Before changing project knowledge, read:
1. `AGENTS.md` for repository-wide agent rules.
2. `README.md` for the directory model, quick start, and the repository version/changelog.
3. `_config/` for project, security, retention, document, and LLM policies.
4. `framework/` for generic concepts, workflows, and standards (IDs in `framework/standards/naming.md`).
5. `llm/context/` for domain, architecture, terminology, and coding context when relevant.

## Repository model
- `wiki/`: human-reviewed and approved project knowledge.
- `entities/`: atomic traceability records — development entities (REQ, DEV, SCR, API, IF, DB, TC, BUG, CR, DEC, DS) and generic evaluation entities (OBJ, SUBJ, CAND, EVD, CRIT, MET, EVAL, ACT).
- `data/raw/`: immutable source data. Never edit or overwrite in place.
- `data/staging/`: intermediate parsing/cleaning outputs.
- `data/normalized/`: standardized reusable data.
- `data/derived/`: calculated or analytical outputs.
- `data/snapshots/`: point-in-time states. Create a new snapshot instead of overwriting.
- `data/lineage/`: input/output/process records from raw to derived.
- `attachments/`: source documents and binary evidence.
- `framework/`: domain-neutral concepts, workflows, and standards.
- `evaluation/`: reusable criteria, scorecards, checklists, quality gates, and results.
- `governance/`: governance of the base itself (adoption, decisions, changes, retrospectives).
- `llm/generated/`: unapproved AI-generated drafts.
- `index/`: reproducible RAG/index artifacts.
- `output/`: exported reports and generated deliverables.

## Required traceability
Preserve the primary relationship graph:

`REQ -> DEV -> (SCR/API/IF/DB) -> TC -> BUG`

For evaluation-oriented work, also preserve:

`Objective -> Subject/Candidate -> Evidence -> Metric/Criterion -> Evaluation -> Decision -> Action -> Validation`

When a requirement changes, inspect downstream relationships and report impact before editing related artifacts.

## Data handling rules
1. Do not modify `data/raw/` files in place.
2. Register source, checksum, location, schema, security classification, retention, and parser in `data/manifests/`, and record transformations in `data/lineage/`.
3. Do not place credentials, API keys, passwords, tokens, or personal secrets in Wiki/LLM context files.
4. For large data, summarize or transform first; do not load the entire dataset into model context without a clear need.
5. Keep generated and reproducible data separate from authoritative source data.

## AI output rules
1. Create drafts under `llm/generated/` unless the user explicitly asks to update an approved artifact.
2. Preserve evidence links using entity IDs, Wiki paths, dataset IDs, or attachment references.
3. Do not promote AI output to official Wiki knowledge without review/approval.
4. Prefer existing IDs and documents over creating duplicates.

## Base framework rules
1. Do not add a specific POC's data or domain-only concepts to the common base.
2. Register patterns found in real projects under `governance/adoption/candidates/` first; apply them to the common structure only after adoption.
3. Keep Evidence, Snapshot, Confidence, Evaluation, Data Lineage, and Self Check rules intact.
4. Link important evaluation results to the Evidence, Snapshot, Confidence, or Lineage they depend on.

## Versioning rules
1. Record versions and change history in each main document's YAML front matter (`version`, `updated_at`, `changelog`).
2. Do not branch files, directories, or sections by version (e.g. `CHANGELOG-v2.md`, `## ... v2`). Edit the document in place and add a changelog entry.
3. The repository version lives in `README.md` front matter. See `framework/standards/metadata.md`.

## Claude Code extensions
- Project skills: `.claude/skills/`
- Specialist subagents: `.claude/agents/`
- Project settings example: `.claude/settings.json.example`
- Provider-specific guidance: `llm/providers/claude/`

Use the project skills when the task matches their descriptions. Delegate focused review work to the specialist agents when useful.

## Validation
Before completing repository structure changes, run:

```bash
python scripts/validation/validate_structure.py
python scripts/evaluate/self_check_base.py
```

For traceability output, run:

```bash
python scripts/traceability/build_trace_matrix.py
```

If validation fails, fix the structural issue instead of bypassing the check.
