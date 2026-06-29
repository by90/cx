# cx Codex Use-Case-Driven TDD Workflow Pack

cx is a Codex skill package for disciplined human-AI software development. Its core goal is to make AI first anchor work in `docs/cx` use cases, design notes, tasks, and change documents, then implement Python, PyTorch, and Rust projects with strict TDD and strict OOP or equivalent type modeling.

cx is not a component library or business implementation. It defines collaboration flow, document structure, task splitting, test-first work, release versioning, and delivery evidence.

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
2. `$cx-story` maintains use cases, design notes, tasks, and changes under `docs/cx`.
3. Each main success scenario has one folder, such as `docs/cx/01.create_user/`.
4. Each scenario folder contains `00.use_case.md`, `00.design.md`, `tasks/`, and `changes/`.
5. Each task is a folder, such as `tasks/01.write_user_entity/00.task.md`.
6. Each change is written under `changes/<timestamp>-task<id>-<task_name>.md`; AI checks unfinished changes before choosing work.
7. One task handles one task document, one code file, and one matching unit-test file when needed.
8. One main success scenario folder carries one user-goal use case. The main success scenario usually has 3 to 9 steps from trigger to completed goal and does not bundle several mutually exclusive choices, page buttons, or complete tasks.
9. If a main-success step needs its own actors, preconditions, steps, and branches, it is a sub-use case or separate use case and should move to its own scenario folder with an index in `docs/cx/00.project.md`.
10. Before work starts, the agent asks one execution-mode question: finish documentation, tests, implementation, and validation directly, or ask after each completed task.
11. If the user does not explicitly choose per-task confirmation, the default is direct completion; document completion does not stop the flow.
12. Only per-task confirmation mode stops after each task and waits for review.
13. `$cx-tdd` runs narrow failing tests, minimal implementation, and refactor. `$cx-pytorch-tdd`, `$cx-rust-tdd`, and `$cx-common-module` add language and reusable-entrypoint constraints.

## docs/cx Layout

```text
docs/cx/
docs/cx/00.project.md
docs/cx/01.create_user/
docs/cx/01.create_user/00.use_case.md
docs/cx/01.create_user/00.design.md
docs/cx/01.create_user/tasks/
docs/cx/01.create_user/tasks/01.write_user_entity/00.task.md
docs/cx/01.create_user/changes/
docs/cx/01.create_user/changes/20260629T120000-task01-write_user_entity.md
```

All cx scenario, task, process, and change documents belong under `docs/cx`. Documents elsewhere are unrelated to cx.

## Available Skills

| Skill | Purpose |
| --- | --- |
| `$cx-workflow` | Workflow routing and minimal skill selection |
| `$cx-story` | Use cases, main success scenarios, branch scenarios, tasks, and changes |
| `$cx-tdd` | Strict test-first work, narrow failing tests, minimal implementation, and refactor |
| `$cx-changelog` | `changes/` documents, release notes, and audit trails |
| `$cx-version` | Project-local `tools/semver.py`, `VERSION`, `docs/VERSIONS.md`, release tags, and release validation |
| `$cx-research` | Model selection, paper research, source filtering, and cited synthesis |
| `$cx-pytorch-tdd` | Python, PyTorch, Lightning, tensors, training, and ML tests |
| `$cx-pytorch-quick-hpo` | Quick PyTorch tuning, field contribution research, feature sets, and candidates |
| `$cx-pytorch-full-hpo` | Full PyTorch tuning, full-data training, evaluation, backtesting, and candidate selection |
| `$cx-timeseries-modeling` | Heterogeneous multivariate time-series modeling and PyTorch Forecasting selection |
| `$cx-rust-tdd` | Rust type design, ownership design, built-in tests, `cargo fmt`, `cargo test`, and `clippy` |
| `$cx-common-module` | Reusable features, reusable classes, public entrypoints, and repeated logic convergence |
| `$cx-evidence` | Pre-handoff evidence review |

## Prompt Contract

A strong coding-agent prompt should include:

- Goal: behavior or result to change.
- Context: target `docs/cx` scenario, task, change, files, branch, or environment.
- Constraints: API, language rules, performance, compatibility, or style limits.
- Required workflow: cx skills to use and whether TDD, research, versioning, or evidence review is needed.
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
