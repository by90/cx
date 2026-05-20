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
8. Does the `docs/` root contain only indexes, instructions, and the version index, with concrete documents under numbered lowercase underscore feature folders such as `docs/001_feature_name/`?
9. Were orphan planning documents created?
10. Were reusable features, classes, or components searched across existing implementation, related skills, and the Reusable Capability Registry before extraction or explicit non-extraction?
11. Are Python tests `unittest` unless a project exception exists?
12. Does Python source live under `src/<subsystem>/`, do tests under `tests/` mirror the `src` structure, and do test files map one-to-one as `xx.py` -> `xx_test.py`?
13. Do added or edited source files and unit tests have file-level purpose explanations that name the main classes, functions, or test targets maintained by the file?
14. Do added or edited classes, functions, methods, and test methods explain responsibilities, parameter meanings, return values, or explicitly say there is no return value?
15. Do added or edited source files and unit tests follow the line-by-line intent-comment standard, with adjacent explanatory comments for every line of business logic?
16. After Python changes, was a Black default-format check run, for example `python -m black --check src tests tools` or the project equivalent?
17. Does Python express default behavior through default parameters, config objects, dataclasses, factories, or small methods instead of long branch stacks inside `__init__`?
18. Does the work follow the corresponding implementation skill's `## Minimal Implementation Discipline`: absolutely no unmaintainable pile-up code, no premature frameworkization, generalization, abstraction, or requirement-external validation?
19. Is the code minimal, small, and direct, and were reusable features, classes, or logic first searched and registered through `$cx-common-module`?
20. Does the code avoid non-OOP dynamic access such as `getattr`, `setattr`, `delattr`, monkey-patching, dynamic injection, or stringly typed dispatch; if unavoidable, is the reason documented, implementation isolated, and behavior tested?
21. For a generic capability, reusable feature, or reusable class, were the public entrypoint, normal call style, special-case entrypoint, instance or state lifecycle, state source, test coverage path for all source call sites, and non-goals defined first?
22. Does GUIDE or README show a normal-call example, and do tests cover that example?
23. Do tests cover the special entrypoint, lifecycle, state restoration, or test isolation path?
24. Are there helpers, wrappers, validators, or constants with only one call site and no real complexity to isolate?
25. Did the work avoid requirement-external validation, exception wrapping, dynamic construction, scanners, registries, or future extension entrypoints?
26. When adding a peer capability, config section, field, or data source, does the design avoid hard-coded export logic or control-flow branches?
27. Were Rust commands run when Rust code changed?
28. Does the work satisfy the prompt contract: goal, context, constraints, required workflow, verification, and deliverables?
29. Did ordinary non-programming tasks avoid creating BDD automatically, and did unclear boundaries trigger a user question first?
30. Does the final summary report commands run, results, skipped checks with reasons, and residual risk?

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
