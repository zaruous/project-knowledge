# Claude Code Compatibility

A multi-LLM project repository should keep core governance vendor-neutral and add Claude Code as an adapter layer.

Required Claude-oriented paths:

- `CLAUDE.md`: project entry point for Claude Code.
- `.claude/skills/`: reusable Claude Code workflows.
- `.claude/agents/`: specialist project subagents.
- `llm/providers/claude/`: provider-specific prompt/context guidance.

Keep `AGENTS.md`, Wiki/entity conventions, raw-data immutability, and approval rules authoritative across providers. Do not fork project truth into separate Claude-only copies.
