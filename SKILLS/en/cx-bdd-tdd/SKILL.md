---
name: cx-bdd-tdd
description: Use for feature work, bug fixes, requirements, architecture changes, implementation planning, BDD scenarios, TDD tests, changelog updates, or AI-assisted coding workflow.
version: 1.0.0
---

# cx BDD/TDD Single-Source Workflow

## Purpose

Use this skill to keep development driven by `docs/ENGINEERING_SPEC.md` and `docs/CHANGELOG.md`. The engineering spec is the single source of truth for behavior, design, tasks, tests, common modules, and verification evidence. The changelog is a compact historical index, not another requirements document.

## Required workflow

1. Read `docs/ENGINEERING_SPEC.md` and `docs/CHANGELOG.md` before planning.
2. Create or update exactly one relevant `CHANGE-YYYY-NNN` entry.
3. Update existing engineering spec sections instead of creating new planning files.
4. Add or revise BDD scenarios before implementation details.
5. Add test matrix entries before code changes.
6. Write the narrow failing test first and run the command that proves the expected red failure.
7. Implement the smallest change that satisfies the failing test.
8. Refactor only after tests pass.
9. Record verification commands and results in the engineering spec.

## BDD scenario format

```gherkin
Scenario: BDD-AREA-001 - Short behavior title
  Given <initial context>
  When <event>
  Then <observable outcome>
```

Include business rule, edge cases, related change ID, and related tests. Use behavior IDs that survive refactors.

## TDD matrix format

```text
BDD-AREA-001 -> tests/test_file.py::TestClass::test_behavior
Expected red: <why it fails before implementation>
Command: python -m unittest tests.test_file.TestClass.test_behavior
```

## Document rule

Do not create orphan `spec.md`, `plan.md`, `tasks.md`, or ad hoc design documents. If a plan is needed, write it into the Task Queue section of `docs/ENGINEERING_SPEC.md`.
