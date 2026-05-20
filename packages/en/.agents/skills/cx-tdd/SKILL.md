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
6. Place source files under `src/<subsystem>/` and create one-to-one test files under the matching test path; for example, `src/config/cnn_config.py` maps to `tests/config/cnn_config_test.py`.
7. Write the narrowest failing test first.
8. Run the test and record the expected red failure.
9. Implement the smallest production change that can make the test pass.
10. Run the narrow test until green.
11. Refactor only after green, and keep tests green while refactoring.
12. Run broader validation when the change touches shared behavior.
13. Record commands, results, and residual gaps in the target feature folder.

## Code Quality Rules

- No unstructured pile-up code. Keep behavior behind named types, small methods, and explicit interfaces.
- Use object-oriented design when the behavior has state, lifecycle, invariants, or collaboration between domain objects.
- Prefer explicit attributes, methods, constructors, protocols, traits, or interfaces over dynamic reflection.
- Do not use Python `getattr`, `setattr`, `delattr`, monkey-patching, dynamic method injection, or stringly typed dispatch by default.
- If dynamic reflection appears necessary, first prove there is no clearer static API, record the reason, add focused tests, and isolate it behind a small adapter.
- Avoid global mutable state, hidden singletons, catch-all exception handling, and broad mock-heavy tests.
- Keep public APIs small and documented through tests.
- Python code must include file-level explanations, class responsibility notes, function responsibility notes, and line-by-line intent comments. Except for blank lines, pure formatting lines, or repeated structural lines, every line of business code must have an adjacent explanatory comment.
- Subsystem code must not be flattened into the project root or mixed into unrelated directories. For the config subsystem, the source directory is `src/config/`, and CNN configuration must live in its own file, `src/config/cnn_config.py`.
- Unit tests must live under `tests/`, mirror the `src` structure, and map one-to-one with source files by appending `_test.py`; do not use one broad test file for multiple source files, and do not split one source file across multiple arbitrarily named test files.
- Constructors and functions should express default behavior with type annotations and default parameters. Do not stack long parameter-case branches inside `__init__`; move complex default construction into dataclasses, config objects, factories, or small dedicated methods.
- Code must stay minimal, small, and direct. Do not create bloated, long, hard-to-maintain code. Any potentially reusable logic must first invoke `$cx-common-module` to search existing implementation and design the common module.
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
