---
name: cx-pytorch-tdd
description: Use together with cx-tdd only when Python, PyTorch, or Lightning TDD, unit tests, tensor tests, or machine-learning tests are explicitly required. Adds only uv, unittest, mirrored source-test layout, shared real test-database data from tests/__init__.py, and tensor and device checks.
version: 0.1.0
---

# cx Python And PyTorch Test Supplement

## Boundary

This skill does not define the test-first workflow. Execute `$cx-tdd` completely, then add these Python, PyTorch, and Lightning rules to the same test cycle.

Without an explicit test requirement, do not use this skill and do not create, edit, or run unit tests.

## Python Tools And Layout

- Use the project-level `uv` environment for Python, formatting, and tests.
- Use Python's built-in `unittest`. Do not introduce `pytest` unless the current user request explicitly requires it.
- Map `src/<subsystem>/xx.py` only to `tests/<subsystem>/xx_test.py`. Do not cover several source files with one large test file or split one source file across several test files.
- Keep blank `__init__.py` files under `src/`. The root `tests/__init__.py` is the shared test-database initialization entry and must not be blank; keep blank `__init__.py` files in other test-package directories.
- Use absolute imports from the repository root and never modify `sys.path`.
- Verify discovery with `uv run python -m unittest discover -v -s ./tests -p "*_test.py" -t .`; run a narrower test method or class during the development loop.
- After editing Python source or tests, use the project `uv` Python to run Black's default formatting check.
- Check the official stable Python, PyTorch, and CUDA combination only when creating or rebuilding an environment. Use official documentation when behavior may vary by version.

## Real Test Data

- Data-related tests must use real records from the test database. Do not fabricate replacement data inside test files.
- `tests/__init__.py` opens the test database once, reads the fixed test range, and constructs shared domain objects. Each `xx_test.py` imports and reuses those objects.
- Do not reopen the database, repeat the same query range, or reconstruct the same domain objects in each test file, class, or method.
- If the test database or required real records are missing, report the missing prerequisite instead of substituting in-memory data, a fake database, or a mocked data-access layer.
- Unless the current user request explicitly requires it, do not write mock tests.

## PyTorch And Lightning Checks

- Keep tests deterministic, tiny, and CPU-first. Use CUDA or another device only when that device behavior is the subject.
- Assert tensor shape, dtype, and device when required by the current behavior. Compare dtype with the config subsystem's type object; only config-default tests may directly assert framework dtype constants.
- Following `$cx-tdd`, compare the first tensor element, the last tensor element, and any one middle element separately against known constants rather than comparing a complete tensor.
- Cover empty, single-item, multi-item, variable-length, padding, mask, length, determinism, or gradient behavior only when the current requirement needs it.
- Use tiny batches, small models, and limited batches for Lightning orchestration tests. Never put a long training loop in a unit test.

## Output

In addition to the `$cx-tdd` record, report the `unittest` command, `uv` environment, shared test-database entry, and tensor shape, dtype, and device results.
