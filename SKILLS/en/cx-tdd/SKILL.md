---
name: cx-tdd
description: Use only when the current user request, existing task document, or change document explicitly asks for TDD, unit tests, failing tests, or red-green-refactor. Works from docs/cx changes and tasks with one task document, one production code file, one matching unit-test file, full object-oriented design, and verification evidence.
version: 0.1.0
---

# cx Explicit TDD

## Language Rules

- Use the package language for conversations, explanations, plans, summaries, review decisions, verification evidence, and cx documents. Do not mix languages inside prose fragments or term lists.
- In Chinese-package work, if an English identifier, command, path, API name, library, protocol, standard, proper name, or ambiguity-sensitive term must remain in English, explain its meaning, role, and local context in Chinese in the same sentence or an adjacent sentence. In English-package work, explain unavoidable non-English terms in English.

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
5. Python `src/`, `tests/`, and every subdirectory under them must contain blank `__init__.py` files.
6. Project imports use absolute imports from the repository root, for example `from src.config.config import Config`; tests must not modify `sys.path`.
7. Explicit Python unit tests must be discoverable and runnable from the VS Code test view; use unittest discovery arguments `-v -s ./tests -p *_test.py -t .`.
8. Rust uses built-in tests and `cargo test`.
9. Write the failing test first and report the expected failure.
10. Implement the smallest change that passes.
11. Refactor only within the current task boundary.
12. Do not weaken assertions to make a test pass.
13. After code passes explicitly requested tests, run `$cx-review` code-deliverable review for document agreement, duplication smells, full object-oriented design, minimal implementation, and business semantics.
14. If review fails, do not mark the task complete; fix implementation or docs, then rerun tests and review.
15. Record verification commands, results, `$cx-review` decision, `$cx-evidence` evidence decision, and residual gaps in the current task or change document.

## Python Expectations

- Use `uv` managed Python.
- Use `unittest` unless the project already uses another framework.
- Use full object-oriented design for state, lifecycle, invariants, and domain collaboration.
- TDD cannot justify preserving bloated entrypoints, useless tests, or future-extension wrappers. Tests should pin only behavior required by the current use case, not convenience wrappers, negative-index compatibility, clone methods, rebuild methods, padding methods, fallback validation, or future-extension entrypoints.
- If an implementation turns behavior expressible with a few fields, direct array slicing, standard-library semantics, or one clear constructor into hundreds or thousands of lines, the task remains incomplete until it is deleted back to the smallest functional entrypoint.
- Constructors and functions express configuration defaults as default parameters, for example `path=Config.default_config_file()` or `batch_size=config.train.batch_size`; function bodies store parameters on same-named fields.
- Common packages under `src/<subsystem>/` include package-local `readme.md` files that explain functional entrypoints and usage.
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
