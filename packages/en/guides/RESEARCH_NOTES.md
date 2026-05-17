# Research Notes

This package is based on the current Codex customization model:

- `AGENTS.md` is durable repository guidance for coding agents.
- Skills are reusable workflows stored as directories with `SKILL.md` files. Each skill needs a `name` and `description`.
- Repository skills are discovered under `.agents/skills`.
- Skills can be invoked explicitly with `$skill-name`, and they can also be selected implicitly from their description.
- Custom subagents live under `.codex/agents/*.toml`. Each custom agent needs `name`, `description`, and `developer_instructions`.
- Codex only spawns subagents when explicitly asked.

Useful references:

- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/codex/concepts/customization
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- https://agents.md/

The main design decision is to keep Spec/Plan/Tasks discipline but collapse long-lived artifacts into documentation sets under `docs/`. Small projects may use `docs/ENGINEERING_SPEC.md` plus `docs/CHANGELOG.md`; multi-feature projects use `docs/INDEX.md`, `docs/VERSIONS.md`, and multiple `docs/<feature-group>/` documentation sets. Concrete change IDs and task order live only in each feature group's `CHANGELOG.md`, and non-programming tasks do not use TDD. This preserves testable behavior and audit history while preventing per-requirement document clutter.
