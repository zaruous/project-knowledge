# Claude Prompt Guidance

For project knowledge tasks:

- state the target stable IDs and expected output clearly;
- provide long source material before the final question when manually constructing large prompts;
- keep source boundaries explicit using headings or structured tags;
- ask for repository paths/IDs as evidence;
- distinguish facts found in project artifacts from assumptions;
- prefer targeted file discovery over loading the full repository into context;
- use `llm/context/` for stable domain/architecture terminology rather than repeating it in each prompt.
