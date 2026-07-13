# Change: Implement Training Config

## Status

Open

## Related objects

- Use case: `../00.use_case.md`
- Design: `../00.design.md`
- Task: `../tasks/01.implement_training_config.md`

## Current facts

The example project already has use-case, design, and task documents, but the `TrainingConfig` class has not been implemented.

## Target state

The example explicitly follows the test-first workflow: one failing test constrains `TrainingConfig`, then only `src/config/training_config.py` is implemented.

## Major changes

1. Add the narrowest unit test that maps one-to-one to the production file.
2. Implement `TrainingConfig` for the current configuration requirement.

## Ordered work list

| Order | Task | Status |
| --- | --- | --- |
| 01 | `../tasks/01.implement_training_config.md` | Open |

## File scope

- Production code: `src/config/training_config.py`
- Unit test: `tests/config/training_config_test.py`

## Verification

- Run the narrow unit test first and record the expected failure.
- After implementation, rerun the same test and record the passing result.

## Completion action

Delete this change file after unified review passes and let Git retain the change history.
