---
name: project-knowledge-manager
description: Manage a Wiki-based, multi-LLM project knowledge repository that connects proposal, preparation, implementation, test, change, release, and operation artifacts with traceable entities, governed raw/normalized data, automation scripts, and LLM/RAG assets. Use when ChatGPT needs to create or reorganize project folders, support ChatGPT/Codex and Claude Code in the same repository, generate Markdown/YAML project artifacts, maintain REQ→DEV→API/IF/DB→TC→BUG traceability, register datasets or attachments, validate repository structure, prepare LLM context, or separate AI-generated drafts from approved project knowledge.
---

# Project Knowledge Manager

Maintain project knowledge as four coordinated layers: official Wiki, traceable entities, governed data, and provider-neutral LLM automation.

## Operating rules

1. Treat `wiki/` as human-approved project knowledge.
2. Treat `entities/` as atomic traceability records.
3. Never modify files under `data/raw/` in place. Create transformed outputs under `staging/`, `normalized/`, or `derived/`.
4. Put unapproved AI output under `llm/generated/`; promote it only after explicit review/approval.
5. Keep large binaries and raw datasets outside Git when practical. Store URI/object key/checksum in manifests.
6. Preserve source links on generated summaries, reports, test cases, and impact analyses.
7. Prefer stable IDs over filenames when creating relationships.
8. Keep shared governance in `AGENTS.md`; use provider adapters such as `CLAUDE.md` (which imports `AGENTS.md`), `.claude/`, and `skills/` without duplicating project truth.

## Repository workflow

### 1. Classify incoming material

Determine whether the item is:
- official project knowledge → `wiki/`
- traceable requirement/design/test/defect record → `entities/`
- raw operational/customer/system data → `data/incoming/` then `data/raw/`
- binary supporting artifact → `attachments/`
- AI draft → `llm/generated/`
- deterministic helper → `scripts/`

Read `references/repository-layout.md` when choosing a destination. Read `references/claude-code.md` when adding or validating Claude Code support.

### 2. Register metadata

For project artifacts, include YAML frontmatter with stable `id`, `type`, `status`, and relationships where applicable.

Use these prefixes:
- `REQ-####` requirement
- `DEV-####` implementation feature
- `SCR-####` screen
- `API-####` API
- `IF-####` interface
- `DB-####` table/data object
- `TC-####` test case
- `BUG-####` defect
- `CR-####` change request
- `DEC-####` decision
- `DS-####` dataset
- `ISS-####` issue, `RISK-####` risk, `DLV-####` approved deliverable

For evaluation-oriented work, also use `OBJ` objective, `SUBJ` subject, `CAND` candidate, `EVD` evidence, `CRIT` criterion, `MET` metric, `EVM` evaluation model, `EVAL` evaluation, `ACT` action, `SNAP` snapshot, `LINEAGE` data lineage, and `ADOPT` adoption proposal.

When the repository has `_base/registry/`, it is the source of truth for types, ID formats, locations, status values, and relation fields. Record each relation once on the source record and never write inverse fields.

Record document versions in YAML front matter (`version`, `changelog`); never branch files or sections by version.

For raw data, create or update a dataset manifest with source, location, format, retention, security classification, parser, and related IDs.

### 3. Maintain traceability

Preserve the primary graph:

`REQ → DEV → (SCR/API/IF/DB) → TC → BUG`

When a requirement changes, inspect all downstream relations before proposing edits. Flag missing tests, orphan requirements, or entities with broken references.

### 4. Prepare LLM/RAG context

Do not send large raw files directly to an LLM by default. Prefer:

`raw → parser → normalized/derived → chunks + metadata → retrieval → LLM`

Use official Wiki, entities, normalized data, and manifests as the preferred context sources. Keep embeddings and generated indexes reproducible.

### 5. Validate before completion

When filesystem access is available:
- Run `python _base/scripts/validate.py` from the repository root for structural and record checks.
- Run repository-specific validation scripts if present.
- Report missing required roots or policy violations instead of silently creating conflicting conventions.

## Output expectations

When creating or modifying a project repository:
- create empty tracked directories with `.gitkeep` when Git must preserve them;
- avoid `.gitkeep` in directories already containing tracked files;
- create short README/AGENTS guidance where needed;
- provide templates rather than one-off examples for repeated artifact types;
- keep generated data and raw binaries out of Git unless the project explicitly requires versioning them.

## References

- Read `references/repository-layout.md` for directory semantics and data lifecycle.
- Read `references/metadata-conventions.md` for entity/frontmatter/manifest conventions.
- Read `references/claude-code.md` for the multi-LLM/Claude adapter layout.
