---
name: cx-bdd-tdd
description: Use for feature work, bug fixes, requirements, architecture changes, implementation planning, BDD scenarios, TDD tests, changelog updates, or AI-assisted coding workflow.
version: 1.0.0
---

# cx BDD/TDD Documentation-Set Workflow

## Purpose

Use this skill to keep development driven by one or more documentation sets under `docs/`. Small projects may use `docs/ENGINEERING_SPEC.md` and `docs/CHANGELOG.md`; multi-feature projects must use `docs/<feature-group>/ENGINEERING_SPEC.md` and `docs/<feature-group>/CHANGELOG.md`, with `docs/INDEX.md` or `docs/README.md` as the root index and instructions.

## Required workflow

1. Read `docs/INDEX.md` or `docs/README.md`, then read the target documentation set's `ENGINEERING_SPEC.md` and `CHANGELOG.md`.
2. If the work belongs to a new feature group, create `docs/<feature-group>/` first and register it in the root index.
3. Create or update exactly one relevant `CHANGE-YYYY-NNN` entry in the target documentation set.
4. Update existing engineering spec sections instead of creating new loose planning files.
5. Add or revise business scenarios before implementation details: main success scenarios, alternate scenarios, and exception scenarios.
6. Add test matrix entries before code changes, mapping every main success, alternate, or exception scenario to tests or an explicit reason it is not tested.
7. Write the narrow failing test first and run the command that proves the expected red failure.
8. Implement the smallest change that satisfies the failing test.
9. Refactor only after tests pass.
10. Record verification commands and results in the target engineering spec.
11. When adding or editing code, add beginner-friendly explanatory comments for code files, classes, functions, and important statements. Explain code intent line by line by default, except for pure formatting or repeated structural lines.

## BDD scenario format

```gherkin
Scenario: BDD-AREA-001 - Short behavior title
  Given <initial context>
  When <event>
  Then <observable outcome>
```

Include business rule, edge cases, related change ID, and related tests. Use behavior IDs that survive refactors.

## Business Scenario Structure

Every complex behavior must be split into:

```text
Main success scenario: the normal path and final observable result.
Alternate scenarios: valid branches, optional paths, different roles, or different input shapes.
Exception scenarios: invalid input, missing data, permission failure, external dependency failure, and required exceptions.
```

Exception scenarios must not merely say "handle failure"; they must describe the cause, system response, user-visible result, and whether logs or verification evidence are required.

## TDD matrix format

```text
BDD-AREA-001 -> tests/test_file.py::TestClass::test_behavior
Expected red: <why it fails before implementation>
Command: python -m unittest tests.test_file.TestClass.test_behavior
```

## Document rule

Do not create orphan `spec.md`, `plan.md`, `tasks.md`, or ad hoc design documents. If a plan is needed, write it into the target documentation set's `ENGINEERING_SPEC.md` Task Queue section.

When producing Chinese-language documentation, use Simplified Chinese. Long-lived documentation must live under the project's `docs/` directory.

BDD scenarios, test matrices, implementation plans, and verification evidence must be written in the target documentation set under the project's `docs/` directory. In multi-feature projects, the `docs/` root contains only indexes and instructions; feature documentation lives under `docs/<feature-group>/`.

## Documentation Set Layout

Single-feature projects may use:

```text
docs/ENGINEERING_SPEC.md
docs/CHANGELOG.md
```

Multi-feature projects use:

```text
docs/INDEX.md
docs/<feature-group>/ENGINEERING_SPEC.md
docs/<feature-group>/CHANGELOG.md
```
