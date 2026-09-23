# Claude / Claude Code

Use root `CLAUDE.md` as the project entry point. Project-scoped reusable workflows live in `.claude/skills/` and specialist reviewers live in `.claude/agents/`.

## Recommended flow

1. Start Claude Code from the repository root.
2. Let `CLAUDE.md` establish project conventions.
3. Use approved Wiki/entities as the default evidence base.
4. Use project skills for repeat workflows such as status, artifact registration, impact analysis, and validation.
5. Use specialist subagents for focused curation, traceability, or data-governance review.
6. Keep model-generated drafts in `llm/generated/` until reviewed.

Do not store API keys or Claude credentials in this repository.
