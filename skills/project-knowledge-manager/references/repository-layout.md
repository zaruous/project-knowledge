# Repository Layout Reference

## Core roots

| Path | Purpose |
|---|---|
| `_base/` | template engine, not edited in projects: `manifest.yml` (modules, profiles, ownership), `registry/`, `templates/`, `framework/`, `scripts/` (init_project, validate, trace, self_check), `tests/` |
| `_config/` | project settings, project-specific types (`types.yml`), LLM, retention, security policy |
| `wiki/` | approved phase-oriented documentation |
| `entities/` | atomic traceability records (development + generic evaluation entities) |
| `data/` | incoming/raw/staging/normalized/derived/snapshots/lineage datasets and manifests |
| `attachments/` | PDF, DOCX, XLSX, PPTX, images, drawings, manuals |
| `scripts/` | project-specific scripts (base scripts live in `_base/scripts/`) |
| `llm/` | prompts, context, summaries, generated drafts, evaluation |
| `index/` | RAG index outputs (optional `rag` module) |
| `evaluation/` | evaluation models (`models/`) and computed results (`results/`), `eval` module |
| `governance/` | template repository only: adoption proposals and base decisions (removed when a project is initialized) |
| `templates/` | project-specific templates (base templates live in `_base/templates/`) |
| `tests/` | fixtures and integration tests |
| `output/` | generated reports, exports, diagrams, packages |
| `archive/` | historical documents, datasets, releases |

## Profiles, modules, and Wiki phases

Folders are created by `python _base/scripts/init_project.py --profile <name>` from `_base/manifest.yml`:

- modules: `core` (always), `dev`, `eval`, optional `monitor` (`data/events/`) and `rag` (`index/`)
- `development` profile phases: `01_proposal`, `02_analysis-design`, `03_implementation`, `04_test`, `05_release`, `06_operation`
- `evaluation` profile phases: `01_scope`, `02_collect`, `03_evaluate`, `04_decide`, `05_act-monitor`
- always: `wiki/00_project/` (overview, glossary) and `wiki/90_management/` (meetings, reports, base-feedback)

Issues, risks, change requests, decisions, actions, and approved deliverables are entities (ISS, RISK, CR, DEC, ACT, DLV), not Wiki folders.

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
