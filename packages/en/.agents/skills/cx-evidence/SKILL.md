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
12. Were Rust commands run when Rust code changed?
13. Does the work satisfy the prompt contract: goal, context, constraints, required workflow, verification, and deliverables?
14. Does the final summary report commands run, results, skipped checks with reasons, and residual risk?

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
