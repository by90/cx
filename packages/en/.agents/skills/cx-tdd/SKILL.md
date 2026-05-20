---
name: cx-tdd
description: Use for test-driven development after BDD is defined: red-green-refactor, narrow failing tests, test matrices, code quality gates, and verification evidence.
version: 0.1.0
---

# cx TDD Implementation Discipline

## Purpose

Use this skill after `$cx-bdd` has defined the behavior. TDD turns BDD examples into executable tests, forces small design steps, and prevents the assistant from writing unverified production code.

## Required Workflow

1. First confirm the user has explicitly approved entry into testing and implementation after the document update. If not, stop and ask for confirmation.
2. Read the target feature folder's `BDD.md`, `ENGINEERING_SPEC.md`, and `CHANGELOG.md`.
3. Select one BDD ID and one observable behavior.
4. Confirm the prompt provides verification commands or infer the narrowest existing command from the repository. If neither is possible, ask before implementation.
5. Add or update the Test Matrix before implementation.
6. For a generic capability, reusable feature, or reusable class, first write public-call tests, then special-entrypoint tests, then lifecycle/state restoration tests, and only after that consider internal boundaries.
7. Place source files under `src/<subsystem>/` and create one-to-one test files under the matching test path; for example, `src/config/cnn_config.py` maps to `tests/config/cnn_config_test.py`.
8. Write the narrowest failing test first.
9. Run the test and record the expected red failure.
10. Implement the smallest production change that can make the test pass.
11. Run the narrow test until green.
12. Refactor only after green, and keep tests green while refactoring.
13. Run broader validation when the change touches shared behavior.
14. Record commands, results, and residual gaps in the target feature folder.

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
- Before implementing a generic capability, reusable feature, or reusable class, first lock down the public entrypoint, normal call style, special-case entrypoint, lifecycle, state source, and test coverage path; do not write internal loading, validation, conversion, caching, or persistence code until those are covered by tests.
- Refactoring should delete code, reduce branches, and shrink the public surface, not move logic into more small functions.

## Code Quality Rules

- No unstructured pile-up code; also do not manufacture shell functions, classes, or interfaces for one-line forwarding or one-off logic.
- Use object-oriented design only when the behavior has state, lifecycle, invariants, or collaboration between domain objects.
- Prefer explicit attributes, methods, constructors, protocols, traits, or interfaces over dynamic reflection.
- Do not use Python `getattr`, `setattr`, `delattr`, monkey-patching, dynamic method injection, or stringly typed dispatch by default.
- If dynamic reflection appears necessary, first prove there is no clearer static API, record the reason, add focused tests, and isolate it behind a small adapter.
- Avoid global mutable state, hidden singletons, catch-all exception handling, and broad mock-heavy tests.
- Keep public APIs small and documented through tests.
- Tests for a generic capability, reusable feature, or reusable class must first prove the real caller entrypoint works; do not start by testing internal helpers and freezing a wrong design.
- Python code must include file-level explanations, class responsibility notes, function responsibility notes, and line-by-line intent comments. Except for blank lines, pure formatting lines, or repeated structural lines, every line of business code must have an adjacent explanatory comment.
- Subsystem code must not be flattened into the project root or mixed into unrelated directories. For the config subsystem, the source directory is `src/config/`, and CNN configuration must live in its own file, `src/config/cnn_config.py`.
- Unit tests must live under `tests/`, mirror the `src` structure, and map one-to-one with source files by appending `_test.py`; do not use one broad test file for multiple source files, and do not split one source file across multiple arbitrarily named test files.
- Constructors and functions should express default behavior with type annotations and default parameters. Do not stack long parameter-case branches inside `__init__`; move complex default construction into dataclasses, config objects, factories, or small dedicated methods.
- Code must stay minimal, small, and direct. Do not create bloated, long, hard-to-maintain code. Any potentially reusable feature, class, or logic must first invoke `$cx-common-module` to search existing implementation and design the public entrypoint.
- Before final output, review the diff against the prompt contract: goal met, constraints honored, verification run, and residual risks stated.

## Test Matrix Format

```text
BDD-CONFIG-001 -> tests/config/cnn_config_test.py::CnnConfigTest::test_missing_model_name_is_rejected
Expected red: validator currently accepts missing model names
Command: uv run python -m unittest tests.config.cnn_config_test.CnnConfigTest.test_missing_model_name_is_rejected
```

## Output

Every TDD cycle should leave:

- A BDD ID mapped to a test.
- A recorded red failure.
- The minimal implementation.
- A green test result.
- Refactoring notes when refactoring happened.
- Updated verification evidence.
