# AGENTS.md

## Non-Negotiable Rules

These rules override every other rule in this file, all cx skills, templates, examples, and temporary task instructions. Follow a different path only when the user explicitly overrides a specific rule in the current conversation.

1. **Commit and push without ownership splitting**: when the user asks to commit, deliver, open a PR, or release, treat the current working tree as one complete change set, stage and commit tracked and untracked files, and do not analyze who changed which files or split commits by file origin.
2. **Comprehensive comments**: all added or edited code must include file-level explanations, class explanations, function explanations, and line-by-line explanations for business code; only blank lines, pure formatting lines, or repeated structural lines may omit adjacent explanatory comments.
3. **Document confirmation gate**: after BDD, engineering spec, implementation plan, or changelog updates are complete, stop, report the document result and next implementation plan to the user, and wait for explicit user confirmation; do not write tests, edit implementation, or enter TDD before confirmation.
4. **Chinese package means Chinese documents**: when the Chinese cx package is installed, every cx-generated or cx-maintained document must be Simplified Chinese; code identifiers, commands, API names, and quoted external names may remain in their source language.
5. **Tests map one-to-one to source**: unit test directories must mirror `src`, and `src/<subsystem>/xx.py` maps only to `tests/<subsystem>/xx_test.py`; do not use one broad test file for multiple source files, and do not split one source file across multiple arbitrarily named test files.
6. **Default parameters first**: constructors and functions should express defaults with clear type annotations and default parameters; do not build long `__init__` branches for parameter cases, and move complex default construction into dataclasses, config objects, factories, or small dedicated methods.
7. **Minimal code and OOP access**: do not create bloated, long, hard-to-maintain code. Any reusable feature, class, or logic must first go through `$cx-common-module` search and public-entrypoint design. Do not use `getattr`, `setattr`, `delattr`, monkey-patching, dynamic injection, or stringly typed dispatch by default; allow them only when no static OOP API works, and then document the reason, isolate the implementation, and test it.
8. **No automatic BDD for non-programming work**: do not create BDD automatically for ordinary non-programming tasks; if it is unclear whether behavior discovery or acceptance scenarios are needed, ask the user one minimal clarification question first.

## Repository working agreement

This repository uses the cx documentation-set BDD/TDD workflow: every project is organized as multiple feature groups, the `docs/` root is for indexes and instructions, and ordered feature groups own their own documentation sets.

1. Read `docs/INDEX.md` or `docs/README.md`, then read the target feature folder's `ENGINEERING_SPEC.md`, `CHANGELOG.md`, and `BDD.md` when it exists before planning or editing code.
2. Use `$cx-workflow` for workflow handling, task routing, and uncertainty about which cx skill applies.
3. Use `$cx-bdd` for behavior discovery and `$cx-tdd` for test-first implementation.
4. Do not create orphan `spec.md`, `plan.md`, `tasks.md`, or loose design notes. Feature-group documentation sets must live in numbered lowercase underscore folders such as `docs/001_feature_name/`.
5. Merge new requirements, BDD scenarios, architecture notes, task breakdowns, test mappings, and verification evidence into the target documentation set's `ENGINEERING_SPEC.md`.
6. Use the target documentation set's `CHANGELOG.md` only as a historical log. Every `CHANGE-*` entry must link back to the same documentation set's engineering spec.
7. After BDD, engineering spec, implementation plan, or changelog updates are complete, stop, report the document result and next implementation plan to the user, and wait for explicit user confirmation. Do not write tests, edit implementation, or enter TDD before confirmation.
8. After user confirmation, start from BDD behavior, then write failing tests, then implement the smallest change, then refactor.
9. Prefer reusable features, classes, components, and public capability entrypoints over duplicated logic. Before adding a utility, data structure, test harness, or UI state model, search existing implementation, related skills, and the Reusable Capability Registry.
10. Every feature group must use its own branch. Merge completed feature-group branches into `dev`; do not merge them directly into `main`.
11. Only after the user confirms the version is complete may `dev` be merged into `main`; only `main` may be used for version commits, release tags, and release-tag pushes. Feature branches and `dev` may still be pushed for collaboration, backup, or CI.
12. After changes, run the narrowest meaningful tests first, then broader validation when practical. Record commands and results.
13. When adding or editing code, add beginner-friendly explanatory comments for code files, classes, functions, and every line of business code. Code files must have a file-level explanation, classes and functions must describe their responsibilities, and code intent must be explained line by line by default except for pure formatting, blank lines, or repeated structural lines.

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
- `$cx-common-module`: generic capabilities, reusable features, reusable classes, reusable-capability extraction, and common API design.
- `$cx-evidence`: final review before merge or delivery.

## Python rules

