---
name: cx-evidence
description: Use before finalizing a task, branch, or pull request to check BDD/TDD compliance, test output, changelog/spec consistency, and document-sprawl problems.
version: 0.1.0
---

# cx Evidence Review

## Purpose

Review whether the work is actually supported by tests and the target documentation set. This is a delivery gate, not a style-only review.

## Review checklist

1. Does every change have a `CHANGE-*` entry?
2. Does every `CHANGE-*` entry map to the same documentation set's `ENGINEERING_SPEC.md`?
3. Were BDD scenarios added or updated for changed behavior?
4. Does every BDD scenario map to tests?
5. After documents were complete and before testing or implementation began, was there explicit user confirmation?
6. Was the red failure shown before implementation?
7. Are test commands and results recorded?
8. In multi-feature projects, does the `docs/` root contain only indexes and instructions, with feature documents under `docs/<feature-group>/`?
9. Were orphan planning documents created?
10. Were reusable components searched across existing implementation, related skills, and the Common Module Registry before extraction or explicit non-extraction?
11. Are Python tests `unittest` unless a project exception exists?
12. Does Python source live under `src/<subsystem>/`, do tests under `tests/` mirror the `src` structure, and do test files map one-to-one as `xx.py` -> `xx_test.py`?
13. Do added or edited code files, classes, functions, and every line of business code have explanatory comments?
14. Does Python express default behavior through default parameters, config objects, dataclasses, factories, or small methods instead of long branch stacks inside `__init__`?
15. Does the work follow the corresponding implementation skill's `## Minimal Implementation Discipline`: absolutely no unmaintainable pile-up code, no premature frameworkization, generalization, abstraction, or requirement-external validation?
16. Is the code minimal, small, and direct, and was reusable logic first searched and registered through `$cx-common-module`?
17. Does the code avoid non-OOP dynamic access such as `getattr`, `setattr`, `delattr`, monkey-patching, dynamic injection, or stringly typed dispatch; if unavoidable, is the reason documented, implementation isolated, and behavior tested?
18. Were Rust commands run when Rust code changed?
19. Does the work satisfy the prompt contract: goal, context, constraints, required workflow, verification, and deliverables?
20. Does the final summary report commands run, results, skipped checks with reasons, and residual risk?

## Output format

```text
Findings:
1. [severity] file:line - issue
   Evidence:
   Fix:

Verified:
- command -> result

Missing evidence:
- ...
```
