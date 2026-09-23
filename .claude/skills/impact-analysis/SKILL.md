---
name: impact-analysis
description: Analyze the downstream impact of a changed requirement, feature, interface, API, database object, test, defect, or change request across the project knowledge graph.
---

# Impact Analysis

1. Locate the requested stable ID and confirm its current state.
2. Run `python scripts/traceability/build_trace_matrix.py` and traverse the `outgoing`/`incoming` columns (relations and computed inverses from `_base/registry/relations.yml`) across the development chain (REQ, DEV, SCR, API, IF, DB, TC, BUG) and the evaluation chain (OBJ, CAND, EVD, CRIT, MET, EVM, EVAL, DEC, ACT), plus CR, ISS, RISK, and DLV.
3. When a criterion, metric, or evaluation model changes, list the evaluations the trace output reports as `재평가 필요` and the decisions `based_on` them.
4. Inspect Wiki/design/release artifacts that reference the affected IDs.
5. Separate direct impact, probable impact, and unknown impact.
6. Identify required document, implementation, test, migration, deployment, and rollback updates.
7. Do not modify downstream files until the impact set is understood.
