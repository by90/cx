---
name: cx-workflow
description: Use for workflow handling, task routing, end-to-end development orchestration, selecting the right cx skills, docs/cx use-case flow, change-first work selection, default one-task/one-code-file execution, explicit tests, full OOP, minimal reusable code, and mandatory post-code review before a task can be considered complete.
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
6. A task touches one task document and one production code file; if a second code file is needed, split the next task first.
7. Unit tests are not default deliverables. Create, edit, or run unit tests only when the current user request, existing task document, or change document explicitly asks for unit tests, TDD, failing tests, or red-green-refactor.
8. Python, PyTorch, and Rust work follow full OOP or equivalent type modeling for state, lifecycle, invariants, and domain collaboration.
9. Code defaults to minimal, reusable, low-duplication implementation; avoid bloated files, overly long variable names, sentence-like identifiers, and abstractions without real reuse.
10. Default execution is one-task/one-code-file: complete the current task document, edit only the bound production code file, report the result, and continue to another code file only when the user explicitly asks for multi-task continuation.
11. After production code is written, run local code review before considering the task complete. If review fails, the task remains incomplete until the implementation or docs are fixed and reviewed again.
12. Mandatory review uses `$cx-evidence` and checks exact agreement with the use-case, design, task, and change documents; duplication smells; full OOP; minimal code with no extra validation, extra variable passing, or redundant variable/parameter names; and business-semantic fit.

## Skill Selection

- Use `$cx-story` for use cases, main success scenarios, conditional substeps, tasks, and changes.
- Use `$cx-tdd` only when the user or current docs explicitly ask for TDD, unit tests, failing tests, or red-green-refactor.
- Use `$cx-common-module` before adding reusable code, reusable classes, shared utilities, stable APIs, or common state.
- Use `$cx-pytorch-tdd` only for explicitly requested Python, PyTorch, Lightning, tensor, training, or ML tests.
- Use `$cx-rust-tdd` for Rust implementation and explicit Rust tests when requested.
- Use `$cx-pytorch-quick-hpo` and `$cx-pytorch-full-hpo` for staged tuning.
- Use `$cx-timeseries-modeling` for heterogeneous multivariate time-series design.
- Use `$cx-research` for model selection, papers, and cited synthesis.
- Use `$cx-version` for release versioning.
- Use `$cx-evidence` after code is written for mandatory local review, and before handoff, merge, release, or when compliance is uncertain.

## Output

Return:

- Whether the request is programming, research, release, documentation, review, or operational work.
- Target `docs/cx` scenario and task if known.
- Current unfinished change if one controls the work.
- Selected skills and order.
- Execution mode, including whether continuation beyond the current code file was explicitly requested.
- Narrowest validation commands expected.
- Review decision. FAIL means the task is not complete.
