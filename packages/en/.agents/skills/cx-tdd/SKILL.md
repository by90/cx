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
6. Write the narrowest failing test first.
7. Run the test and record the expected red failure.
8. Implement the smallest production change that can make the test pass.
9. Run the narrow test until green.
10. Refactor only after green, and keep tests green while refactoring.
11. Run broader validation when the change touches shared behavior.
12. Record commands, results, and residual gaps in the target feature folder.

## Code Quality Rules

- No unstructured pile-up code. Keep behavior behind named types, small methods, and explicit interfaces.
- Use object-oriented design when the behavior has state, lifecycle, invariants, or collaboration between domain objects.
- Prefer explicit attributes, methods, constructors, protocols, traits, or interfaces over dynamic reflection.
- Do not use Python `getattr`, `setattr`, `delattr`, monkey-patching, dynamic method injection, or stringly typed dispatch by default.
- If dynamic reflection appears necessary, first prove there is no clearer static API, record the reason, add focused tests, and isolate it behind a small adapter.
- Avoid global mutable state, hidden singletons, catch-all exception handling, and broad mock-heavy tests.
- Keep public APIs small and documented through tests.
- Before final output, review the diff against the prompt contract: goal met, constraints honored, verification run, and residual risks stated.

## Test Matrix Format

```text
BDD-CONFIG-001 -> tests/test_config.py::ConfigValidationTest::test_missing_model_name_is_rejected
Expected red: validator currently accepts missing model names
Command: uv run python -m unittest tests.test_config.ConfigValidationTest.test_missing_model_name_is_rejected
```

## Output

Every TDD cycle should leave:

- A BDD ID mapped to a test.
- A recorded red failure.
- The minimal implementation.
- A green test result.
- Refactoring notes when refactoring happened.
- Updated verification evidence.
