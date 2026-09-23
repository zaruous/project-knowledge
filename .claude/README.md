# Claude Code Project Configuration

This directory contains project-scoped Claude Code extensions that can be committed and shared with the team.

## Layout

- `agents/`: specialist subagents for focused repository reviews.
- `skills/`: reusable project workflows exposed to Claude Code.
- `settings.json.example`: conservative starting point for project permissions. Copy to `settings.json` only after reviewing it for the target environment.

## Relationship to root guidance

`CLAUDE.md` is the Claude Code entry point. `AGENTS.md` remains the vendor-neutral repository policy used by ChatGPT/Codex and other agents. Both should describe the same core governance rules; provider-specific behavior belongs here or under `llm/providers/`.
