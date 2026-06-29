---
name: cx-workflow
description: Use for workflow handling, task routing, end-to-end development orchestration, selecting the right cx skills, docs/cx use-case flow, strict TDD/OOP, change-first work selection, and deciding whether research, release versioning, evidence review, or clarification is needed.
version: 0.1.0
---

# cx Workflow Router

## Purpose

Use this skill first when a user request needs workflow routing or several cx skills. It decides the smallest useful skill set and the execution order.

## Required First Steps

1. Create a visible todo list for any multi-step work.
2. Read the target project's `AGENTS.md` or repository instructions when present.
3. Read `docs/cx/00.project.md` or the relevant project-level `docs/cx` documents when present.
4. If a target scenario exists, read its use-case document, design document, `tasks/`, and `changes/`.
5. Unless adding a new task, conditional substep, or use case, inspect unfinished changes first and use them to decide the current work.
6. Recommend the smallest necessary cx skill combination before execution.

## Non-Negotiable Flow

1. Development tasks are use-case driven and live under `docs/cx`.
2. Every main success scenario has one folder.
3. Every scenario folder has a use-case document, design document, `tasks/`, and `changes/`.
4. A task folder starts at `01.` and owns one task document.
5. A task's basic measure is a class or type group.
6. A task touches one task document, one code file, and one unit-test file when needed.
7. Python, PyTorch, and Rust work follow strict TDD and strict OOP or equivalent type modeling.
8. Before starting work, ask one execution-mode question: finish documentation, tests, implementation, and validation directly, or ask after each completed task.
9. If the user does not explicitly choose per-task confirmation, default to direct completion; direct mode does not stop after use-case, design, task, or change documents are complete.
10. If one change spans multiple tasks, execute the ordered task list one task at a time; only per-task confirmation mode waits for user review after each task.

## Skill Selection

- Use `$cx-story` for use cases, main success scenarios, conditional substeps, tasks, and changes.
- Use `$cx-tdd` after the execution mode is known; direct mode proceeds into tests and implementation without a separate document-complete confirmation gate.
- Use `$cx-common-module` before adding reusable code, reusable classes, shared utilities, stable APIs, or common state.
- Use `$cx-pytorch-tdd` for Python, PyTorch, Lightning, tensors, training, or ML tests.
- Use `$cx-rust-tdd` for Rust implementation and testing.
- Use `$cx-pytorch-quick-hpo` and `$cx-pytorch-full-hpo` for staged tuning.
- Use `$cx-timeseries-modeling` for heterogeneous multivariate time-series design.
- Use `$cx-research` for model selection, papers, and cited synthesis.
- Use `$cx-version` for release versioning.
- Use `$cx-evidence` before handoff, merge, release, or when compliance is uncertain.

## Output

Return:

- Whether the request is programming, research, release, documentation, review, or operational work.
- Target `docs/cx` scenario and task if known.
- Current unfinished change if one controls the work.
- Selected skills and order.
- Execution mode.
- Narrowest validation commands expected.
