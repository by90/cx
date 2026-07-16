# cx Codex Use-Case-Driven Workflow Pack

cx is a Codex skill package for disciplined human-AI development. It requires every project to maintain a root `AGENTS.md` that supplements global rules and every common package to have a caller tutorial. The agent reads current-domain tutorials and registered public entries before using the current use case, design, fixed task set, and temporary changes under `docs/cx`. Unit tests and TDD enter scope only when explicitly requested.

cx is not a component library or business implementation. It defines collaboration flow, document structure, task splitting, full object-oriented design, minimal reuse-first implementation, release versioning, and delivery evidence.

Project, use-case, design, task, topic, and research documents state only current valid facts. A change, implementation-direction shift, or code error in an existing story first enters `changes/` and is committed to Git. After unified review passes, the change file is deleted and the deletion is committed. Git preserves history.

Development code implements only the latest intent. Unless the user explicitly requests a specific validation or error behavior in the current request, do not add validation that raises an error and do not catch, translate, wrap, swallow, or fall back from errors. Preserve the original error type, message, and stack so execution stops. Delete every old interface, alias, adapter, bridge, compatibility branch, parameter, configuration, path, behavior, and related trace, and move all callers to the current entry.

After any deliverable, `$cx-review` runs artifact-quality review and the completion-evidence gate. A failure in either stage keeps the task unfinished and the active change file present.

Current package version: `0.1.2`. cx is still experimental and has not declared a stable `1.0.0` workflow.

Chinese README: [README.zh-CN.md](README.zh-CN.md). In this repository, Chinese workflow changes are completed first and then synchronized into English.

## Installable Content

This repository publishes the same workflow in two language packages:

- `SKILLS/zh`: Chinese skills.
- `SKILLS/en`: English skills.

Users do not need to install a `cx` command first. Install and update skills directly with `shskills`.

## Install Or Update

Local Codex skills should be installed or updated only from the repository's default `main` branch.

