# cx English BDD/TDD Workflow Pack

This package contains the English source for cx, a Codex workflow pack for human-AI BDD/TDD collaboration. The installable public source is `SKILLS/en`; this package directory keeps the full source, templates, guides, agents, and validation tools used to prepare releases.

Do not install both language packs into the same target project. English and Chinese packages intentionally share the same skill and agent names.

## Core Contract

cx is a workflow package, not a component library. It standardizes how humans and AI agents discover behavior, write tests first, implement code, research technical choices, manage release versions, and review evidence.

Feature folders should be ordered by business capability:

```text
docs/1.Configuration System/
docs/1.Configuration System/BDD.md
docs/1.Configuration System/ENGINEERING_SPEC.md
docs/1.Configuration System/CHANGELOG.md
```

The BDD document heading and `Feature:` name must match the folder name.

## Quick Start

```powershell
uv tool install shskills
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:USERPROFILE\.codex\skills" --subpath en --ref main --force --clean
```

If `CODEX_HOME` is set, use `$env:CODEX_HOME\skills` as the destination.

## Prompt Patterns

Best coding-agent prompts give the agent an explicit contract:

```text
Goal:
Context:
Constraints:
Required workflow:
Verification:
Deliverables:
```

Prefer naming the target feature folder, the cx skills to use, commands that must pass, and the evidence that should be recorded. For Claude Code projects, keep `AGENTS.md` as the shared rule source and have `CLAUDE.md` import or reference it.

Feature or bugfix:

```text
Use $cx-workflow. Select the smallest required cx skills. Start with $cx-bdd, create or update the ordered feature folder and BDD.md, then use $cx-tdd to write the failing test before implementation.
```

Python / PyTorch / Lightning:

```text
Use $cx-bdd, $cx-tdd, and $cx-pytorch-tdd. Use explicit OOP design for state and invariants, unittest-first tests, deterministic tiny data, and avoid dynamic reflection such as getattr/setattr unless no static API works.
```

Rust:

```text
Use $cx-bdd, $cx-tdd, and $cx-rust-tdd. Model state with structs/enums/traits, write the failing #[test] or integration test first, then run cargo test, cargo fmt, and clippy when practical.
```

Research:

```text
Use $cx-research. Define the research question, search window, inclusion/exclusion criteria, academic sources, official sources, and interpretation sources. Cite every non-obvious claim.
```

Release:

```text
Use $cx-version. Decide the SemVer bump, update VERSION and manifests, update CHANGELOG.md, validate, then create an annotated vX.Y.Z tag.
```

## Skill Map

| Skill | Use for |
| --- | --- |
| `$cx-workflow` | Workflow routing and skill selection |
| `$cx-bdd` | BDD discovery, ordered feature folders, business rules, scenarios |
| `$cx-tdd` | Red-green-refactor, test matrices, code quality gates |
| `$cx-changelog` | `CHANGE-*` entries and changelog consistency |
| `$cx-version` | SemVer, `VERSION`, changelog, release tags |
| `$cx-research` | Model choice, model mechanisms, recent papers, sourced synthesis |
| `$cx-pytorch-tdd` | Python/PyTorch/Lightning implementation and tests |
| `$cx-rust-tdd` | Rust implementation, ownership-aware design, cargo test/fmt/clippy |
| `$cx-common-module` | Reusable module extraction and API design |
| `$cx-evidence` | Final evidence review |

## Validation

```bash
python -m unittest discover -s tests
python tools/validate_skill_pack.py .
python tools/validate_cx_pack.py .
python tools/validate_single_source.py examples/python_ml_project
```
