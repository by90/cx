---
name: cx-evidence
description: Use after code is written and before a task is marked complete, and before handoff, merge, or release. Reviews docs/cx story compliance, exact implementation agreement with use-case/design/task/change docs, duplication smells, full OOP, minimal reuse, business-semantic fit, verification output, change/task consistency, and document-sprawl problems. If review fails, the task is not complete.
version: 0.1.0
---

# cx Evidence Review

## Purpose

Review whether the work is supported by the current `docs/cx` use case, design document, task document, change document, default one-task/one-code-file discipline, explicit-test scope, full OOP, business semantics, and verification evidence. This is a mandatory post-code review gate. Any P0/P1/P2 finding means review fails and the task must remain incomplete until fixed and reviewed again.

## Review Focus

1. Document agreement: implementation must match the use case, design, task, and change documents exactly; no missing behavior, scope creep, or changed business meaning.
2. Business semantics: classes, methods, state, error exposure, and data flow must fit the domain language, not just pass tests or run technically.
3. Duplication smells: repeated checks, transformations, config reads, field passing, similar helpers, or several locals naming the same concept require `$cx-common-module` review.
4. Full OOP: state, lifecycle, invariants, and domain collaboration must use explicit classes, dataclasses, protocols, structs, enums, traits, or methods instead of loose dictionaries, magic strings, string dispatch, or dynamic attribute access.
5. Minimal implementation: no extra validation, extra fallbacks, extra exception wrapping, extra variable passing, extra parameters, redundant variable/parameter names, bloated files, sentence-like identifiers, or abstractions without real reuse.

## Checklist

1. Is all cx process documentation under `docs/cx`?
2. Does the target scenario have a use-case document, design document, `tasks/`, and `changes/`?
3. Did the agent inspect unfinished changes before choosing work?
4. Does the current task map to one task document?
5. Does the task name one production code file, and was any second code file split into another task?
6. Is the task measure a class or type group?
7. Was the execution mode recorded; did default work stop at the current task and code-file boundary unless continuation was explicitly requested?
8. Were unit tests or TDD explicitly requested before any test file was created, edited, or run?
9. When tests were explicitly requested, is there a failing-test-first record and mirrored test layout where applicable?
10. Did Python use `uv`, and did Rust use `cargo fmt` plus `cargo test` only when relevant?
11. Are verification commands and results recorded in the current task or change document?
12. Are there stray planning documents outside `docs/cx`?
13. Was reusable code checked through `$cx-common-module` before adding new common logic?
14. Is the implementation full OOP where state, lifecycle, invariants, or domain collaboration are present?
15. Is the code minimal and reusable, with no bloated files, overly long identifiers, sentence-like names, or duplicated logic?
16. Does the implementation cover every expected behavior in the task document and avoid behavior outside the task scope?
17. Does the implementation match the main success scenario, conditional substeps, success path, error exposure, and ending conditions?
18. Does the implementation match the design document's reusable entrypoints, common-code usage, decisions, and non-goals?
19. Are there no extra validations, prechecks, intermediate variables, parameters, variable-name duplicates, or parameter-name duplicates?
20. Is the review decision PASS; if not, does the task or change remain incomplete?

## Output

Return findings first, ordered by severity, with file paths and commands. Include `Review decision: PASS` or `Review decision: FAIL`. If review fails, state that the task remains incomplete. If no issues are found, state that clearly and list residual test gaps or risks.
