---
name: cx-common-module
description: Use for code duplication, shared utilities, reusable components, component extraction, API design, indexed-series-like data structures, and deciding whether repeated implementation logic should become common modules.
version: 0.1.0
---

# cx Reusable Component And Common Module Extraction

## Purpose

Turn repeated logic, stable data structures, test harnesses, and UI state models into small, stable, tested reusable components. AI-assisted coding often creates similar code in multiple places; this skill stops that drift by requiring search, API design, migration planning, and tests when duplication becomes meaningful.

## Reuse Discovery

Before adding a new abstraction, search:

1. The current project's `src/`, `tests/`, `docs/`, and the target documentation set's Common Module Registry.
2. Enabled related workflow skills such as `$cx-pytorch-tdd`, `$cx-rust-tdd`, `$cx-tdd`, and this skill.
3. Existing projects or prior implementations explicitly mentioned by the user, such as `IndexedSeries` in `rise202604`.
4. Adjacent structures with the same shape, such as indexed series, packed tensor batches, ragged tensors, time-window datasets, or GPUI state reducers.

Record candidates, accept/reject reasons, and migration impact. Do not add a reusable component without search evidence.

## Extract when

Extract a common module when at least one is true:

- The same logic appears in two or more places.
- A behavior is important enough to have its own BDD scenario.
- The logic crosses project areas, such as training and UI.
- The logic is error-prone: indexed series, tensor padding, masks, progress synchronization, cancellation, metrics, checkpoint paths, or UI state reducers.
- A data structure already expresses a stable domain concept, such as grouped long series, window indices, packed batches, state reducers, or test data fixtures.

Do not extract when the abstraction is speculative and has only one unclear use.

## Required output

- Search evidence and candidate comparison.
- Public API proposal with inputs, outputs, error policy, and a minimal example.
- Tests first, preferably covering real small data and edge cases.
- Backward-compatible migration plan describing which call sites move and which stay unchanged.
- Common Module Registry update in the target documentation set's `ENGINEERING_SPEC.md`.
- Test Matrix update in the target documentation set.

## Registry Fields

```text
Component | Purpose | Public API | Owners/Callers | Tests | Migration notes
```

## Initial module priorities

1. `indexed_series` or `indexed_tensor_series`: long-series wrappers indexed by category, entity, or time window.
2. `lightning_test_harness`.
3. Project-specific component libraries that already have a README and tests.