- Subsystem source code must live under `src/<subsystem>/`; for example, the config subsystem lives under `src/config/`, and CNN configuration belongs in its own file, `src/config/cnn_config.py`.
- Use the project-level `uv` virtual environment. Install dependencies and run Python commands with `uv sync`, `uv run`, or the repository's existing `uv` workflow.
- Before creating or rebuilding a Python / PyTorch environment, visit the official Python and PyTorch websites and choose the current official stable Python, PyTorch, and CUDA combination. Do not default to nightly, prerelease, or unofficial wheels.
- Use functions for stateless logic by default; use object-oriented design for state, lifecycle, invariants, and domain collaborations.
- Use object-oriented design for state, lifecycle, invariants, and domain collaborations.
- Prefer typed default parameters for constructors and functions. Do not fill `__init__` with long `if`/`None`/type-branch handling for many parameter cases.
- Do not use `getattr`, `setattr`, `delattr`, monkey-patching, dynamic method injection, or stringly typed dispatch unless no explicit static OOP API works; document the reason and isolate it behind tests.
- Keep code short, direct, and readable. When a feature, class, or logic may be reusable, use `$cx-common-module` to search existing implementation and the Reusable Capability Registry before adding or reusing a public entrypoint.
- Format with Black defaults.
- Tests must use Python's built-in `unittest`; do not introduce `pytest` unless the repository already explicitly uses it.
- Unit test directories must mirror the `src` structure and map one-to-one with source files: the test for `src/config/cnn_config.py` must be `tests/config/cnn_config_test.py`. Do not mix multiple source files into one broad test file, and do not split one source file across multiple arbitrarily named test files.
- For PyTorch and Lightning, verify current official docs when APIs or versions matter.
- Test tensor shape, dtype, device, determinism, and edge cases.
- Keep training tests tiny: CPU-first, tiny batches, tiny models, `fast_dev_run`, or limited batches.
- Prefer real, small unit-test data. For database behavior, use a reduced SQLite database or fixture when practical, and use mocks sparingly only for boundaries such as external services, time, or randomness that cannot be controlled realistically.

## Windows Toolchain Rules

- On Windows, when a task explicitly requires the `ng` command and it is not installed locally, install the project-required `ng` CLI before continuing. Do not replace `ng` with PowerShell scripts, the `ps` alias, or ad hoc substitute commands.
- Prefer the package manager locked by the project: use `npm` when `package-lock.json` exists, `pnpm` when `pnpm-lock.yaml` exists, and `yarn` when `yarn.lock` exists. If the project gives no constraint, state the assumption and install Angular CLI.
- After installation, run `ng version` or the project's equivalent version command to confirm the CLI works before running generation, build, or test commands.

## Rust / GPUI rules

- Use Rust's built-in unit test mechanism and `cargo test`; do not introduce an extra test framework unless the repository already explicitly uses it.
- Run `cargo fmt` and `cargo test` after Rust changes. Run `cargo clippy --all-targets --all-features` when practical.
- Model domain state with structs/enums/traits and explicit `Result` errors.
- Avoid `unwrap`, `expect`, and `panic!` in production paths unless the invariant is local, proven, and documented.
- Separate pure state and reducers from rendering code.
- Before adding reusable UI state, component APIs, or reducers, search the Reusable Capability Registry and existing implementations.
- Prefer stateless gpui-component elements where possible; let views own state.
- Keep UI component APIs small and reusable.

## Documentation policy

Every project uses multiple ordered feature directories, with the `docs/` root reserved for indexes, instructions, and the version index:

```text
docs/INDEX.md
docs/VERSIONS.md
docs/001_configuration_system/BDD.md
docs/001_configuration_system/ENGINEERING_SPEC.md
docs/001_configuration_system/CHANGELOG.md
docs/001_configuration_system/GUIDE.md
```

Additional generated docs are temporary unless the user explicitly approves them. If you need a plan, write it into the target documentation set's `ENGINEERING_SPEC.md` Task Queue section.

When the Chinese cx package is installed, every cx-generated or cx-maintained document must be Simplified Chinese. Long-lived documentation must live under the project's `docs/` directory. Code identifiers, commands, API names, and quoted external names may remain in their source language.

BDD scenarios, test matrices, implementation plans, and verification evidence must be written in the target documentation set under the project's `docs/` directory; do not create BDD automatically for ordinary non-programming tasks, and ask first when unsure.

## Git Commit Rules

- When the user asks to commit, deliver, open a PR, or release, treat the current working tree as one change set. Do not analyze which files were changed by the assistant, which were changed by the user, or which files are untracked.
- Run `git status --short` before committing only to confirm the working tree contents and spot obvious risk, not to split files by ownership.
- By default, stage all tracked and untracked files and create one commit. Do not split one task into multiple commits unless the user explicitly asks.
- Stop and ask the user first only when obvious secrets, credentials, local environment files, build artifacts, dependency directories, or unrelated large files are present.
- The commit message should describe the overall user-requested result, not file ownership.
- After work is complete, merge the feature branch into `dev`, then delete the local feature branch.
- Push the feature branch to the remote only when the user explicitly asks; do not push feature branches by default.
- Push only `dev` by default. Merge and push `main` only when the user explicitly asks for a release handoff or a merge to `main`.

## Recommended validation commands

```bash
python -m unittest discover -s tests
cargo fmt --check
cargo test
cargo clippy --all-targets --all-features
```

If the project separately installs the cx validation tools, also run `python tools/validate_single_source.py .`.
