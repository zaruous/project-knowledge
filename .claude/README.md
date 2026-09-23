# Claude Code Project Configuration

This directory contains project-scoped Claude Code extensions that can be committed and shared with the team.

## Layout

- `agents/`: specialist subagents for focused repository reviews.
- `skills/`: reusable project workflows exposed to Claude Code.
- `settings.json.example`: conservative starting point for project permissions. Copy to `settings.json` only after reviewing it for the target environment.

## Relationship to root guidance

`AGENTS.md` is the single source of repository rules for every provider. `CLAUDE.md` imports it (`@AGENTS.md`) and adds only Claude Code specifics. Do not restate shared rules here or in skills/agents.

## Recommended flow

1. Start Claude Code from the repository root so `CLAUDE.md` and the imported `AGENTS.md` are loaded.
2. Use approved Wiki/entities as the default evidence base.
3. Use project skills for repeat workflows such as status, artifact registration, impact analysis, and validation.
4. Use specialist subagents for focused curation, traceability, or data-governance review.
5. Keep model-generated drafts in `llm/generated/` until reviewed.

Do not store API keys or Claude credentials in this repository.

## Prompt guidance

For project knowledge tasks:

- state the target stable IDs and expected output clearly;
- provide long source material before the final question when manually constructing large prompts;
- keep source boundaries explicit using headings or structured tags;
- ask for repository paths/IDs as evidence;
- distinguish facts found in project artifacts from assumptions;
- prefer targeted file discovery over loading the full repository into context;
- use `llm/context/` and `wiki/00_project/glossary.md` for stable domain, architecture, and terminology context rather than repeating it in each prompt.
