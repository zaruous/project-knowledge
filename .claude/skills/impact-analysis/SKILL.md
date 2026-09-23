---
name: impact-analysis
description: Analyze the downstream impact of a changed requirement, feature, interface, API, database object, test, defect, or change request across the project knowledge graph.
---

# Impact Analysis

1. Locate the requested stable ID and confirm its current state.
2. Traverse relevant links across REQ, DEV, SCR, API, IF, DB, TC, BUG, CR, and DEC.
3. Inspect Wiki/design/release artifacts that reference the affected IDs.
4. Separate direct impact, probable impact, and unknown impact.
5. Identify required document, implementation, test, migration, deployment, and rollback updates.
6. Do not modify downstream files until the impact set is understood.
