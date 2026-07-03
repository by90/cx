# Research Notes

This package follows the current Codex customization model:

- `AGENTS.md` is durable repository guidance for coding agents.
- Skills are reusable workflows stored in directories with `SKILL.md`.
- Repository-level skills are discovered under `.agents/skills`.
- Skills can be invoked explicitly with `$skill-name` or selected implicitly from their description.
- Custom subagents live under `.codex/agents/*.toml`.
- Codex starts subagents only when the user explicitly asks.

References:

- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/codex/concepts/customization
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- https://agents.md/

The core design decision is to keep the discipline of documents first and task-scoped implementation second, without making unit tests or TDD the default path. AI defaults to completing the current task document and then editing one production code file; if a second code file is needed, it must be split into another task first. `docs/cx` can hold project and domain notes; each main success scenario owns one folder; tasks live in `tasks/`; changes live in `changes/`. Code, documentation, tutorials, research, design, and process-change deliverables must pass `$cx-review`, then `$cx-evidence` before handoff. This lets AI decide work from unfinished changes while preventing scattered per-request documents, all-at-once multi-file implementation, default test generation, or skipped review.
