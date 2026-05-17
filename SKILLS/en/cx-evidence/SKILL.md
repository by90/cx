---
name: cx-evidence
description: Use before finalizing a task, branch, or pull request to check BDD/TDD compliance, non-programming task verification, test output, changelog/spec single-source consistency, branch flow, and document-sprawl problems.
version: 1.0.0
---

# cx Evidence Review

## Purpose

Review whether the work is actually supported by tests and the target documentation set. This is a delivery gate, not a style-only review.

## Review checklist

1. Does every change have a `CHANGE-*` entry in the target documentation set's `CHANGELOG.md`?
2. Does the same documentation set's `ENGINEERING_SPEC.md` avoid concrete `CHANGE-*` IDs?
3. Were BDD scenarios added or updated for changed behavior?
4. Does every programming-behavior BDD scenario map to tests?
5. Was the red failure shown before implementation for programming tasks?
6. Did non-programming tasks avoid TDD and use checklists, review evidence, or delivery confirmation instead?
7. Are test commands and results recorded?
8. In multi-feature projects, does the `docs/` root contain only indexes, instructions, and `VERSIONS.md`, with feature documents under `docs/<feature-group>/`?
9. Does each feature-group folder include `ENGINEERING_SPEC.md`, `CHANGELOG.md`, and `GUIDE.md` when needed?
10. Were orphan planning documents created?
11. Were reusable components searched across existing implementation, related skills, prior projects, and the Common Module Registry before extraction or explicit non-extraction?
12. Was the work completed on a feature-group or change branch, merged into `dev`, and followed by deleting the work branch?
13. When a feature group is ready to release, was `docs/VERSIONS.md` updated with the version tool?
14. Are Python tests `unittest` unless a project exception exists?
15. Were Rust commands run when Rust code changed?

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
