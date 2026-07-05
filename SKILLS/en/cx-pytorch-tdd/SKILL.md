---
name: cx-pytorch-tdd
description: Use only when the current user request, existing task document, or change document explicitly asks for Python/PyTorch/Lightning unit tests, TDD, tensor tests, or ML tests. Covers uv environments, Python/PyTorch/CUDA stable-version checks, tiny tests, sparse mocks, and current API verification.
version: 0.1.0
---

# cx Python / PyTorch / Lightning Explicit Tests

## Language Rules

- Use the package language for conversations, explanations, plans, summaries, review decisions, verification evidence, and cx documents. Do not mix languages inside prose fragments or term lists.
- In Chinese-package work, if an English identifier, command, path, API name, library, protocol, standard, proper name, or ambiguity-sensitive term must remain in English, explain its meaning, role, and local context in Chinese in the same sentence or an adjacent sentence. In English-package work, explain unavoidable non-English terms in English.

## Purpose

Use this for Python ML code, PyTorch tensor utilities, LightningModules, DataModules, training loops, metrics, and model tests only when testing is explicitly requested. Default implementation does not create or edit unit tests.

## Required workflow

1. Confirm that the current request, task document, or change document explicitly asks for unit tests, TDD, tensor tests, or ML tests; otherwise return to `$cx-workflow` default one-code-file implementation.
2. Read the target `docs/cx` use-case document, design document, current task document, current change document, and reusable capability notes.
3. Use the project-level `uv` virtual environment. Prefer Python interpreters installed and managed by `uv`, and use `uv sync`, `uv run`, `uv run --python <version>`, or the repository's existing `uv` workflow for dependency installation and test execution.
4. Before creating or rebuilding an environment, visit the official Python downloads page and the PyTorch Start Locally page to choose the current official stable Python, PyTorch, and CUDA combination. Do not default to nightly, prerelease, or unofficial wheels.
5. When API behavior may be version-sensitive, check current official PyTorch and Lightning documentation.
6. Training, data-preparation, diagnostic, and migration scripts must not accept command-line arguments. When batch, device, path, seed, epoch, model variant, or diagnostic switches must be adjustable, define config-subsystem items with defaults, and let default runs use those defaults.
7. Numeric types, level types, category types, id types, row-id types, and index types must come from type objects in the config subsystem. PyTorch training code should store `torch.dtype` type objects in model config; except for tests that assert config defaults, tests and implementation must not directly hard-code `torch.float32`, `torch.float64`, `torch.float16`, `torch.bfloat16`, `torch.int64`, `torch.int32`, `np.float32`, `np.float64`, `np.int64`, `np.int32`, or equivalent types in data preparation, tensor construction, batching, training, inference, loss computation, or test fixtures.
8. When unit tests are explicitly requested, use Python `unittest`. Do not introduce `pytest` unless the repository has an explicit exception.
9. Keep tests deterministic, tiny, and CPU-first unless GPU behavior is the subject.
10. Prefer pure functions for tensor transformations and isolate Lightning orchestration.
11. Before adding a dataset, tensor container, indexed series, or test harness, add `$cx-common-module` and search for existing reusable features, classes, or components.
12. Follow the one-code-file boundary plus source/test layout and commenting rules from `$cx-tdd`: source files live under `src/<subsystem>/`; when tests are explicitly requested, tests mirror them under `tests/<subsystem>/`, and each source file maps to one `*_test.py`. Source files and explicitly requested unit tests must include file-level purpose notes, class notes, function parameter/return explanations, and line-by-line intent comments.
13. After editing Python source or tests, run Black default-format checks, for example `python -m black --check src tests tools`, and avoid changing unrelated user code.
14. After code and required verification are done, run `$cx-review` code-deliverable review. Focus on docs agreement, repeated tensor/data/config logic, full object-oriented design, minimal implementation, no extra validation, no extra variable passing, and no redundant parameter or variable names.
15. If review fails, do not mark the task complete; fix implementation or docs, then rerun verification and review.

## Minimal Implementation Discipline

Iron rule: absolutely no unmaintainable pile-up code.

