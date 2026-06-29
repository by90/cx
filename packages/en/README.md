# cx English Use-Case-Driven TDD Workflow Pack

This directory contains the English package source for cx. The installable public source is `SKILLS/en`; this package directory keeps source, templates, guides, agents, and validation tools.

Do not install both English and Chinese packages into the same target project. Skill and agent names intentionally stay aligned across languages.

## Core Contract

cx is a workflow pack, not a component library. It defines how humans and AI keep use cases, design notes, tasks, changes, and verification evidence under `docs/cx`. Before work starts, choose an execution mode; if the user does not explicitly choose per-task confirmation, AI defaults to completing documentation, strict TDD, implementation, and validation directly.

```text
docs/cx/00.project.md
docs/cx/01.create_user/00.use_case.md
docs/cx/01.create_user/00.design.md
docs/cx/01.create_user/tasks/01.write_user_entity/00.task.md
docs/cx/01.create_user/changes/20260629T120000-task01-write_user_entity.md
```

Each task's basic measure is a class or type group. One task handles one task document, one code file, and one matching unit-test file when needed.

Use-case granularity follows user goals: one main success scenario folder carries one user-goal use case. The main success scenario runs from trigger to completed goal, usually in 3 to 9 main steps, and each step is one observable actor-system interaction. Conditional, alternate, and exception behavior must use substep numbering such as `1.1` or `2.1` under a concrete main step, and must say whether the flow returns to a step, ends this use case, or enters another use case. Do not put several home-screen buttons, mutually exclusive choices, or complete tasks into one main success scenario. If a complex conditional flow needs its own actors, steps, and completion criteria, split it into a separate use case and index it from the project document.

## Quick Start

Install or update from the repository default `main` branch only:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install_cx_en.ps1
```

Raw install:

```powershell
uv tool install shskills
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:USERPROFILE\.codex\skills" --subpath en --force --clean
```

## Prompt Patterns

Feature or bug:

```text
Use $cx-workflow and select the smallest required cx skills. Before starting, ask whether to finish documentation, tests, implementation, and validation directly, or ask after each task; if I do not choose per-task confirmation, default to direct completion. First use $cx-story to create or update docs/cx use-case, design, task, and change documents, then use $cx-tdd to write the failing test and implement.
```

Python / PyTorch:

```text
Use $cx-story, $cx-tdd, and $cx-pytorch-tdd. Use a uv-managed Python interpreter. Use strict OOP design for state, lifecycle, invariants, and domain collaboration. Write unittest tests first with deterministic tiny data, and avoid dynamic reflection such as getattr/setattr unless no static API works.
```

Rust:

```text
Use $cx-story, $cx-tdd, and $cx-rust-tdd. Model state with structs/enums/traits, write the failing #[test] or integration test first, then run cargo test, cargo fmt, and clippy when practical.
```

Release:

```text
Use $cx-version. Work must happen on a short-lived local branch and merge to main only after user confirmation. Do not push work branches; the remote keeps only main and version tags. Only on main update VERSION, manifests, root changelog, validation, annotated vX.Y.Z tag, then push main and the release tag.
```

## Skill Map

| Skill | Purpose |
| --- | --- |
| `$cx-workflow` | Workflow routing and skill selection |
| `$cx-story` | Use cases, main success scenarios, conditional substeps, tasks, and changes |
| `$cx-tdd` | Strict test-first work, narrow failing tests, minimal implementation, and refactor |
| `$cx-changelog` | `changes/` documents and release-note consistency |
| `$cx-version` | Project-local `tools/semver.py`, SemVer, `VERSION`, `docs/VERSIONS.md`, and release tags |
| `$cx-research` | Model selection, model mechanisms, recent papers, and cited synthesis |
| `$cx-pytorch-tdd` | Python, PyTorch, and Lightning implementation and tests |
| `$cx-pytorch-quick-hpo` | Quick PyTorch tuning and candidate screening |
| `$cx-pytorch-full-hpo` | Full PyTorch tuning, evaluation, backtesting, and release candidates |
| `$cx-timeseries-modeling` | Heterogeneous multivariate time-series modeling |
| `$cx-rust-tdd` | Rust type design, ownership design, and cargo test/fmt/clippy |
| `$cx-common-module` | Reusable features, reusable classes, and public API design |
| `$cx-evidence` | Pre-handoff evidence review |

## Validation

```bash
python -m unittest discover -s tests
python tools/validate_skill_pack.py .
python tools/validate_cx_pack.py .
python tools/validate_single_source.py
```
