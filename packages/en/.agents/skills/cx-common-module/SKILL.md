---
name: cx-common-module
description: Use when code duplication appears, when creating shared utilities, or when deciding whether progress UI, ragged tensor handling, test harnesses, or GPUI state should become common modules.
version: 1.0.0
---

# cx Common Module Extraction

## Purpose

Turn repeated logic into small, stable, tested common modules. AI-assisted coding often creates similar code in multiple places; this skill stops that drift by requiring a reusable API and tests when duplication becomes meaningful.

## Extract when

Extract a common module when at least one is true:

- The same logic appears in two or more places.
- A behavior is important enough to have its own BDD scenario.
- The logic crosses project areas, such as training and UI.
- The logic is error-prone: tensor padding, masks, progress synchronization, cancellation, metrics, checkpoint paths, or UI state reducers.

Do not extract when the abstraction is speculative and has only one unclear use.

## Required output

- Public API proposal.
- Tests first.
- Backward-compatible migration plan.
- Common Module Registry update in `docs/ENGINEERING_SPEC.md`.
- Test Matrix update.

## Initial module priorities

1. `progress_ui`.
2. `ragged_tensors`.
3. `lightning_test_harness`.
4. `gpui_state_model`.
