---
name: validate-project
description: Validate the project knowledge repository structure, core policy files, Claude/agent configuration, raw-data separation, and traceability support before commits, releases, or handoffs.
---

# Validate Project

Run:

```bash
python scripts/validation/validate_structure.py
python scripts/evaluate/self_check_base.py
python -m unittest discover -s tests
```

Then inspect:
- required root files including `AGENTS.md`, `CLAUDE.md`, and `README.md`;
- `README.md` front matter `version`/`changelog`, and no version-suffixed files or sections (e.g. `*-v2.md`);
- `framework/`, `evaluation/`, and `governance/adoption/` base structure;
- `_config/` policies;
- `.claude/skills/` and `.claude/agents/` structure;
- `data/raw/` separation and manifests;
- registry consistency and entity relationships (reported by the validator from `_base/registry/`);
- AI drafts remaining under `llm/generated/` until approved.

Report validation failures with exact paths and recommended corrections.
