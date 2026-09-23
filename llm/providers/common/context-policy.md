# Shared Context Policy

Use context in this order when possible:

1. `AGENTS.md` and provider entry point (`CLAUDE.md` when using Claude Code).
2. Relevant `_config/` policies.
3. Approved `wiki/` and `entities/` records.
4. `data/manifests/` and normalized/derived data needed for the task.
5. Selected raw/attachment evidence only when necessary.
6. `llm/generated/` only as draft material, never as authoritative truth.

Keep secrets out of prompts and context bundles. Prefer stable IDs and repository paths for evidence references.
