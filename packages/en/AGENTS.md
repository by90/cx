# AGENTS.md

## Decision Prompts

When facing architecture tradeoffs, API design, dependency choices, implementation paths, performance or compatibility tradeoffs, release strategy, repeated defects, or project risk, prefer one of these decision frames: first principles, inversion, five whys, second-order thinking, regret minimization, opportunity cost, or premortem analysis.

## Iron Rules

These rules override other rules, cx skills, templates, examples, and temporary task instructions unless the user explicitly overrides one in the current conversation.

1. **Commits and pushes do not split by source**: when the user asks for a commit, delivery, PR, or release, treat the current working tree as one complete change set and stage tracked plus untracked files.
2. **Comprehensive comments**: all new or edited source and unit-test files need file-level purpose notes, class/type notes, function notes, and line-by-line business-code intent comments.
3. **Default one-task one-code-file execution**: before programming or workflow development work, default to completing the current task document and then editing only the one production code file bound to that task. If a second code file is needed, split the next task first. Continue into another code file only when the user explicitly requests multi-task continuation; wait after each task only when the user explicitly requests per-task confirmation.
4. **Language package document language**: English package documents should be English; Chinese package documents must be Simplified Chinese.
5. **Explicit unit tests**: by default, do not create, edit, or run unit tests. Create or edit one matching test file only when the current user request, existing task document, or change document explicitly asks for unit tests, TDD, failing tests, or red-green-refactor. When unit tests are explicitly requested, tests mirror `src`; `src/<subsystem>/xx.py` maps only to `tests/<subsystem>/xx_test.py`.
6. **Default parameters first**: prefer clear type annotations and default parameters over large constructor branching.
7. **Full OOP, minimal code, and reuse first**: use full OOP for state, lifecycle, invariants, and domain collaboration. Avoid bloated code, overly long files, overly long variable names, and sentence-like identifiers. Search and design common entrypoints with `$cx-common-module` before adding reusable logic. Do not default to dynamic reflection, monkey patching, dynamic injection, or string dispatch.
8. **Python scripts do not accept command-line parameters**: target-project scripts take adjustable behavior from config-subsystem items with defaults.
9. **No legacy compatibility during development**: do not keep old entrypoints, aliases, adapters, bridges, or old/new coexistence branches.
10. **Development errors must surface**: do not swallow, hide, default, skip, or fake success for product-harming errors.
11. **No fallback prechecks in performance paths**: data validity belongs at entrypoints, data preparation, fixtures, or diagnostics, not hot-path filtering.
12. **No automatic cx use-case flow for ordinary non-programming work**: ask a minimal clarification question when unsure.
13. **Visible todos**: create and update a visible todo list for multi-step work.
14. **Use uv Python**: run Python scripts, tests, builds, and tools with `uv` managed Python.
15. **Avoid mixed-language prose**: use the package language for prose unless code identifiers, commands, paths, API names, libraries, protocols, standards, or proper names require source text.
16. **Cross-platform encoding**: PowerShell scripts use UTF-8 with BOM; other source, Markdown, JSON, TOML, YAML, and text files use UTF-8 without BOM. When viewing, searching, or printing UTF-8-without-BOM files that contain Chinese in Windows or PowerShell, silently force UTF-8 read and output encoding by default, for example by setting `[Console]::InputEncoding`, `[Console]::OutputEncoding`, and `$OutputEncoding`, and by passing `-Encoding UTF8` to text commands. Do not treat mojibake console output as evidence that the file encoding is damaged, and do not patch against mojibake output. When exact location is needed, use project-level `uv` Python or its `.venv` interpreter to print line numbers and string representations in read-only mode. Apply edits with small `apply_patch` hunks anchored on functions, classes, headings, keys, and code structure. Unless the actual file encoding is abnormal, a patch fails, or the user asks for the reason, do not repeatedly describe encoding handling in routine progress updates or summaries.
17. **Chinese first, English second**: when modifying cx workflow, skills, templates, examples, or install rules, finish the Chinese package first and then synchronize English.
18. **Explicit tests and full OOP**: Python, PyTorch, and Rust projects do not use unit tests or TDD by default. Run test-first flow only when explicitly requested. State, lifecycle, invariants, and domain collaboration use full OOP or equivalent type modeling.
19. **Mandatory review after code**: after production code is written, run local code review before considering the task complete. Review must check exact agreement with `00.use_case.md`, `00.design.md`, the task document, and the change document; duplication smells; full OOP; minimal code with no extra validation, extra variable passing, or redundant variable/parameter names; and business-semantic fit. If review fails, the task remains incomplete until fixed and reviewed again.

## Repository Workflow

This repository uses a `docs/cx` use-case-driven flow. All cx project descriptions, scenarios, tasks, process documents, and changes live under `docs/cx`; documents elsewhere are unrelated to cx.

