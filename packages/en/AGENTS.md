# AGENTS.md

## Repository working agreement

This repository uses the cx single-source BDD/TDD workflow.

1. Read `docs/ENGINEERING_SPEC.md` and `docs/CHANGELOG.md` before planning or editing code.
2. Use `$cx-workflow` for workflow handling, task routing, and uncertainty about which cx skill applies.
3. Use `$cx-bdd-tdd` for feature work, bug fixes, requirements, architecture updates, and implementation planning.
4. Do not create per-feature `spec.md`, `plan.md`, `tasks.md`, or loose design notes unless the user explicitly asks for a separate artifact.
5. Merge new requirements, BDD scenarios, architecture notes, task breakdowns, test mappings, and verification evidence into `docs/ENGINEERING_SPEC.md`.
6. Use `docs/CHANGELOG.md` only as a historical log. Every `CHANGE-*` entry must link back to the engineering spec.
7. Start from BDD behavior, then write failing tests, then implement the smallest change, then refactor.
8. Prefer reusable common modules over duplicated logic. Check the Common Module Registry before adding utilities.
9. After changes, run the narrowest meaningful tests first, then broader validation when practical. Record commands and results.

## Skill routing

- `$cx-workflow`: entry point for workflow handling, task routing, and orchestration across multiple cx skills.
- `$cx-bdd-tdd`: main BDD/TDD flow for feature, bugfix, and planning work.
- `$cx-changelog`: changelog entries, release notes, and `CHANGE-*` consistency.
- `$cx-pytorch-tdd`: Python, PyTorch, Lightning, tensors, training, and ML tests.
- `$cx-ragged-tensor`: padding, masks, lengths, collation, and variable-length tensors.
- `$cx-progress-ui`: multi-task progress state, cancellation, ETA, CLI adapters, or GPUI progress components.
- `$cx-rust-ui`: Rust, GPUI, gpui-component, UI state, and component tests.
- `$cx-common-module`: reusable module extraction and common API design.
- `$cx-evidence`: final review before merge or delivery.

## Python rules

- Use Python functions by default. Use classes only when they make the design clearer or when the user asks.
- Format with Black defaults.
- Tests must use Python's built-in `unittest` unless the repository already requires a different test framework.
- For PyTorch and Lightning, verify current official docs when APIs or versions matter.
- Test tensor shape, dtype, device, determinism, and edge cases.
- Keep training tests tiny: CPU-first, tiny batches, tiny models, `fast_dev_run`, or limited batches.

## Rust / GPUI rules

- Run `cargo fmt` and `cargo test` after Rust changes. Run `cargo clippy --all-targets --all-features` when practical.
- Separate pure state and reducers from GPUI rendering code.
- Prefer stateless gpui-component elements where possible; let views own state.
- Keep UI component APIs small and reusable.

## Documentation policy

Allowed long-lived documentation files in the target repository:

```text
docs/ENGINEERING_SPEC.md
docs/CHANGELOG.md
```

Additional generated docs are temporary unless the user explicitly approves them. If you need a plan, write it into the Task Queue section of `docs/ENGINEERING_SPEC.md`.

## Recommended validation commands

```bash
python -m unittest discover -s tests
cargo fmt --check
cargo test
cargo clippy --all-targets --all-features
```

If the project separately installs the cx validation tools, also run `python tools/validate_single_source.py .`.
