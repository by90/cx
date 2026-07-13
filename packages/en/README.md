# cx English Use-Case-Driven Workflow Pack

This directory contains the English package source for cx. The installable public source is `SKILLS/en`; this package directory keeps source, templates, guides, agents, and validation tools.

Do not install both English and Chinese packages into the same target project. Skill and agent names intentionally stay aligned across languages.

## Core Contract

cx is a workflow pack, not a component library. It requires agents to read `docs/cx/docs/` topic documents and registered common capabilities before using current use cases, designs, fixed tasks, and temporary changes. Durable documents keep only the latest state and Git preserves history.

Development code implements only the latest intent. Unless the user explicitly requests a specific validation or error behavior, preserve the original error type, message, and stack and stop execution. Delete every old interface, alias, adapter, bridge, compatibility branch, and related trace, and move all callers to the current entry.

After code, documentation, tutorials, research, design, or process deliverables, `$cx-review` runs artifact-quality review and the completion-evidence gate. A failure in either stage keeps the task unfinished and the active change file present.

```text
docs/cx/00.project.md
docs/cx/01.create_user/00.use_case.md
docs/cx/01.create_user/00.design.md
docs/cx/01.create_user/tasks/01.write_user_entity.md
docs/cx/01.create_user/changes/adjust_user_entity_constraints.md
```

Establish the task set once for a new story. After creation, task count, numbers, filenames, and identities remain fixed. Requirement changes, implementation changes, and code errors rewrite the original task rather than creating fix or modification tasks.
Change files under `changes/` guide unfinished work only. Commit them before implementation, delete them after review, and commit the deletion.

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
Use $cx-workflow and select the smallest required cx skills. First use $cx-doc to read docs/cx/docs topic documents and search registered common packages and real callers, then use $cx-story to locate the current use case, design, and original task. For a change, implementation-direction shift, or code error in an existing story, use $cx-changelog to create and commit a temporary change file, then rewrite the original task and implementation. Durable documents state only current facts. Do not create or edit unit tests unless I explicitly request them. Unless I explicitly request a specific validation or error behavior in the current request, do not add validation that raises an error and do not catch, translate, wrap, swallow, or fall back from errors; preserve the original error and stop execution. Implement only the latest interface and delete every compatibility trace. After deliverables, run both $cx-review stages; delete and commit the active change file only after both pass.
```

Python / PyTorch:

```text
Use $cx-story. Use a uv-managed Python interpreter. Use full object-oriented design for state, lifecycle, invariants, and domain collaboration. Do not write unit tests by default. Only when I explicitly ask for Python, PyTorch, or Lightning unit tests, TDD, or tensor tests, use $cx-tdd first and then add $cx-pytorch-tdd. Use unittest. For data-related tests, let tests/__init__.py load the test database once and share real objects. Do not use mock tests unless I explicitly request them.
```

Rust:

```text
Use $cx-story. Model state with structs, enums, and traits, and by default edit only the Rust code file bound to the current task. Only when I explicitly ask for Rust unit tests or TDD, use $cx-tdd first and then add $cx-rust-tdd. Data-related tests use one shared fixture to load real test-database records once. Do not use mock tests unless I explicitly request them. Run cargo fmt after Rust changes and clippy when practical; run cargo test only when tests are explicitly required.
```

Release:

```text
Use $cx-version. Work must happen on a short-lived local branch and merge to main only after user confirmation. Do not push work branches; the remote keeps only main and version tags. Only on main update VERSION, manifests, root changelog, validation, annotated vX.Y.Z tag, then push main and the release tag.
```

## Skill Map

| Skill | Purpose |
| --- | --- |
| `$cx-workflow` | Workflow routing and skill selection |
| `$cx-story` | Use cases, main-success scenarios, conditional substeps, fixed tasks, and current state |
| `$cx-tdd` | Explicit test-first work, narrow failing tests, minimal implementation, and refactor |
| `$cx-changelog` | Registration, commit, execution, and completion deletion of temporary change files |
| `$cx-doc` | Topic documents, common-package documentation, and research notes |
| `$cx-version` | Project-local `tools/semver.py`, SemVer, `VERSION`, `docs/VERSIONS.md`, and release tags |
| `$cx-research` | Model selection, model mechanisms, recent papers, and cited synthesis |
| `$cx-design` | Object-oriented design, responsibility splitting, domain objects, class naming, inheritance/composition, and data-access boundaries |
| `$cx-pytorch-tdd` | Adds Python, PyTorch, and Lightning rules to the `$cx-tdd` main workflow |
| `$cx-pytorch-quick-hpo` | Quick PyTorch tuning and candidate screening |
| `$cx-pytorch-full-hpo` | Full PyTorch tuning, evaluation, backtesting, and release candidates |
| `$cx-timeseries-modeling` | Heterogeneous multivariate time-series modeling |
| `$cx-rust-tdd` | Adds Rust built-in tests, shared real-data fixtures, and `cargo` checks to `$cx-tdd` |
| `$cx-common-module` | Reusable features, reusable classes, and functional entrypoint design |
| `$cx-review` | Artifact-quality review, the completion-evidence gate, and residual risk |

## Validation

```bash
python -m unittest discover -v -s ./tests -p "*_test.py" -t .
python tools/validate_skill_pack.py .
python tools/validate_cx_pack.py .
python tools/validate_single_source.py
```
