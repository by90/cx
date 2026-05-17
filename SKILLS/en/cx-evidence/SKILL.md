---
name: cx-evidence
description: Use before finalizing a task, branch, or pull request to check BDD/TDD compliance, test output, changelog/spec consistency, and document-sprawl problems.
version: 1.0.0
---

# cx Evidence Review

## Purpose

Review whether the work is actually supported by tests and the target documentation set. This is a delivery gate, not a style-only review.

## Review checklist

1. Does every change have a `CHANGE-*` entry?
2. Does every `CHANGE-*` entry map to the same documentation set's `ENGINEERING_SPEC.md`?
3. Were BDD scenarios added or updated for changed behavior?
4. Does every BDD scenario map to tests?
5. Was the red failure shown before implementation?
6. Are test commands and results recorded?
7. In multi-feature projects, does the `docs/` root contain only indexes and instructions, with feature documents under `docs/<feature-group>/`?
8. Were orphan planning documents created?
9. Were reusable components searched across existing implementation, related skills, and the Common Module Registry before extraction or explicit non-extraction?
10. Are Python tests `unittest` unless a project exception exists?
11. Were Rust commands run when Rust code changed?

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
