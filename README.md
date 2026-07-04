# cx Codex Use-Case-Driven Workflow Pack

cx is a Codex skill package for disciplined human-AI software development. Its core goal is to make AI first anchor work in `docs/cx` use cases, design notes, tasks, and change documents, then implement Python, PyTorch, and Rust projects by default with one task document and one production code file. Unit tests and TDD enter scope only when explicitly requested.

cx is not a component library or business implementation. It defines collaboration flow, document structure, task splitting, full object-oriented design, minimal reuse-first implementation, release versioning, and delivery evidence.

After code, documentation, tutorials, research, design, process changes, release notes, or any other deliverable is produced, `$cx-review` is mandatory before the task, change, or deliverable can be considered complete. If review fails, the state stays incomplete until document mismatch, duplication smells, non-object-oriented design, bloated implementation, extra validation, extra variable passing, redundant naming, business-semantic drift, non-executable tutorials, weak research sources, or infeasible design is fixed.

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
5. Each task is one Markdown file, such as `tasks/01.write_user_entity.md`.
6. Each change is written under `changes/<change_name>.md` without a timestamp in the filename; changes record only later changes after implementation. AI checks unfinished changes before choosing work.
7. One task handles one task document and one production code file. Split another task before editing a second code file. Add one matching unit-test file only when unit tests or TDD are explicitly requested.
8. One main success scenario folder carries one user-goal use case. The main success scenario usually has 3 to 9 main steps from trigger to completed goal and does not bundle several mutually exclusive choices, page buttons, or complete tasks.
9. Conditional, alternate, and exception behavior must use substep numbering such as `1.1` or `2.1` under a concrete main step, and must say whether the flow returns to a step, ends this use case, or enters another use case.
10. If a main-success step needs its own actors, preconditions, steps, and conditional substeps, it is a sub-use case or separate use case and should move to its own scenario folder with an index in `docs/cx/00.project.md`.
11. Default execution completes the current task document, edits only that task's production code file, reports the result, and continues to another code file only when the user explicitly requests multi-task continuation.
12. By default, do not create, edit, or run unit tests. Use `$cx-tdd` only when the user request, existing task document, or change document explicitly asks for TDD, unit tests, or failing tests.
13. After any deliverable is produced, `$cx-review` must run the matching local review; before handoff, `$cx-evidence` verifies review decisions and evidence. Only both PASS allow the task or change to be marked complete.
14. Only explicit per-task confirmation mode stops after each task and waits for review.
15. `$cx-pytorch-tdd` is added only for explicit Python/PyTorch tests; `$cx-rust-tdd` handles Rust implementation and explicit tests; `$cx-common-module` adds reusable-entrypoint constraints.

## docs/cx Layout

```text
docs/cx/
docs/cx/00.project.md
docs/cx/01.create_user/
docs/cx/01.create_user/00.use_case.md
docs/cx/01.create_user/00.design.md
docs/cx/01.create_user/tasks/
docs/cx/01.create_user/tasks/01.write_user_entity.md
docs/cx/01.create_user/changes/
docs/cx/01.create_user/changes/adjust_user_entity_constraints.md
```

All cx scenario, task, process, and change documents belong under `docs/cx`. Documents elsewhere are unrelated to cx.

## Available Skills

| Skill | Purpose |
| --- | --- |
| `$cx-workflow` | Workflow routing and minimal skill selection |
| `$cx-story` | Use cases, main success scenarios, conditional substeps, tasks, and changes |
| `$cx-tdd` | Explicit test-first work, narrow failing tests, minimal implementation, and refactor |
| `$cx-changelog` | `changes/` documents, release notes, and audit trails |
| `$cx-version` | Project-local `tools/semver.py`, `VERSION`, `docs/VERSIONS.md`, release tags, and release validation |
| `$cx-research` | Model selection, paper research, source filtering, and cited synthesis |
| `$cx-design` | Object-oriented design, responsibility splitting, domain objects, class naming, inheritance/composition, and data-access boundaries |
| `$cx-pytorch-tdd` | Python, PyTorch, Lightning, tensors, training, and ML tests |
| `$cx-pytorch-quick-hpo` | Quick PyTorch tuning, field contribution research, feature sets, and candidates |
| `$cx-pytorch-full-hpo` | Full PyTorch tuning, full-data training, evaluation, backtesting, and candidate selection |
| `$cx-timeseries-modeling` | Heterogeneous multivariate time-series modeling and PyTorch Forecasting selection |
| `$cx-rust-tdd` | Rust type design, ownership design, optional explicit tests, `cargo fmt`, `cargo test`, and `clippy` |
| `$cx-common-module` | Reusable features, reusable classes, functional entrypoints, and repeated logic convergence |
| `$cx-review` | Mandatory local review after code, documentation, tutorial, research, design, or process-change deliverables |
| `$cx-evidence` | Pre-handoff evidence review, review-decision checks, document agreement, and residual risk |

## Prompt Contract

A strong coding-agent prompt should include:

- Goal: behavior or result to change.
- Context: target `docs/cx` scenario, task, change, files, branch, or environment.
- Constraints: API, language rules, performance, compatibility, or style limits.
- Required workflow: cx skills to use and whether unit tests or TDD, research, versioning, or evidence review are explicitly requested.
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
