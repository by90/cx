---
name: cx-evidence
description: Use before marking a task complete and before handoff, merge, or release. Reviews docs/cx story compliance, `$cx-review` decisions for code/documentation/tutorial/research/design deliverables, verification output, change/task consistency, document sprawl, business semantics, and residual risk. Missing or failed required review means the task, change, or deliverable is not complete.
version: 0.1.0
---

# cx Evidence Review

## Language Rules

- Use the package language for conversations, explanations, plans, summaries, review decisions, verification evidence, and cx documents. Do not mix languages inside prose fragments or term lists.
- In Chinese-package work, if an English identifier, command, path, API name, library, protocol, standard, proper name, or ambiguity-sensitive term must remain in English, explain its meaning, role, and local context in Chinese in the same sentence or an adjacent sentence. In English-package work, explain unavoidable non-English terms in English.

## Purpose

Review whether the work is supported by the current `docs/cx` use case, design document, task document, change document, explicit-test scope, artifact-specific `$cx-review` decisions, business semantics, and verification evidence. This is a task, change, and handoff evidence gate. Any P0/P1/P2 finding, missing required review, or failed required review means the task, change, or deliverable remains incomplete until fixed and reviewed again.

## Evidence Focus

1. Review completeness: every produced artifact type has a `$cx-review` PASS record; code, documentation, tutorial, research, design, and process review do not substitute for each other.
2. Document agreement: task, change, and review decisions match the use case, design, task document, change document, and user request.
3. Business semantics: deliverables carry the right business meaning, not merely valid formatting or runnable commands.
4. Verification evidence: commands, screenshots, sources, manual checks, or other evidence truly cover the current deliverables; unit tests count only when explicitly requested.
5. Completion status: no missing-evidence, unreviewed, review-failed, user-unconfirmed, or blocked work is written as complete.
6. Language evidence: conversation summaries, cx documents, review decisions, and verification evidence use the package language without mixed-language fragments. Chinese-package work explains retained English in Chinese.

## Checklist

1. Is all cx process documentation under `docs/cx`?
2. Does the target scenario have a use-case document, design document, `tasks/`, and `changes/`?
3. Did the agent inspect unfinished changes before choosing work?
4. Does the current task map to one task document?
5. Does each task file use `tasks/NN.task_name.md`, and is there no generic `00.task.md` task file?
6. Does the task name one production code file, and was any second code file split into another task?
7. Is the task measure a class or type group?
8. Was the execution mode recorded; did default work stop at the current task and code-file boundary unless continuation was explicitly requested?
9. Do documents state concrete facts, concrete actions, and concrete decisions, without filler, repeated goals, missing "what to do", or undefined invented terms?
10. Do project documents, use cases, designs, and tasks avoid repeating the same goals across all documents?
11. Do change documents record only later changes after implementation, and do change filenames have no timestamps?
12. Were unit tests or TDD explicitly requested before any test file was created, edited, or run?
13. When tests were explicitly requested, is there a failing-test-first record and mirrored test layout where applicable?
14. Do Python `src/`, `tests/`, and every subdirectory under them contain blank `__init__.py` files?
15. Do project imports use absolute imports from the repository root, and do tests avoid modifying `sys.path`?
16. Are explicit Python unit tests discoverable from the VS Code test view, or was the equivalent command `uv run python -m unittest discover -v -s ./tests -p "*_test.py" -t .` run?
17. Did Python use `uv`, and did Rust use `cargo fmt` plus `cargo test` only when relevant?
18. Does every produced code, documentation, tutorial, research, design, process-change, or release-note artifact have a `$cx-review` PASS decision?
19. If any artifact type lacks review, does it remain incomplete rather than being written as complete?
20. Are verification commands and results recorded in the current task or change document?
21. Are there stray planning documents outside `docs/cx`?
22. Was reusable code checked through `$cx-common-module` before adding new common logic?
23. Is the implementation full OOP where state, lifecycle, invariants, or domain collaboration are present?
24. Is the code minimal and reusable, with no bloated files, overly long identifiers, sentence-like names, or duplicated logic?
25. Has all bloated code been removed from source code, tests, scripts, tools, examples, and workflow-generated code: no behavior expressible with a few fields, direct array slicing, standard-library semantics, or one clear constructor is expanded into hundreds or thousands of lines; and no unrequired protocol inheritance, convenience wrappers, clone methods, rebuild methods, padding methods, negative-index compatibility, fallback validation, debug entrypoints, future-extension entrypoints, or test-only entrypoints remain?
26. Are configuration defaults written as default parameters, for example `path=Config.default_config_file()` or `batch_size=config.train.batch_size`, and stored on same-named fields?
27. Do common packages under `src/<subsystem>/` include package-local `readme.md` files that list public APIs and usage?
28. Does the implementation cover every expected behavior in the task document and avoid behavior outside the task scope?
29. Does the implementation match the main success scenario, conditional substeps, success path, error exposure, and ending conditions?
30. Does the implementation match the design document's reusable entrypoints, common-code usage, decisions, and non-goals?
31. Are there no extra validations, prechecks, intermediate variables, parameters, variable-name duplicates, or parameter-name duplicates?
32. Do documentation deliverables have a clear audience, goal, scope, status, single home, and no stale or unsupported claims?
33. Are tutorial deliverables executable in order, with prerequisites, commands, expected outputs, and failure handling?
34. Do research deliverables define the question, date window, inclusion/exclusion criteria, target reader, source quality, limits, and citations for non-obvious claims?
35. Do design deliverables state target behavior, constraints, invariants, public entrypoints, reuse boundaries, non-goals, tradeoffs, and implementable task boundaries?
36. Are all required artifact review decisions PASS; if not, does the task, change, or deliverable remain incomplete?
37. Do conversation summaries, cx documents, review decisions, and verification evidence follow the language rules? In Chinese-package work, is any retained English term, abbreviation, or proper name explained in Chinese in the same sentence or an adjacent sentence?

## Output

Return findings first, ordered by severity, with file paths and commands. Include `Review decision: PASS` or `Review decision: FAIL`. If review fails, state that the task, change, or deliverable remains incomplete. If no issues are found, state that clearly and list residual evidence gaps or risks.