1. Before planning or code changes, read `docs/cx/00.project.md` or relevant project-level docs, then the target scenario's use-case document, design document, `tasks/`, and `changes/`.
2. Unless adding a task, conditional substep, or use case, inspect unfinished changes first and use them to decide current work.
3. Each main success scenario has one folder, such as `docs/cx/01.create_user/`.
4. Each scenario folder contains `00.use_case.md`, `00.design.md`, `tasks/`, and `changes/`.
5. The use-case document expresses the main success scenario and conditional, alternate, or exception substeps attached to concrete main steps.
6. One `docs/cx/NN.name/` folder carries one user-goal use case. Do not use a vague "use the app" use case to hold a whole application, page set, menu, or several independent operations.
7. The main success scenario describes the most common path from trigger to completed user goal, usually 3 to 9 main steps. Each step is one observable actor-system interaction.
8. If a main-success step needs its own actors, preconditions, main success scenario, and conditional substeps, it is a sub-use case or separate use case and should move to a new `docs/cx/NN.name/` folder; the original step should use a substep such as "enter use case: X".
9. Conditional, alternate, and exception behavior must attach to a concrete main-success step with substep numbering such as `1.1` or `2.1`. Split complex conditional flows into separate use cases when they exceed 3 to 5 steps, introduce a new actor, have independent completion criteria, or need independent tasks and tests.
10. The design document explains reusable code, new common code, and design decisions.
11. Each task is a folder starting at `01.`, such as `tasks/01.write_user_entity/00.task.md`.
12. Each change is one file, such as `changes/20260629T120000-task01-write_user_entity.md`.
13. When a change spans multiple tasks or also changes the use-case document, split it into an ordered task list. Default execution handles only the current task and one production code file; continue only when explicitly requested.
14. One task touches one task document and one production code file. Add one matching unit-test file only when tests or TDD are explicitly requested.
15. A task document's basic measure is a class or type group.
16. Use `$cx-workflow` for routing and skill selection.
17. Use `$cx-story` for use cases, main success scenarios, conditional substeps, task splits, and changes.
18. Use `$cx-tdd` only when TDD or unit tests are explicitly requested; add `$cx-pytorch-tdd` only for explicit Python/PyTorch tests. Use `$cx-rust-tdd` for Rust implementation, with Rust tests only when explicitly requested.
19. Use `$cx-common-module` before adding reusable features, classes, or common entrypoints.
20. Run the narrowest effective test first, then broader validation as needed, and record commands and results.
21. After production code is complete, run `$cx-evidence` or an equivalent local code-review flow. Mark the task or change complete only after review passes.

## docs/cx Layout

```text
docs/cx/
docs/cx/00.project.md
docs/cx/01.create_user/
docs/cx/01.create_user/00.use_case.md
docs/cx/01.create_user/00.design.md
docs/cx/01.create_user/tasks/
docs/cx/01.create_user/tasks/01.write_user_entity/00.task.md
docs/cx/01.create_user/changes/
docs/cx/01.create_user/changes/20260629T120000-task01-write_user_entity.md
```

Do not create scattered `spec.md`, `plan.md`, `tasks.md`, or design documents. Plans belong in the current task or change document. Verification evidence belongs in the current task or change document.

## Prompt Contract

A coding-agent prompt should include goal, context, constraints, required workflow, verification, deliverables, and branch expectations.

## Skill Routing

- `$cx-workflow`: workflow routing and skill orchestration.
- `$cx-story`: use cases, main success scenarios, conditional substeps, task folders, change folders, and current task document.
- `$cx-tdd`: explicit test-first implementation and verification evidence.
- `$cx-changelog`: `changes/` documents, release notes, and audit trails.
- `$cx-version`: project-local `tools/semver.py`, SemVer, `VERSION`, `docs/VERSIONS.md`, and annotated tags.
- `$cx-research`: model selection, paper research, source filtering, and cited synthesis.
- `$cx-pytorch-tdd`: Python, PyTorch, Lightning, tensors, training, and ML tests.
- `$cx-pytorch-quick-hpo`: quick PyTorch tuning and candidate screening.
- `$cx-pytorch-full-hpo`: full PyTorch tuning and release candidate selection.
- `$cx-timeseries-modeling`: heterogeneous multivariate time-series modeling.
- `$cx-rust-tdd`: Rust implementation, ownership design, and cargo test/fmt/clippy.
- `$cx-common-module`: reusable features, reusable classes, and common API design.
- `$cx-evidence`: pre-merge or pre-handoff evidence review.
- Mandatory post-code review uses `$cx-evidence`; a failed review means the task is not complete.

## Python Rules

- Source code lives under `src/<subsystem>/`.
- Use project-level `uv` environments and `uv run`.
- Check official Python and PyTorch stable versions before creating or rebuilding Python/PyTorch environments.
- Use full OOP for domain logic. Tiny purely stateless logic may remain as short functions; state, lifecycle, invariants, and domain collaboration use OOP.
- Do not add command-line argument parsing to target-project scripts; use config items with defaults.
- Do not default to dynamic reflection.
- When Python unit tests are explicitly requested, use `unittest` unless the project already uses another framework.
- When unit tests are explicitly requested, tests mirror `src` one-to-one.
- Tensor tests cover shape, dtype, device, determinism, and edge cases.
- Training tests stay tiny.

## Rust / GPUI Rules

- When Rust unit tests are explicitly requested, use built-in test mechanisms and `cargo test`.
- Run `cargo fmt` and `cargo test`; run `cargo clippy --all-targets --all-features` when practical.
- Model domain state with struct, enum, trait, and explicit `Result`.
- Avoid `unwrap`, `expect`, and `panic!` in production paths unless locally proven and documented.
- Separate pure state, reducers, and rendering.
- After Rust/GPUI desktop UI changes, launch or package the real app and observe it on device.
- Put temporary screenshots and UI verification artifacts under `temp/` or the project temporary directory.

## Git Rules

- User-requested commits, deliveries, PRs, or releases treat the working tree as one complete change set.
- `git status --short` is for risk visibility, not ownership splitting.
- Stage tracked and untracked files by default unless obvious secrets, credentials, local env files, build outputs, dependency directories, or unrelated large files appear.
- Completed local work branches merge to `main` after user confirmation and are then deleted.
- Do not push work branches unless the user explicitly overrides the main-only remote policy.

## Recommended Validation

```bash
python -m black --check src tests tools
python -m unittest discover -s tests
cargo fmt --check
cargo test
cargo clippy --all-targets --all-features
```

If the project installs cx validation tools, run `python tools/validate_single_source.py`.
