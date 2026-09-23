# Agent Skills (ChatGPT / Codex)

ChatGPT/Codex reads the root `AGENTS.md` first; it is the single source of repository rules for every provider. This directory holds reusable Skill sources.

- `project-knowledge-manager/`: ChatGPT Skill for managing this repository (layout, metadata, traceability, validation).

Skills follow the same governance as other providers: approved Wiki/entities are authoritative, raw data is immutable, and AI drafts remain under `llm/generated/` until reviewed. A skill must not redefine or relax rules from `AGENTS.md`.
