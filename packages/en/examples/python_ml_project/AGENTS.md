# AGENTS.md

This file supplements the global `AGENTS.md` with facts, boundaries, and required tutorials for the Python machine-learning example. Global rules remain in force.

## Project goals

1. Demonstrate how a Python machine-learning project manages training use cases, fixed tasks, and temporary changes with `docs/cx`.
2. Demonstrate how training code reads defaults from a configuration object without command-line arguments or duplicate configuration systems.

## Languages and toolchain

| Item | Current choice | Commands or entries |
| --- | --- | --- |
| Language | Python | `uv run python` |
| Environment and packages | `uv` | `uv sync` |
| Tests | Python `unittest`, only when the task explicitly declares tests | `uv run python -m unittest discover -s tests` |
| Documentation | English Markdown | `docs/cx/` |

## Project structure and boundaries

- Production source is under `src/`; explicitly declared tests mirror it under `tests/`.
- Training, data, and model state use explicit objects.
- Python script behavior comes from configuration objects and does not accept command-line arguments.

## Common-package tutorial navigation

| Domain | Common package or stable capability | Tutorial link | Public entry | Read-first condition |
| --- | --- | --- | --- | --- |
| Training configuration | `config` | [Training configuration tutorial](docs/cx/docs/01.training_configuration_tutorial.md) | `src.config.training_config.TrainingConfig` | Before adding or changing training parameters, training entries, or model defaults |

## Domain reading gate

1. Read the tutorial above before entering the training-configuration domain.
2. Search its documented source entry and real callers.
3. If the entry is missing or the tutorial is stale, use `$cx-doc` to fix documentation and navigation first.
4. Reuse the configuration object whenever it satisfies the need. Do not create a second configuration system.

## Verification and delivery

- Run the narrowest verification explicitly specified by the current task.
- Use `$cx-review` before delivery to verify implementation, tutorials, links, and completion evidence.
