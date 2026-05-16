# ENGINEERING_SPEC.md

This is the single long-lived engineering specification for the project. Do not create separate per-feature planning documents unless a human explicitly approves them.

## 0. Document Rules

- Requirements, BDD scenarios, architecture, task queue, test matrix, common module decisions, and verification evidence live here.
- `docs/CHANGELOG.md` records history only.
- Every `CHANGE-*` entry must appear here.
- Every new or changed behavior should have a BDD scenario.
- Every BDD scenario should map to tests before implementation.

## 1. Product Intent

TODO: Describe the product, users, current goals, and non-goals.

## 2. Change Index

- CHANGE-2026-001: Initial cx workflow installation.

## 3. Behavior Map

| Area | Behavior | BDD IDs | Notes |
| --- | --- | --- | --- |
| Workflow | Development starts from one engineering spec and one changelog | BDD-CX-001 | Initial policy |

## 4. BDD Scenarios

### Scenario: BDD-CX-001 - Development uses the single-source BDD/TDD workflow

Given a developer asks for a feature or bugfix
When the assistant plans and implements the work
Then it updates this engineering spec and the changelog before implementation
And it writes failing tests before production code
And it records verification evidence after the tests pass

- Related change: CHANGE-2026-001
- Business rule: Work must remain searchable and auditable in one canonical engineering document.
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

## 8. Common Module Registry

| Module | Purpose | Public API | Tests | Owner |
| --- | --- | --- | --- | --- |
| progress_ui | Multi-task progress state and adapters | TODO | TODO | TODO |
| ragged_tensors | Variable-length tensor utilities | TODO | TODO | TODO |
| lightning_test_harness | Tiny deterministic Lightning test fixtures | TODO | TODO | TODO |
| gpui_state_model | Pure Rust UI state and reducers | TODO | TODO | TODO |

## 9. Verification Evidence

| Date | Change | Command | Result | Notes |
| --- | --- | --- | --- | --- |
| 2026-05-13 | CHANGE-2026-001 | `python tools/validate_single_source.py examples/python_ml_project` | pass | Example validation |

## 10. Decision Log

| Date | Decision | Reason | Consequences |
| --- | --- | --- | --- |
| 2026-05-13 | Use one engineering spec and one changelog | Prevent document sprawl and keep AI tasks searchable | Requires discipline and validation |
