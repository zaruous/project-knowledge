# Metadata Conventions

## Entity frontmatter

Minimum fields:

```yaml
---
id: REQ-0001
type: requirement
title: Example requirement
status: draft
---
```

Record each relationship once, on the source record, as a list of IDs. Inverse links are computed by scripts. For example, a feature and a test case:

```yaml
# entities/features/DEV-0012.md
implements: [REQ-0001]
uses: [API-0007]
# entities/test-cases/TC-0021.md
verifies: [DEV-0012]
```

Relation names and allowed types come from `_base/registry/relations.yml` when present.

## Dataset manifest

Recommended fields:

```yaml
id: DS-0001
type: dataset
name: Equipment production result
status: active
kind: equipment_log
source:
  system: SAMPLE_SYSTEM
  interface: RS232
location:
  storage: minio
  bucket: project-001
  object_prefix: raw/equipment/2026/09/
format: csv
schema:
  file: data/schemas/equipment.schema.json
retention:
  policy: raw_data_default
security:
  classification: internal
processing:
  parser: scripts/transform/normalize_logs.py
supports: [REQ-0001, IF-0003]
```

## AI-generated content

Record at least:
- generated date/time when available
- model/tool when relevant
- source artifact IDs
- review status

Do not mark AI drafts `approved` without explicit human approval.
