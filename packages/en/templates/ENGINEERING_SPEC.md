# ENGINEERING_SPEC.md

This is the long-lived engineering specification for one ordered feature group. Single-feature projects may place it at `docs/ENGINEERING_SPEC.md`; multi-feature projects should place it at `docs/1.Configuration System/ENGINEERING_SPEC.md` and link it from `docs/INDEX.md`.

## 0. Document Rules

- This feature group's architecture, task queue, test matrix, reusable component decisions, and verification evidence live here.
- BDD scenarios live in the sibling `BDD.md`, whose heading and `Feature:` name must match the folder name.
- The sibling `CHANGELOG.md` records this feature group's history only.
- Every `CHANGE-*` entry must appear in both the sibling `CHANGELOG.md` and this file.
- Every new or changed behavior should have a main success scenario, necessary alternate scenarios, and exception scenarios in `BDD.md`.
- Every BDD scenario should map to tests before implementation.

## 1. Product Intent

TODO: Describe the product, users, current goals, and non-goals.

## 2. Change Index

- CHANGE-2026-001: Initial cx workflow installation.

## 3. Behavior Map

| Area | Behavior | BDD IDs | Notes |
| --- | --- | --- | --- |
| Workflow | Development starts from the target documentation set and changelog | BDD-CX-001 | Initial policy |

## 4. BDD Scenarios

### Scenario: BDD-CX-001 - Development uses the documentation-set BDD/TDD workflow

Main success scenario:

Given a developer asks for a feature or bugfix
When the assistant plans and implements the work
Then it updates the target engineering spec and changelog before implementation
And it writes failing tests before production code
And it records verification evidence after the tests pass

Alternate scenarios:

- Single-feature projects may use `docs/ENGINEERING_SPEC.md` and `docs/CHANGELOG.md` directly.
- Multi-feature projects should use `docs/<feature-group>/ENGINEERING_SPEC.md` and the sibling `CHANGELOG.md`.

Exception scenarios:

- If the target documentation set is missing, create it first and register it in `docs/INDEX.md`.
- If a `CHANGE-*` appears only in changelog and does not map back to the engineering spec, delivery validation must fail.

- Related change: CHANGE-2026-001
- Business rule: Work must remain searchable and auditable in the target documentation set.
- Edge cases: urgent bugfixes, refactors, Python ML work, Rust UI work, reusable module extraction.
- Related tests: `tools/validate_single_source.py`, `tools/validate_skill_pack.py`, `tools/validate_cx_pack.py`

## 5. Technical Architecture

TODO: Describe important modules, interfaces, data flow, error handling, and integration boundaries.

## 6. Test Matrix

| BDD ID | Test command | Expected red | Status |
| --- | --- | --- | --- |
| BDD-CX-001 | `python tools/validate_single_source.py .` | Fails if docs are missing, orphan docs exist, or change IDs are not mapped | Active |

## 7. Task Queue

| Task | Source | Status | Notes |
| --- | --- | --- | --- |
| Install cx package | CHANGE-2026-001 | done | Replace TODO sections with project-specific content. |

## 8. Reusable Component Registry

| Component | Purpose | Public API | Owners/Callers | Tests | Migration notes |
| --- | --- | --- | --- | --- | --- |
| indexed_series | Long-series wrapper indexed by entity, category, or window | TODO | TODO | TODO | TODO |
| progress_ui | Multi-task progress state and adapters | TODO | TODO | TODO | TODO |
| ragged_tensors | Variable-length tensor utilities | TODO | TODO | TODO | TODO |
| lightning_test_harness | Tiny deterministic Lightning test fixtures | TODO | TODO | TODO | TODO |
| gpui_state_model | Pure Rust UI state and reducers | TODO | TODO | TODO | TODO |

## 9. Verification Evidence

| Date | Change | Command | Result | Notes |
| --- | --- | --- | --- | --- |
| 2026-05-13 | CHANGE-2026-001 | `python tools/validate_single_source.py examples/python_ml_project` | pass | Example validation |

## 10. Decision Log

| Date | Decision | Reason | Consequences |
| --- | --- | --- | --- |
| 2026-05-13 | Use a target engineering documentation set and changelog | Prevent document sprawl and keep AI tasks searchable | Requires discipline and validation |
