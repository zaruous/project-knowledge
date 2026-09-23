# Repository Layout Reference

## Core roots

| Path | Purpose |
|---|---|
| `_config/` | project, document type, status, LLM, retention, security policy |
| `framework/` | domain-neutral concepts, workflows, standards (ID prefixes in `standards/naming.md`) |
| `wiki/` | approved phase-oriented documentation |
| `entities/` | atomic traceability records (development + generic evaluation entities) |
| `data/` | incoming/raw/staging/normalized/derived/snapshots/lineage datasets and manifests |
| `attachments/` | PDF, DOCX, XLSX, PPTX, images, drawings, manuals |
| `scripts/` | ingestion, transform, validation, traceability, reporting, RAG helpers |
| `llm/` | prompts, context, summaries, generated drafts, evaluation |
| `index/` | chunks, metadata, embeddings, graph index |
| `evaluation/` | reusable criteria, scorecards, checklists, quality gates, results |
| `governance/` | adoption, decisions, changes, retrospectives for the base itself |
| `templates/` | reusable Markdown/YAML templates |
| `tests/` | fixtures and integration tests |
| `output/` | generated reports, exports, diagrams, packages |
| `archive/` | historical documents, datasets, releases |

## Phase-oriented Wiki

Use these phase groups unless the project has a documented alternative:

- `00_project/`
- `01_proposal/`
- `02_preparation/`
- `03_implementation/`
- `04_test/`
- `05_change/`
- `06_issue-risk/`
- `07_meeting/`
- `08_release/`
- `09_operation/`

## Data lifecycle

`incoming → raw → staging → normalized → derived → snapshot/evidence → evaluation`

- `incoming`: temporary landing area; validate before acceptance.
- `raw`: immutable accepted source data.
- `staging`: parsing/cleaning work area.
- `normalized`: canonical structured form.
- `derived`: calculations, aggregations, analytical outputs.
- `snapshots`: point-in-time states; never overwrite, create a new snapshot.
- `lineage`: input/output/process/checksum records for each transformation.
- `schemas`: machine-readable structure definitions.
- `manifests`: provenance and governance metadata.

## Git policy

Keep source-controlled:
- Markdown/YAML/JSON metadata
- templates
- scripts
- manifests
- approved Wiki and entities

Prefer external storage for:
- large raw datasets
- large binary attachments
- embeddings/vector indexes
- generated exports

When externalized, preserve storage URI/object key, checksum, dataset ID, source, and retention metadata in Git.

## Versioning

Record versions and change history in the main document's YAML front matter (`version`, `updated_at`, `changelog`). Do not create version-suffixed files (`CHANGELOG-v2.md`) or version sections (`## ... v2`).
