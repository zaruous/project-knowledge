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

Add relationship arrays only when relevant, for example:

```yaml
related_features:
  - DEV-0012
related_tests:
  - TC-0021
source:
  - ../../wiki/01_proposal/rfp/customer-rfp.md
```

## Dataset manifest

Recommended fields:

```yaml
dataset_id: DS-0001
name: Equipment production result
type: equipment_log
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
  period: 3y
security:
  classification: internal
processing:
  parser: scripts/transform/normalize_logs.py
related:
  requirements: [REQ-0001]
  interfaces: [IF-0003]
```

## AI-generated content

Record at least:
- generated date/time when available
- model/tool when relevant
- source artifact IDs
- review status

Do not mark AI drafts `approved` without explicit human approval.
