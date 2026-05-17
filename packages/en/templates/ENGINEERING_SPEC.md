# ENGINEERING_SPEC.md

This is the long-lived engineering specification for one feature group. Single-feature projects may place it at `docs/ENGINEERING_SPEC.md`; multi-feature projects should place it at `docs/<feature-group>/ENGINEERING_SPEC.md` and link it from `docs/INDEX.md`.

## 0. Document Rules

- This feature group's business goals, BDD scenarios, architecture, test matrix, reusable component decisions, and verification evidence live here.
- The sibling `CHANGELOG.md` is the only ordered record of changes and change tasks; do not copy concrete change IDs into this file.
- This file must not contain concrete change IDs; update the sibling `CHANGELOG.md` when you need to schedule change tasks.
- Every new or changed business behavior should have a main success scenario, necessary alternate scenarios, and exception scenarios.
- Programming tasks map behavior to tests before implementation; non-programming tasks do not use TDD and instead record checklists, review evidence, or delivery confirmation.

## 1. Product Intent

TODO: Describe the product, users, current goals, and non-goals.

## 2. Feature Scope

| Scope | Included | Excluded | Notes |
| --- | --- | --- | --- |
| Workflow | Use the target documentation set for business behavior and evidence | Ordering change tasks in the engineering spec | Change order is maintained only in `CHANGELOG.md` |

## 3. Behavior Map

| Area | Behavior | BDD IDs | Notes |
| --- | --- | --- | --- |
| Workflow | Development starts from the target documentation set and changelog | BDD-CX-001 | Initial policy |

## 4. BDD Scenarios

### Scenario: BDD-CX-001 - Development uses the documentation-set BDD workflow

Main success scenario:

Given a developer asks for a feature or bugfix
When the assistant plans and implements the work
Then it describes business behavior and acceptance criteria in the target engineering spec
And it records ordered change tasks in the sibling changelog
And it writes failing tests before production code for programming behavior
And it records verification evidence after tests or checks pass

Alternate scenarios:

- Single-feature projects may use `docs/ENGINEERING_SPEC.md` and `docs/CHANGELOG.md` directly.
- Multi-feature projects should use `docs/<feature-group>/ENGINEERING_SPEC.md`, the sibling `CHANGELOG.md`, and optional `GUIDE.md`.
- Non-programming documentation, research, installation, configuration, or review tasks do not start TDD; record goals, check results, and evidence instead.
- Before extracting reusable components, search the current project, related skills, prior projects, and this feature group's Reusable Component Registry.

Exception scenarios:

- If the target documentation set is missing, create the feature-group folder first and register it in `docs/INDEX.md`.
- If a concrete change ID appears in this file, delivery validation must fail and the entry must move to the sibling `CHANGELOG.md`.
- If tests cannot run, record the reason, alternative verification, and residual risk.

- Business rule: Work must remain searchable and auditable in the target documentation set while change order stays only in changelog.
- Edge cases: urgent bugfixes, refactors, Python ML work, Rust UI work, reusable module extraction, pure documentation tasks.
- Related tests: `tools/validate_single_source.py`, `tools/validate_skill_pack.py`, `tools/validate_cx_pack.py`

## 5. Technical Architecture

TODO: Describe important modules, interfaces, data flow, error handling, and integration boundaries.

## 6. Test Matrix

| BDD ID | Test command | Expected red | Status |
| --- | --- | --- | --- |
| BDD-CX-001 | `python tools/validate_single_source.py .` | Fails if docs are missing, orphan docs exist, or concrete change IDs appear in the engineering spec | Active |

## 7. Implementation Notes

| Topic | Notes | Status |
| --- | --- | --- |
| Adoption | Replace TODO sections with project content; keep ordered change tasks in `CHANGELOG.md` | planned |

## 8. Reusable Component Registry

| Component | Purpose | Public API | Owners/Callers | Tests | Migration notes |
| --- | --- | --- | --- | --- | --- |
| indexed_series | Long-series wrapper indexed by entity, category, or window | TODO | TODO | TODO | TODO |
| progress_ui | Multi-task progress state and adapters | TODO | TODO | TODO | TODO |
| ragged_tensors | Variable-length tensor utilities | TODO | TODO | TODO | TODO |
| lightning_test_harness | Tiny deterministic Lightning test fixtures | TODO | TODO | TODO | TODO |
| gpui_state_model | Pure Rust UI state and reducers | TODO | TODO | TODO | TODO |

## 9. Verification Evidence

| Date | Source | Command | Result | Notes |
| --- | --- | --- | --- | --- |
| 2026-05-13 | BDD-CX-001 | `python tools/validate_single_source.py examples/python_ml_project` | pass | Example validation |

## 10. Decision Log

| Date | Decision | Reason | Consequences |
| --- | --- | --- | --- |
| 2026-05-13 | Use a target engineering documentation set, separate changelog, and version index | Prevent document sprawl and keep AI tasks searchable | Requires discipline and validation |
