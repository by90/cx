---
name: cx-pytorch-tdd
description: Use for Python, PyTorch, Lightning, tensor utilities, model training, data modules, metrics, or ML tests. Enforces unittest-first, tiny tests, and current API verification.
version: 1.0.0
---

# cx Python / PyTorch / Lightning TDD

## Purpose

Use this for Python ML code, PyTorch tensor utilities, LightningModules, DataModules, training loops, metrics, and model tests.

## Required workflow

1. Read the related BDD IDs and Common Module Registry entries in `docs/ENGINEERING_SPEC.md`.
2. When API behavior may be version-sensitive, check current official PyTorch and Lightning documentation.
3. Write Python `unittest` tests first unless the repository has an explicit exception.
4. Keep tests deterministic, tiny, and CPU-first unless GPU behavior is the subject.
5. Prefer pure functions for tensor transformations and isolate Lightning orchestration.
6. Use Black-compatible formatting and avoid changing unrelated user code.

## Tensor test checklist

- Assert shape, dtype, and device when relevant.
- Test empty input, single item, multiple items, and variable-length input.
- Test padding, mask, and length semantics when applicable.
- Test deterministic behavior and important edge cases.
- Test gradients when differentiability is part of the behavior.

## Lightning checklist

- Test LightningModule construction.
- Test pure loss functions or `training_step` with tiny batches.
- Test optimizer configuration if customized.
- Use `fast_dev_run`, limited batches, tiny models, and tiny data for orchestration tests.
- Never introduce long-running training loops into unit tests.
