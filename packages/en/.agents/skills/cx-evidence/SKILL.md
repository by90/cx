---
name: cx-evidence
description: Use before marking a task complete and before handoff, merge, or release. Reviews docs/cx story compliance, `$cx-review` decisions for code/documentation/tutorial/research/design deliverables, verification output, change/task consistency, document sprawl, business semantics, and residual risk. Missing or failed required review means the task, change, or deliverable is not complete.
version: 0.1.0
---

# cx Evidence Review

## Purpose

Review whether the work is supported by the current `docs/cx` use case, design document, task document, change document, explicit-test scope, artifact-specific `$cx-review` decisions, business semantics, and verification evidence. This is a task, change, and handoff evidence gate. Any P0/P1/P2 finding, missing required review, or failed required review means the task, change, or deliverable remains incomplete until fixed and reviewed again.

## Evidence Focus

1. Review completeness: every produced artifact type has a `$cx-review` PASS record; code, documentation, tutorial, research, design, and process review do not substitute for each other.
2. Document agreement: task, change, and review decisions match the use case, design, task document, change document, and user request.
3. Business semantics: deliverables carry the right business meaning, not merely valid formatting or runnable commands.
4. Verification evidence: commands, screenshots, sources, manual checks, or other evidence truly cover the current deliverables; unit tests count only when explicitly requested.
5. Completion status: no missing-evidence, unreviewed, review-failed, user-unconfirmed, or blocked work is written as complete.

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
11. Does every produced code, documentation, tutorial, research, design, process-change, or release-note artifact have a `$cx-review` PASS decision?
12. If any artifact type lacks review, does it remain incomplete rather than being written as complete?
13. Are verification commands and results recorded in the current task or change document?
14. Are there stray planning documents outside `docs/cx`?
15. Was reusable code checked through `$cx-common-module` before adding new common logic?
16. Is the implementation full OOP where state, lifecycle, invariants, or domain collaboration are present?
17. Is the code minimal and reusable, with no bloated files, overly long identifiers, sentence-like names, or duplicated logic?
18. Does the implementation cover every expected behavior in the task document and avoid behavior outside the task scope?
19. Does the implementation match the main success scenario, conditional substeps, success path, error exposure, and ending conditions?
20. Does the implementation match the design document's reusable entrypoints, common-code usage, decisions, and non-goals?
21. Are there no extra validations, prechecks, intermediate variables, parameters, variable-name duplicates, or parameter-name duplicates?
22. Do documentation deliverables have a clear audience, goal, scope, status, single home, and no stale or unsupported claims?
23. Are tutorial deliverables executable in order, with prerequisites, commands, expected outputs, and failure handling?
24. Do research deliverables define the question, date window, inclusion/exclusion criteria, target reader, source quality, limits, and citations for non-obvious claims?
25. Do design deliverables state target behavior, constraints, invariants, public entrypoints, reuse boundaries, non-goals, tradeoffs, and implementable task boundaries?
26. Are all required artifact review decisions PASS; if not, does the task, change, or deliverable remain incomplete?

## Output

Return findings first, ordered by severity, with file paths and commands. Include `Review decision: PASS` or `Review decision: FAIL`. If review fails, state that the task, change, or deliverable remains incomplete. If no issues are found, state that clearly and list residual evidence gaps or risks.
