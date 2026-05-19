# AGENTS.md

## Repository working agreement

This repository uses the cx documentation-set BDD/TDD workflow: the `docs/` root is for indexes and instructions, while ordered feature groups own their own documentation sets.

1. Read `docs/INDEX.md` or `docs/README.md`, then read the target feature folder's `BDD.md`, `ENGINEERING_SPEC.md`, and `CHANGELOG.md` before planning or editing code.
2. Use `$cx-workflow` for workflow handling, task routing, and uncertainty about which cx skill applies.
3. Use `$cx-bdd` for behavior discovery and `$cx-tdd` for test-first implementation.
4. Do not create orphan `spec.md`, `plan.md`, `tasks.md`, or loose design notes. Use `docs/<feature-group>/` documentation sets for multiple feature groups.
5. Merge new requirements, BDD scenarios, architecture notes, task breakdowns, test mappings, and verification evidence into the target documentation set's `ENGINEERING_SPEC.md`.
6. Use the target documentation set's `CHANGELOG.md` only as a historical log. Every `CHANGE-*` entry must link back to the same documentation set's engineering spec.
7. Start from BDD behavior, then write failing tests, then implement the smallest change, then refactor.
8. Prefer reusable components and common modules over duplicated logic. Before adding a utility, data structure, test harness, or UI state model, search existing implementation, related skills, and the Common Module Registry.
9. Every feature group must use its own branch. Merge completed feature-group branches into `dev`; do not merge them directly into `main`.
10. Only after the user confirms the version is complete may `dev` be merged into `main`; only `main` may be used for version commits, release tags, and release-tag pushes. Feature branches and `dev` may still be pushed for collaboration, backup, or CI.
11. After changes, run the narrowest meaningful tests first, then broader validation when practical. Record commands and results.
12. When adding or editing code, add beginner-friendly explanatory comments for code files, classes, functions, and important statements. Explain code intent line by line by default, except for pure formatting or repeated structural lines.

## Prompt contract

Coding-agent prompts should specify:

- Goal: the behavior or outcome to change.
- Context: target feature folder, relevant files, branch, or environment.
- Constraints: APIs, language rules, performance, compatibility, or style limits.
- Required workflow: cx skills to use and whether BDD, TDD, research, versioning, or evidence review is required.
- Verification: exact commands, tests, screenshots, or checks expected.
- Deliverables: code, docs, changelog entries, evidence, or final summary.
- Branching: feature-group branch name, merge target `dev`, and whether a release handoff to `main` is requested.

If the repository also uses Claude Code, keep this `AGENTS.md` as the shared rule source and have `CLAUDE.md` import or reference it instead of duplicating the rules.

## Skill routing

- `$cx-workflow`: entry point for workflow handling, task routing, and orchestration across multiple cx skills.
- `$cx-bdd`: BDD discovery, ordered feature folders, business rules, and scenarios.
- `$cx-tdd`: test-first implementation, red-green-refactor, and test matrix evidence.
- `$cx-changelog`: changelog entries, release notes, and `CHANGE-*` consistency.
- `$cx-version`: release versioning with SemVer, VERSION, changelog, and annotated tags.
- `$cx-research`: model selection, AI paper research, source screening, and cited synthesis.
- `$cx-pytorch-tdd`: Python, PyTorch, Lightning, tensors, training, and ML tests.
- `$cx-rust-tdd`: Rust implementation, ownership-aware design, and cargo test/fmt/clippy.
- `$cx-common-module`: reusable component extraction, common module extraction, and common API design.
- `$cx-evidence`: final review before merge or delivery.

## Python rules

- Use the project-level `uv` virtual environment. Install dependencies and run Python commands with `uv sync`, `uv run`, or the repository's existing `uv` workflow.
- Before creating or rebuilding a Python / PyTorch environment, visit the official Python and PyTorch websites and choose the current official stable Python, PyTorch, and CUDA combination. Do not default to nightly, prerelease, or unofficial wheels.
- Use Python functions by default. Use classes only when they make the design clearer or when the user asks.
- Use object-oriented design for state, lifecycle, invariants, and domain collaborations.
- Do not use `getattr`, `setattr`, `delattr`, monkey-patching, or dynamic method injection unless no explicit static API works; document the reason and isolate it behind tests.
- Format with Black defaults.
- Tests must use Python's built-in `unittest`; do not introduce `pytest` unless the repository already explicitly uses it.
- For PyTorch and Lightning, verify current official docs when APIs or versions matter.
- Test tensor shape, dtype, device, determinism, and edge cases.
- Keep training tests tiny: CPU-first, tiny batches, tiny models, `fast_dev_run`, or limited batches.
- Prefer real, small unit-test data. For database behavior, use a reduced SQLite database or fixture when practical, and use mocks sparingly only for boundaries such as external services, time, or randomness that cannot be controlled realistically.

## Rust / GPUI rules

- Use Rust's built-in unit test mechanism and `cargo test`; do not introduce an extra test framework unless the repository already explicitly uses it.
- Run `cargo fmt` and `cargo test` after Rust changes. Run `cargo clippy --all-targets --all-features` when practical.
- Model domain state with structs/enums/traits and explicit `Result` errors.
- Avoid `unwrap`, `expect`, and `panic!` in production paths unless the invariant is local, proven, and documented.
- Separate pure state and reducers from rendering code.
- Before adding reusable UI state, component APIs, or reducers, search the Common Module Registry and existing implementations.
- Prefer stateless gpui-component elements where possible; let views own state.
- Keep UI component APIs small and reusable.

## Documentation policy

Single-feature projects may use one root documentation set:

```text
docs/ENGINEERING_SPEC.md
docs/CHANGELOG.md
```

Multi-feature projects use ordered feature directories, with the `docs/` root reserved for indexes and instructions:

```text
docs/INDEX.md
docs/1.Configuration System/BDD.md
docs/1.Configuration System/ENGINEERING_SPEC.md
docs/1.Configuration System/CHANGELOG.md
```

Additional generated docs are temporary unless the user explicitly approves them. If you need a plan, write it into the target documentation set's `ENGINEERING_SPEC.md` Task Queue section.

When producing Chinese-language documentation, use Simplified Chinese. Long-lived documentation must live under the project's `docs/` directory.

BDD scenarios, test matrices, implementation plans, and verification evidence must be written in the target documentation set under the project's `docs/` directory.

## Recommended validation commands

```bash
python -m unittest discover -s tests
cargo fmt --check
cargo test
cargo clippy --all-targets --all-features
```

If the project separately installs the cx validation tools, also run `python tools/validate_single_source.py .`.
