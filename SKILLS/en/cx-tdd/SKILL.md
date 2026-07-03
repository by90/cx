---
name: cx-tdd
description: Use only when the current user request, existing task document, or change document explicitly asks for TDD, unit tests, failing tests, or red-green-refactor. Works from docs/cx changes and tasks with one task document, one production code file, one matching unit-test file, full OOP, and verification evidence.
version: 0.1.0
---

# cx Explicit TDD

## Purpose

Use this skill after the current task is known and TDD, unit tests, failing tests, or red-green-refactor are explicitly requested. Default implementation does not use this skill and does not create unit tests.

## Inputs

Read, in order:

1. Target scenario's use-case document.
2. Target scenario's design document.
3. Current unfinished change document.
4. Current task document.
5. The one code file named by the task.
6. The one matching unit-test file required by the explicit test request.

## Rules

1. Confirm that the current request, task document, or change document explicitly asks for TDD, unit tests, failing tests, or red-green-refactor; otherwise return to `$cx-workflow` default one-code-file implementation.
2. The task measure is a class or type group.
3. One task changes one production code file and one matching unit-test file.
4. Python tests mirror `src`: `src/subsystem/name.py` maps to `tests/subsystem/name_test.py`.
5. Rust uses built-in tests and `cargo test`.
6. Write the failing test first and report the expected failure.
7. Implement the smallest change that passes.
8. Refactor only within the current task boundary.
9. Do not weaken assertions to make a test pass.
10. After code passes explicitly requested tests, run `$cx-review` code-deliverable review for document agreement, duplication smells, full OOP, minimal implementation, and business semantics.
11. If review fails, do not mark the task complete; fix implementation or docs, then rerun tests and review.
12. Record verification commands, results, `$cx-review` decision, `$cx-evidence` evidence decision, and residual gaps in the current task or change document.

## Python Expectations

- Use `uv` managed Python.
- Use `unittest` unless the project already uses another framework.
- Use full OOP for state, lifecycle, invariants, and domain collaboration.
- Do not use dynamic reflection by default.
- Do not add command-line parameters to target-project scripts.

## Rust Expectations

- Model domain state with struct, enum, trait, and explicit `Result`.
- Avoid `unwrap`, `expect`, and `panic!` in production paths unless the invariant is local and documented.
- Run `cargo fmt` and `cargo test`; run `cargo clippy --all-targets --all-features` when practical.

## Output

Return:

- Current task and class/type measure.
- Test file and code file.
- Expected red failure.
- Implementation summary.
- Verification commands and results.
- `$cx-review` code-deliverable decision and `$cx-evidence` evidence decision. FAIL means the task remains incomplete.
- Execution mode, remaining risk, or next task gate.
