---
name: cx-pytorch-tdd
description: Use for Python, PyTorch, Lightning, tensor utilities, model training, data modules, metrics, ML tests, project-level uv environments, Python/PyTorch/CUDA stable-version checks, and test data strategy. Enforces unittest-first, tiny tests, sparse mocks, and current API verification.
version: 0.1.0
---

# cx Python / PyTorch / Lightning TDD

## Purpose

Use this for Python ML code, PyTorch tensor utilities, LightningModules, DataModules, training loops, metrics, and model tests.

## Required workflow

1. First confirm the user has explicitly approved entry into testing and implementation after the document update. If not, stop and ask for confirmation.
2. Read the related BDD IDs and Common Module Registry entries in the target documentation set's `ENGINEERING_SPEC.md`.
3. Use the project-level `uv` virtual environment. Prefer `uv sync`, `uv run`, or the repository's existing `uv` workflow for dependency installation and test execution.
4. Before creating or rebuilding an environment, visit the official Python downloads page and the PyTorch Start Locally page to choose the current official stable Python, PyTorch, and CUDA combination. Do not default to nightly, prerelease, or unofficial wheels.
5. When API behavior may be version-sensitive, check current official PyTorch and Lightning documentation.
6. Write Python `unittest` tests first. Do not introduce `pytest` unless the repository has an explicit exception.
7. Keep tests deterministic, tiny, and CPU-first unless GPU behavior is the subject.
8. Prefer pure functions for tensor transformations and isolate Lightning orchestration.
9. Before adding a dataset, tensor container, indexed series, or test harness, add `$cx-common-module` and search for existing reusable components.
10. Follow the source/test layout and commenting rules from `$cx-tdd`: source files live under `src/<subsystem>/`, tests mirror them under `tests/<subsystem>/`, each source file maps to one `*_test.py`, and code files, classes, functions, and every line of business code have explanatory comments.
11. Use Black-compatible formatting and avoid changing unrelated user code.

## Minimal Implementation Discipline

Iron rule: absolutely no unmaintainable pile-up code.

- Default to the least code that satisfies the current need; do not frameworkize, generalize, or abstract early.
- Do not create functions, classes, constants, or validators for one-line forwarding, one-off logic, or flows without real reuse value.
- Do not add validation that only "looks safer" but is not required, such as filename allowlists, path validity checks, extra AST scans, or duplicate config rule checks.
- In most cases, do not catch or wrap exceptions yourself; when the underlying library already gives clear exceptions, let the original exception propagate.
- Do not create custom exception types unless callers truly need to distinguish that exception and already have a clear handling path.
- Prefer expressing defaults through function or constructor parameters; do not promote simple paths, filenames, or one-off defaults to module-level constants.
- Keep only the public API needed for current behavior; do not add debug entrypoints, memory validation entrypoints, scan entrypoints, or interfaces for future needs.
- Let YAML, JSON, database, filesystem, and similar parsing errors be handled by the corresponding library or standard library by default; add semantic checks only when business rules explicitly require them.
- Every helper function must satisfy all of these: clear name, reduces duplication or isolates real complexity, and either has more than one call site or significantly improves readability. Otherwise inline it.
- Refactoring should delete code, reduce branches, and shrink the public surface, not move logic into more small functions.

## Python Design Rules

- Use object-oriented design for model state, dataset state, configuration, lifecycle, and domain invariants.
- Prefer explicit classes, dataclasses, protocols, typed constructor arguments, and named methods over dynamic attribute access.
- Do not use `getattr`, `setattr`, `delattr`, monkey-patching, or dynamic method injection by default.
- If reflection is unavoidable, first document why explicit methods, mappings, protocols, or dispatch tables do not work; isolate the reflection behind a tiny adapter and test it directly.
- Do not build stringly typed training pipelines. Use typed config objects and explicit factories.
- Keep tensor transformations small and pure where possible, but avoid dumping unrelated logic into utility files.
- Keep Lightning orchestration thin; put domain logic in tested objects or pure functions.
- Avoid broad mocks, global mutable state, catch-all exception handling, and hidden filesystem side effects.

## Environment rules

- Use the project-root `uv` environment, such as the environment defined by `.venv`, `uv.lock`, and `pyproject.toml`.
- If a new environment is required, check https://www.python.org/downloads/ and https://pytorch.org/get-started/locally/ first.
- Choose the PyTorch Stable build and select CPU or CUDA wheels from the official matrix. Treat the CUDA version supported by the PyTorch stable installer as authoritative.
- Run Python unit tests with `uv run python -m unittest ...`.

## Test data rules

- Prefer real but reduced unit-test data.
- For database behavior, prefer a small SQLite database or fixture instead of mocking the data-access layer.
- Use mocks sparingly, only for boundaries such as external services, time, randomness, expensive hardware, or uncontrollable side effects.

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
