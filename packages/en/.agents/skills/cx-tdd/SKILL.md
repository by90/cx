---
name: cx-tdd
description: Use for strict test-driven development after the docs/cx story task and execution mode are known: red-green-refactor, narrow failing tests, one task document, one code file, one matching unit-test file, strict OOP, and verification evidence.
version: 0.1.0
---

# cx Strict TDD

## Purpose

Use this skill after the current task and execution mode are known. If the user has not explicitly chosen per-task confirmation, proceed directly from documents into the narrowest failing test, the smallest implementation, and a focused refactor.

## Inputs

Read, in order:

1. Target scenario's use-case document.
2. Target scenario's design document.
3. Current unfinished change document.
4. Current task document.
5. The one code file named by the task.
6. The one matching unit-test file when needed.

## Rules

1. Confirm the execution mode first; if the user did not explicitly choose per-task confirmation, direct mode proceeds into tests, implementation, and validation without a separate document-complete confirmation gate.
2. The task measure is a class or type group.
3. One task changes one code file and, when needed, one matching unit-test file.
4. Python tests mirror `src`: `src/subsystem/name.py` maps to `tests/subsystem/name_test.py`.
5. Rust uses built-in tests and `cargo test`.
6. Write the failing test first and report the expected failure.
7. Implement the smallest change that passes.
8. Refactor only within the current task boundary.
9. Do not weaken assertions to make a test pass.
10. Record verification commands and results in the current task or change document.

## Python Expectations

- Use `uv` managed Python.
- Use `unittest` unless the project already uses another framework.
- Use strict OOP for state, lifecycle, invariants, and domain collaboration.
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
- Execution mode, remaining risk, or next task gate.
