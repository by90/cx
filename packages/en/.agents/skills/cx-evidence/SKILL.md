---
name: cx-evidence
description: Use before handoff, merge, or release to review docs/cx story compliance, strict TDD evidence, test output, change/task consistency, and document-sprawl problems.
version: 0.1.0
---

# cx Evidence Review

## Purpose

Review whether the work is supported by the current `docs/cx` use case, task, change document, and executable verification. This is a delivery gate.

## Checklist

1. Is all cx process documentation under `docs/cx`?
2. Does the target scenario have a use-case document, design document, `tasks/`, and `changes/`?
3. Did the agent inspect unfinished changes before choosing work?
4. Does the current task map to one task document?
5. Does the task name one code file and one unit-test file when needed?
6. Is the task measure a class or type group?
7. Was the execution mode recorded; in direct mode, did the work continue through documents, tests, implementation, and validation; in per-task confirmation mode, did it wait for review after each task?
8. Is there a failing-test-first record or a clear reason no test was needed?
9. Did Python use `uv` and mirrored tests?
10. Did Rust use `cargo fmt` and `cargo test` when relevant?
11. Are verification commands and results recorded in the current task or change document?
12. Are there stray planning documents outside `docs/cx`?
13. Was reusable code checked through `$cx-common-module` before adding new common logic?

## Output

Return findings first, ordered by severity, with file paths and commands. If no issues are found, state that clearly and list residual test gaps or risks.
