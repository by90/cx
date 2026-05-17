# AGENTS.md

## Repository working agreement

This repository uses the cx documentation-set BDD/TDD workflow: the `docs/` root is for indexes and instructions, while feature groups may own their own documentation sets.

1. Read `docs/INDEX.md` or `docs/README.md`, then read the target documentation set's `ENGINEERING_SPEC.md` and `CHANGELOG.md` before planning or editing code.
2. Use `$cx-workflow` for workflow handling, task routing, and uncertainty about which cx skill applies.
3. Use `$cx-bdd-tdd` for programming-related feature work, bug fixes, requirements, architecture updates, and implementation planning; non-programming tasks do not use TDD.
4. Do not create orphan `spec.md`, `plan.md`, `tasks.md`, or loose design notes. Use `docs/<feature-group>/` documentation sets for multiple feature groups.
5. Merge new requirements, BDD scenarios, architecture notes, test mappings, reusable component decisions, and verification evidence into the target documentation set's `ENGINEERING_SPEC.md`.
6. Use the target documentation set's `CHANGELOG.md` as the only ordered record of changes and change tasks; concrete `CHANGE-*` IDs must not appear in `ENGINEERING_SPEC.md`.
7. For programming tasks, start from BDD behavior, then write failing tests, then implement the smallest change, then refactor; for non-programming tasks, verify with checklists, review evidence, or delivery confirmation.
8. In principle, each feature group or change uses its own git branch, then merges into `dev` and deletes the work branch after completion.
9. When a feature group is complete and ready for a version, use the version tool to update `docs/VERSIONS.md`, for example `v0.0.1 "Create project template"`.
10. Prefer reusable components and common modules over duplicated logic. Before adding a utility, data structure, test harness, or UI state model, search existing implementation, related skills, prior projects, and the Common Module Registry.
11. After changes, run the narrowest meaningful tests or checks first, then broader validation when practical. Record commands and results.
12. When adding or editing code, add beginner-friendly explanatory comments for code files, classes, functions, and important statements. Explain code intent line by line by default, except for pure formatting or repeated structural lines.

## Skill routing

- `$cx-workflow`: entry point for workflow handling, task routing, and orchestration across multiple cx skills.
- `$cx-bdd-tdd`: main BDD/TDD flow for programming feature, bugfix, and planning work.
- `$cx-changelog`: changelog entries, ordered change tasks, release notes, and `CHANGE-*` single source.
- `$cx-pytorch-tdd`: Python, PyTorch, Lightning, tensors, training, and ML tests.
- `$cx-ragged-tensor`: padding, masks, lengths, collation, and variable-length tensors.
- `$cx-progress-ui`: multi-task progress state, cancellation, ETA, CLI adapters, or GPUI progress components.
- `$cx-rust-ui`: Rust, GPUI, gpui-component, UI state, and component tests.
- `$cx-common-module`: reusable component extraction, common module extraction, and common API design.
- `$cx-evidence`: final review before merge or delivery.

## Python rules

- Use the project-level `uv` virtual environment. Install dependencies and run Python commands with `uv sync`, `uv run`, or the repository's existing `uv` workflow.
- Before creating or rebuilding a Python / PyTorch environment, visit the official Python and PyTorch websites and choose the current official stable Python, PyTorch, and CUDA combination. Do not default to nightly, prerelease, or unofficial wheels.
- Use Python functions by default. Use classes only when they make the design clearer or when the user asks.
- Format with Black defaults.
- Tests must use Python's built-in `unittest`; do not introduce `pytest` unless the repository already explicitly uses it.
- For PyTorch and Lightning, verify current official docs when APIs or versions matter.
- Test tensor shape, dtype, device, determinism, and edge cases.
- Keep training tests tiny: CPU-first, tiny batches, tiny models, `fast_dev_run`, or limited batches.
- Prefer real, small unit-test data. For database behavior, use a reduced SQLite database or fixture when practical, and use mocks sparingly only for boundaries such as external services, time, or randomness that cannot be controlled realistically.

## Rust / GPUI rules

- Use Rust's built-in unit test mechanism and `cargo test`; do not introduce an extra test framework unless the repository already explicitly uses it.
- Run `cargo fmt` and `cargo test` after Rust changes. Run `cargo clippy --all-targets --all-features` when practical.
- Separate pure state and reducers from GPUI rendering code.
- Before adding reusable UI state, component APIs, or reducers, search the Common Module Registry and existing implementations.
- Prefer stateless gpui-component elements where possible; let views own state.
- Keep UI component APIs small and reusable.

## Documentation policy

Single-feature projects may use one root documentation set:

```text
docs/ENGINEERING_SPEC.md
docs/CHANGELOG.md
docs/GUIDE.md
```

Multi-feature projects use multiple feature directories, with the `docs/` root reserved for indexes and instructions:

```text
docs/INDEX.md
docs/VERSIONS.md
docs/<feature-group>/ENGINEERING_SPEC.md
docs/<feature-group>/CHANGELOG.md
docs/<feature-group>/GUIDE.md
```

Additional generated docs are temporary unless the user explicitly approves them. If change tasks need ordering, write them into the target documentation set's `CHANGELOG.md`; do not duplicate change records in the BDD spec.

When producing Chinese-language documentation, use Simplified Chinese. Long-lived documentation must live under the project's `docs/` directory.

BDD scenarios, test matrices, implementation notes, and verification evidence must be written in the target documentation set under the project's `docs/` directory. Non-programming tasks do not use TDD.

## Recommended validation commands

```bash
python -m unittest discover -s tests
cargo fmt --check
cargo test
cargo clippy --all-targets --all-features
```

If the project separately installs the cx validation tools, also run `python tools/validate_single_source.py .`.
