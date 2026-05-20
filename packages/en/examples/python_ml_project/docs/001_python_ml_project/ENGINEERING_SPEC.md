# ENGINEERING_SPEC.md

This is the long-lived engineering specification for the `001_python_ml_project` feature group. Every project is organized as multiple feature groups, and this file lives at `docs/001_python_ml_project/ENGINEERING_SPEC.md`, linked from `docs/INDEX.md`.

## 0. Document Rules

- This feature group's architecture, task queue, test matrix, reusable feature/class/component decisions, and verification evidence live here.
- When behavior discovery is needed, BDD scenarios live in the sibling `BDD.md`, whose heading and `Feature:` name must match `001_python_ml_project`.
- Do not create `BDD.md` automatically for ordinary non-programming tasks; ask the user first when unsure.
- The sibling `CHANGELOG.md` records this feature group's history only.
- Every `CHANGE-*` entry belongs only in the sibling `CHANGELOG.md`; this file maps to those entries through section, behavior, or task names.
- Every new or changed behavior should have a main success scenario, necessary alternate scenarios, and exception scenarios in `BDD.md`.
- Every BDD scenario should map to tests before implementation; after documents are complete, the agent must wait for user confirmation before writing tests or implementation.

## 1. Product Intent

TODO: Describe the product, users, current goals, and non-goals.

## 2. Change Index

- Initial cx workflow installation: matches the initial entry in the sibling `CHANGELOG.md`.

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
And it stops and waits for the user to confirm the documents and next implementation plan
And after user confirmation, it writes failing tests before production code
And it records verification evidence after the tests pass

Alternate scenarios:

- Every project uses `docs/001_feature_name/ENGINEERING_SPEC.md` and the sibling `CHANGELOG.md`.
- The `docs/` root keeps only index and instruction files such as `INDEX.md`, `README.md`, or `VERSIONS.md`.

Exception scenarios:

- If the target documentation set is missing, create it first and register it in `docs/INDEX.md`.
- If a `CHANGE-*` appears only in changelog and does not map back to the engineering spec, delivery validation must fail.

- Related changelog entry: the initial entry in the sibling `CHANGELOG.md`
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
| Install cx package | Initial changelog entry | done | Replace TODO sections with project-specific content. |

## 8. Reusable Capability Registry

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
| 2026-05-13 | Initial validation | `python tools/validate_single_source.py examples/python_ml_project` | pass | Example validation |

## 10. Decision Log

| Date | Decision | Reason | Consequences |
| --- | --- | --- | --- |
| 2026-05-13 | Use a target engineering documentation set and changelog | Prevent document sprawl and keep AI tasks searchable | Requires discipline and validation |