- Default to the least code that satisfies the current need; do not frameworkize, generalize, or abstract early.
- Keep file, class, method, and variable names short and clear; avoid sentence-like identifiers, and extract responsibilities or reuse domain terms when names grow too long.
- Do not create functions, classes, constants, or validators for one-line forwarding, one-off logic, or flows without real reuse value.
- Unless business rules explicitly require it, do not hide exceptions, silently fall back, or turn errors that would harm the product into defaults, empty results, skipped records, fake successful retries, or warnings; during development, let these errors stop execution.
- Use a simple test: if the same bug shipped to the product would cause a problem, it must surface as a failure. Only add explicit handling when the business requires degradation, recovery, or user-visible guidance, and cover that path with tests.
- Do not add validation that only "looks safer" but is not required, such as filename allowlists, path validity checks, extra AST scans, or duplicate config rule checks.
- Do not put per-item data-validity checks inside large loops, training loops, hot paths, or batch processing to fall back or slow the system down. Handle data validity at entrypoints, data preparation, test fixtures, or separate diagnostic tasks, and never use those checks to replace real failures.
- By default, do not catch or wrap exceptions yourself; when the underlying library already gives clear exceptions, let the original exception propagate.
- Do not create custom exception types unless callers truly need to distinguish that exception and already have a clear handling path.
- Prefer expressing defaults through function or constructor parameters; do not promote simple paths, filenames, or one-off defaults to module-level constants.
- Keep only the functional entrypoint needed for current behavior; do not add debug entrypoints, memory validation entrypoints, scan entrypoints, or interfaces for future needs.
- During project development, never keep compatibility interfaces, old entrypoints, aliases, adapter layers, bridge functions, or new/old coexistence branches for old code. Do not optimize for old/new code compatibility; remove all unused code, old paths, obsolete tests, and stale documents after the change.
- Let YAML, JSON, database, filesystem, and similar parsing errors be handled by the corresponding library or standard library by default; add semantic checks only when business rules explicitly require them.
- Every helper function must satisfy all of these: clear name, reduces duplication or isolates real complexity, and either has more than one call site or significantly improves readability. Otherwise inline it.
- Refactoring should delete code, reduce branches, and shrink the public surface, not move logic into more small functions.

## Python Design Rules

- Use full object-oriented design for model state, dataset state, configuration, lifecycle, and domain invariants.
- Prefer explicit classes, dataclasses, protocols, typed constructor arguments, and named methods over dynamic attribute access.
- Do not use `getattr`, `setattr`, `delattr`, monkey-patching, or dynamic method injection by default.
- If reflection is unavoidable, first document why explicit methods, mappings, protocols, or dispatch tables do not work; isolate the reflection behind a tiny adapter and test it directly.
- Do not build stringly typed training pipelines. Use typed config objects and explicit factories.
- Do not add `argparse`, `click`, `typer`, `sys.argv`, or custom command-line parsing to scripts. Any adjustable behavior belongs in config-subsystem items, and each item must have a default value.
- Keep tensor transformations small and pure where possible, but avoid dumping unrelated logic into utility files.
- Keep Lightning orchestration thin; put domain logic in tested objects or pure functions.
- Avoid broad mocks, global mutable state, catch-all exception handling, and hidden filesystem side effects.

## Environment rules

- Use the project-root `uv` environment, such as the environment defined by `.venv`, `uv.lock`, and `pyproject.toml`.
- Python interpreters must preferably come from `uv` management; system `python` / `python3` may be used to inspect the environment, but should not replace the project `uv` Python for tests, builds, or tooling commands.
- If a new environment is required, check https://www.python.org/downloads/ and https://pytorch.org/get-started/locally/ first.
- Choose the PyTorch Stable build and select CPU or CUDA wheels from the official matrix. Treat the CUDA version supported by the PyTorch stable installer as authoritative.
- When unit tests are explicitly requested, run them with `uv run python -m unittest ...`.

## Test data rules

- Prefer real but reduced unit-test data.
- For database behavior, prefer a small SQLite database or fixture instead of mocking the data-access layer.
- Use mocks sparingly, only for boundaries such as external services, time, randomness, expensive hardware, or uncontrollable side effects.
- Unit-test assertions must state that one actual value equals one known constant fact. Expected values must come from manual confirmation, real small samples, fixed fixtures, or frozen database facts. Do not recompute another calculation, query, transformation, aggregation, ordering, formula, or equivalent business algorithm on the expected side and compare both results.
- For lists, arrays, tensors, query results, dataset samples, and other ordered collections, check the first item, the last item, and one middle item against known constant facts by default, plus length, shape, dtype, and device when relevant. Do not compare a full collection against another fully computed collection just to look complete.
- Only when the current request or task document explicitly requires full collection verification may a test check every item. Limit-up and limit-down price calculation tests are an explicit exception and may cover a full market-data sample; even then, expected limit prices, abnormal codes, and expected states must be known constant facts or manually confirmed facts, not values recomputed with the same limit-price algorithm in the test.

## Tensor test checklist

- Assert shape, dtype, and device when relevant.
- dtype assertions must compare against type objects from the config subsystem; only tests for config defaults may assert concrete framework type constants directly.
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