Recommended from a cloned repository:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install_cx_en.ps1
```

Raw `shskills` install:

```powershell
uv tool install shskills
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:USERPROFILE\.codex\skills" --subpath en --force --clean
```

If `CODEX_HOME` is set, use `$env:CODEX_HOME\skills` as the destination.

## Core Workflow

1. `$cx-workflow` classifies the request, creates a visible todo list, and selects the smallest required skills.
2. `$cx-doc` reads or creates project `AGENTS.md`, then follows its domain navigation to every common-package tutorial and registered public entry before `$cx-story` locates the current use case, design, and fixed tasks.
3. Each main success scenario has one folder, such as `docs/cx/01.create_user/`.
4. Each scenario folder contains `00.use_case.md`, `00.design.md`, `tasks/`, and `changes/`.
5. Each task is one Markdown file, such as `tasks/01.write_user_entity.md`.
6. Each change or code error in an existing story uses `changes/<change_name>.md`; commit it before work, delete it after review, and commit the deletion.
7. Establish the task set once for a new story. After creation, task count and identity stay fixed; rewrite original tasks for requirement changes, implementation changes, or code errors.
8. One main success scenario folder carries one user-goal use case. The main success scenario usually has 3 to 9 main steps from trigger to completed goal and does not bundle several mutually exclusive choices, page buttons, or complete tasks.
9. Conditional, alternate, and exception behavior must use substep numbering such as `1.1` or `2.1` under a concrete main step, and must say whether the flow returns to a step, ends this use case, or enters another use case.
10. If a main-success step needs its own actors, preconditions, steps, and conditional substeps, it is a sub-use case or separate use case and should move to its own scenario folder with an index in `docs/cx/00.project.md`.
11. Default execution completes the current task document, edits only that task's production code file, reports the result, and continues to another code file only when the user explicitly requests multi-task continuation.
12. By default, do not create, edit, or run unit tests. Use `$cx-tdd` only when the user request, existing task document, or change document explicitly asks for TDD, unit tests, or failing tests.
13. Development code implements only the latest intent and moves every caller to the current entry. Unless the user explicitly requests specific validation or error handling, preserve the original error type, message, and stack and stop execution without compatibility or fallback traces.
14. After any deliverable, `$cx-review` runs both artifact-quality review and the completion-evidence gate. Only both PASS permit completion and deletion of the active change file.
15. Only explicit per-task confirmation mode stops after each task and waits for review.
16. `$cx-tdd` owns the test-first main workflow. Add `$cx-pytorch-tdd` for explicitly requested Python, PyTorch, or Lightning tests and `$cx-rust-tdd` for explicitly requested Rust tests; neither language skill handles ordinary implementation.

## docs/cx Layout

```text
AGENTS.md
docs/cx/
docs/cx/00.project.md
docs/cx/docs/
docs/cx/docs/00.index.md
docs/cx/docs/01.market_data_server_protocol.md
docs/cx/notes/
docs/cx/notes/01.choose_time_series_model.md
docs/cx/01.create_user/
docs/cx/01.create_user/00.use_case.md
docs/cx/01.create_user/00.design.md
docs/cx/01.create_user/tasks/
docs/cx/01.create_user/tasks/01.write_user_entity.md
docs/cx/01.create_user/changes/
docs/cx/01.create_user/changes/adjust_user_entity_constraints.md
```

Project `AGENTS.md` is tailored to project goals, languages, toolchain, and common packages and lists required tutorials for each domain. `docs/cx/docs/` stores an independent caller tutorial for every common package and topic documents for stable technical processes. `docs/cx/notes/` stores current conclusions for specific research questions. Durable documents never preserve old/new comparisons or completed changes.

## Available Skills

| Skill | Purpose |
| --- | --- |
| `$cx-workflow` | Workflow routing and minimal skill selection |
| `$cx-story` | Use cases, main-success scenarios, conditional substeps, fixed tasks, and current state |
| `$cx-tdd` | Explicit test-first work, narrow failing tests, minimal implementation, and refactor |
| `$cx-changelog` | Registration, commit, execution, and completion deletion of temporary change files |
| `$cx-doc` | Common-package caller tutorials, stable topic documents, research notes, and project `AGENTS.md` tutorial navigation |
| `$cx-version` | Project-local `tools/semver.py`, `VERSION`, `docs/VERSIONS.md`, release tags, and release validation |
| `$cx-research` | Model selection, paper research, source filtering, and cited synthesis |
| `$cx-design` | Object-oriented design, responsibility splitting, domain objects, class naming, inheritance/composition, and data-access boundaries |
| `$cx-pytorch-tdd` | Adds `unittest`, mirrored test layout, shared real test data, and tensor checks to `$cx-tdd` |
| `$cx-pytorch-quick-hpo` | Lightweight PyTorch HPO on one tenth of complete-entity samples, including data, model, and training selection plus ablation and backtesting for 5 candidates |
| `$cx-pytorch-full-hpo` | Full-data PyTorch HPO that changes only batch size, learning rate, optimizer, and scheduler parameters, then trains, tests, and backtests all 5 candidates |
| `$cx-timeseries-modeling` | Heterogeneous multivariate time-series modeling and PyTorch Forecasting selection |
| `$cx-rust-tdd` | Adds Rust built-in tests, shared real test data, and `cargo` checks to `$cx-tdd` |
| `$cx-common-module` | Reusable features, reusable classes, functional entrypoints, and repeated logic convergence |
| `$cx-review` | Artifact-quality review, the completion-evidence gate, document agreement, and residual risk |

## Prompt Contract

A strong coding-agent prompt should include:

- Goal: behavior or result to change.
- Context: target `docs/cx` scenario, task, change, files, branch, or environment.
- Constraints: API, language rules, performance, compatibility, or style limits.
- Required workflow: cx skills to use and whether unit tests or TDD, research, versioning, or unified review are explicitly requested.
- Verification: commands, tests, screenshots, or checks expected.
- Deliverables: code, documents, change records, evidence, or summary.

## Release Versioning

- `VERSION` is the single source of truth.
- `packages/en/manifest.json` and `packages/zh/manifest.json` must match `VERSION`.
- Root `CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
- Release tags use annotated Git tags named `vX.Y.Z`.

Common commands:

```bash
python tools/cx_version.py show .
python tools/cx_version.py check .
python tools/validate_release.py .
```

Target projects copy `$cx-version`'s `scripts/semver.py` to `tools/semver.py` and use:

```bash
python tools/semver.py next feature-group --root .
python tools/semver.py next patch --root .
python tools/semver.py prepare <version> "<title>" --root .
```

## Pre-Release Validation

```bash
python tools/cx_version.py check .
python tools/validate_release.py .
```
