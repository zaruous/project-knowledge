---
name: traceability-reviewer
description: Review REQ to DEV, design, API/interface/database, test, defect, change, and decision relationships and identify missing or broken traceability.
---

Review project traceability using the primary graph:

`REQ -> DEV -> (SCR/API/IF/DB) -> TC -> BUG`

Relations, allowed source/target types, and coverage rules are defined in `_base/registry/relations.yml`. Use `python _base/scripts/trace.py` output instead of inferring links from filenames.

For each requested scope:
- identify missing downstream links;
- flag requirements without implementation or tests;
- flag tests without a requirement/feature basis;
- include related CR/DEC records when they affect interpretation;
- distinguish confirmed links from inferred candidates;
- do not create IDs solely to make the matrix look complete.
