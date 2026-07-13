# AGENTS.md

## Startup Requirement: Windows Chinese Encoding

Before reading, searching, writing, or displaying Chinese files in Windows PowerShell, set the current command channel to `UTF-8`. `PowerShell` is the Windows command shell name, and `UTF-8` is the encoding standard; these names are kept to match real commands and standards.

In Windows PowerShell 5.1, run these commands first:

```powershell
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8NoBom
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom
```

If Chinese terminal output shows mojibake, do not judge file content from that output. Use `apply_patch`, structured search, explicitly encoded read commands, or saved `UTF-8` scripts for Chinese prose. State the mojibake fact and handling method only once; then continue directly instead of repeating the same warning before every file operation.

## Startup Requirement: Windows PowerShell 5.1 Command Compatibility

In native Windows Codex App sessions, write commands for Windows PowerShell 5.1 by default unless the current shell has already been confirmed as PowerShell 7 or newer. `Codex App` is the local desktop application name, and `PowerShell 7` is the newer shell name; these names are kept to match the real product and version.

Do not use `&&` or `||`, because Windows PowerShell 5.1 does not support those command connectors. When commands must run in sequence, use separate command calls. When the next command depends on the previous command succeeding, run them step by step and check the exit result. Do not discover shell capability by trying a command, letting it fail, and then rewriting it.

## Decision Prompts

When facing architecture tradeoffs, API design, dependency choices, implementation paths, performance or compatibility tradeoffs, release strategy, repeated defects, or project risk, prefer one of these decision frames: first principles, inversion, five whys, second-order thinking, regret minimization, opportunity cost, or premortem analysis.

## Iron Rules

These rules override other rules, cx skills, templates, examples, and temporary task instructions unless the user explicitly overrides one in the current conversation.

1. **Commits and pushes do not split by source**: when the user asks for a commit, delivery, PR, or release, treat the current working tree as one complete change set and stage tracked plus untracked files.
2. **Comprehensive comments**: all new or edited source and unit-test files need file-level purpose notes, class/type notes, function notes, and line-by-line business-code intent comments.
3. **Default one-task one-code-file execution**: establish the task set and each production-file binding once when a new story is created. Before programming or workflow development, complete the current original task and edit only its one production file. After story creation, a file or implementation change first enters a temporary change and rewrites the original task; never add, delete, or rename task files. Continue into another original task only when the user explicitly requests multi-task continuation.
4. **Language package document language**: English package documents should be English; Chinese package documents must be Simplified Chinese.
5. **Explicit unit tests**: by default, do not create, edit, or run unit tests. Create or edit one matching test file only when the current user request, existing task document, or change document explicitly asks for unit tests, TDD, failing tests, or red-green-refactor. When unit tests are explicitly requested, tests mirror `src`; `src/<subsystem>/xx.py` maps only to `tests/<subsystem>/xx_test.py`.
6. **Default parameters first**: prefer clear type annotations and default parameters over large constructor branching. Configuration defaults should be written directly as default parameters, for example `path=Config.default_config_file()` or `batch_size=config.train.batch_size`; inside the function body, store the parameter on a same-named field, for example `self.batch_size = batch_size`.
7. **Full object-oriented design, minimal code, and reuse first**: use full object-oriented design for state, lifecycle, invariants, and domain collaboration. Avoid bloated code, overly long files, overly long variable names, and sentence-like identifiers. Search and design functional entrypoints with `$cx-common-module` before adding reusable logic. Do not default to dynamic reflection, monkey patching, dynamic injection, or string dispatch.
8. **Python scripts do not accept command-line parameters**: target-project scripts take adjustable behavior from config-subsystem items with defaults.
9. **Development keeps only the latest intent**: every source file, interface, parameter, configuration item, path, caller, document, example, and explicitly declared test targets the current latest intent. Never keep old interfaces, old entries, aliases, adapters, bridges, coexistence branches, compatibility parameters, compatibility configuration, compatibility paths, old-behavior fallbacks, or any old trace. Migrate callers to the current entry and delete all old code, documentation, examples, and tests.
10. **Original error propagation**: unless the user explicitly requests one specific validation or error behavior in the current request, never add a series of validations that raises an error and never catch, translate, wrap, swallow, silently skip, default, return an empty result, fake retry success, or degrade from an error. Preserve the original error type, message, and stack and let it stop the program. Model normal business states explicitly, but never turn a program error into a continuing business branch.
11. **No fallback prechecks in performance paths**: data validity belongs at entrypoints, data preparation, fixtures, or diagnostics, not hot-path filtering.
12. **No automatic cx use-case flow for ordinary non-programming work**: ask a minimal clarification question when unsure.
13. **Visible todos**: create and update a visible todo list for multi-step work.
14. **Use uv Python**: run Python scripts, tests, builds, and tools with `uv` managed Python.
15. **Avoid mixed-language prose**: use the package language for conversations, explanations, plans, summaries, documents, review decisions, verification evidence, and comments. In Chinese-language conversations and Chinese-package documents, any unavoidable English identifier, command, path, API name, library, protocol, standard, proper name, or ambiguity-sensitive term must be explained in Chinese in the same sentence or an adjacent sentence, including its meaning, role, and why the English form is kept. In English-package prose, explain unavoidable non-English source terms in English.
16. **Cross-platform encoding**: PowerShell scripts use UTF-8 with BOM; other source, Markdown, JSON, TOML, YAML, and text files use UTF-8 without BOM. Windows PCs can handle Chinese projects correctly, but file encoding, console display encoding, pipeline encoding, external-program argument encoding, and terminal fonts are separate layers; mojibake in one layer must not be treated as file corruption. On Windows, prefer PowerShell 7 or newer for non-PowerShell text because it defaults to UTF-8 without BOM. When using Windows PowerShell 5.1, explicitly set `[Console]::InputEncoding`, `[Console]::OutputEncoding`, and `$OutputEncoding`, and pass explicit encodings to text commands such as `Get-Content`, `Set-Content`, `Select-String`, and `Out-File`. Scripts may batch-edit Chinese text, but the script file, input files, output files, and invocation channel must all use explicit UTF-8 and preserve the target file's BOM policy. Do not pass Chinese replacement tables, prose, or code to external programs through PowerShell inline strings, command-line arguments, or here-strings unless that encoding path has been verified. For batch edits, prefer saved UTF-8 script files, project `uv` Python, PowerShell 7 `-Encoding utf8NoBOM`, or explicit BOM-free .NET writes; for precise small edits, use `apply_patch`. Modify file encoding or explain encoding details only when the file is actually encoded incorrectly, a patch fails, or the user explicitly asks.
17. **Chinese first, English second**: when modifying cx workflow, skills, templates, examples, or install rules, finish the Chinese package first and then synchronize English.
18. **Explicit tests and full object-oriented design**: Python, PyTorch, and Rust projects do not use unit tests or TDD by default. Run test-first flow only when explicitly requested. State, lifecycle, invariants, and domain collaboration use full object-oriented design or equivalent type modeling.
19. **Mandatory unified review after deliverables**: after code, documentation, tutorials, research, design, process work, release notes, or any other deliverable is produced, use `$cx-review` for artifact-quality review and the completion-evidence gate. Code review checks agreement with the current use case, design, original task, and unfinished change; prior topic-document and common-capability discovery; duplication; object modeling; latest-only interfaces; original error propagation; minimal code; and business semantics. Documentation, tutorial, research, and design review check current-state uniqueness, executability, source quality and synthesis, feasibility, and meaning. A failure in either stage keeps the task unfinished and the active change file present.
20. **Bloated code must be deleted**: any source code, tests, scripts, tools, examples, or workflow-generated code that turns behavior expressible with a few fields, direct array slicing, standard-library semantics, or one clear constructor into hundreds or thousands of lines is incomplete and fails review. This rule applies across languages, directories, and skills; do not relax it for TDD, compatibility, debugging, future extension, or looking complete. Do not add protocol inheritance, convenience wrappers, clone methods, rebuild methods, fallback validation, negative-index compatibility, mask padding, debug entrypoints, future-extension entrypoints, or test-only entrypoints unless the current use case requires them. Before coding, list the smallest functional entrypoint and non-goals; after coding, delete functions, properties, classes, and tests with no real call site, no reduction in caller complexity, and no isolation of real complexity. Code should be direct, short, and close to the data structure and business semantics; do not wrap behavior callers can express with arrays, tensors, standard slicing, constructors, or configuration defaults.
21. **Global numeric type rule**: every new or edited `NumPy` array, PyTorch tensor, model input, indicator matrix, intermediate result, training datum, level value, category value, entity id, time id, row id, group offset, and index array must use type objects from the project config. Projects should define config items for continuous numeric type, level/category type, and index type, and performance paths must use those type objects directly instead of parsing strings inside loops, data loading, indicator computation, batching, training, inference, loss computation, or test fixtures. Except in config definitions, tests that assert config defaults, and config documentation that explains defaults, do not hard-code `np.float32`, `np.float64`, `np.float16`, `np.int64`, `np.int32`, `np.int8`, `torch.float32`, `torch.float64`, `torch.float16`, `torch.bfloat16`, `torch.int64`, `torch.int32`, or equivalent numeric types in production paths, test fixtures, or documentation examples. If a project uses a `NumPy` data layer and `NumPy` has no native `bfloat16`, do not use a third-party package to extend `NumPy` for that type; ML code may choose `torch.bfloat16` through PyTorch model config.
22. **cx source repository modification rule**: when modifying cx workflow, skills, templates, examples, install rules, or global `AGENTS.md` templates, modify only the cx source repository as the durable source. Do not hand-edit the local global install directory as the final result. After every modification, commit and push `main`, then run the matching install script so local global cx skills and `AGENTS.md` are updated from the remote source.
23. **Current state and Git history**: project, use-case, design, task, topic, research, and interface documents state only current valid facts. Never preserve an old solution, old/new comparison, migration process, completed change, or development process in durable documents. Only the active unfinished change file may state old/new differences. Commit that file before work; delete it after unified review passes and commit the deletion. Git commits, tags, and releases are the only history source.

## Repository Workflow

This repository uses a `docs/cx` use-case-driven flow. All cx project descriptions, scenarios, tasks, process documents, and changes live under `docs/cx`; documents elsewhere are unrelated to cx.

1. cx documents must state concrete facts, concrete actions, and concrete decisions. Avoid filler, repeated goals, missing "what to do", and undefined invented terms.
2. Project documents contain project goals, key terms, design constraints, and a use-case index. Number goals with `1. 2. 3.` and state the result plus why it is needed.
3. Use cases contain actors, preconditions, triggers, main success scenario, step-attached conditional substeps, sub-use cases, and observable completion. Do not put test plans, implementation tasks, or repeated project goals inside use-case bodies.
4. Design documents contain file scope, functional entrypoints, reusable capabilities, design decisions, tradeoff reasons, and verification. Task documents contain what to do, file scope, task measure, verification, and status.
5. `changes/` stores only current unfinished work instructions. For a requirement change, design change, implementation change, or code error in an existing story, create or update the change file and commit it before implementation.
6. Define new terms on first use and prefer user/project terms.
7. Before planning or code changes, read relevant `docs/cx/docs/` topics, then project context, the target use case, design, original task, and unfinished changes.
8. Start by reading topic documents and searching registered common packages, then use unfinished changes to decide current work.
9. Each main success scenario has one folder, such as `docs/cx/01.create_user/`.
10. Each scenario folder contains `00.use_case.md`, `00.design.md`, `tasks/`, and `changes/`.
11. The use-case document expresses the main success scenario and conditional, alternate, or exception substeps attached to concrete main steps.
12. One `docs/cx/NN.name/` folder carries one user-goal use case. Do not use a vague "use the app" use case to hold a whole application, page set, menu, or several independent operations.
13. The main success scenario describes the most common path from trigger to completed user goal, usually 3 to 9 main steps. Each step is one observable actor-system interaction.
14. If a main-success step needs its own actors, preconditions, main success scenario, and conditional substeps, it is a sub-use case or separate use case and should move to a new `docs/cx/NN.name/` folder; the original step should use a substep such as "enter use case: X".
15. Conditional, alternate, and exception behavior must attach to a concrete main-success step with substep numbering such as `1.1` or `2.1`. Split complex conditional flows into separate use cases when they exceed 3 to 5 steps, introduce a new actor, have independent completion criteria, or need independent tasks and tests.
16. The design document explains reusable code, new common code, and design decisions.
17. Each task is one Markdown file starting at `01.`, such as `tasks/01.write_user_entity.md`; do not create generic `00.task.md` files.
18. Each change is one Markdown file without a timestamp in the filename, such as `changes/adjust_user_entity_constraints.md`.
19. When a change spans multiple original tasks or also changes the use-case document, list an ordered work sequence in the change file. Default execution handles only the current original task and one production file; continue only when explicitly requested.
20. Establish the task set once when a new story is created. After creation, task count, numbers, filenames, and identities stay fixed. Requirement changes, implementation changes, and code errors rewrite original task documents and never create fix, remove, modify, or reimplementation tasks. One task owns one production file and, only when explicitly declared, one matching unit-test file.
21. A task document's basic measure is a class or type group.
22. Use `$cx-workflow` for routing and skill selection.
23. Use `$cx-story` for use cases, main-success scenarios, conditional substeps, fixed task sets, and current state. Use `$cx-changelog` for temporary changes.
24. When TDD or unit tests are explicitly requested, use `$cx-tdd` as the single main workflow. Add `$cx-pytorch-tdd` for Python, PyTorch, or Lightning tests, and add `$cx-rust-tdd` for Rust tests. Do not use either language test skill without an explicit test requirement.
25. Before reusable features, classes, or common entries, use `$cx-doc` to read topic documents and `$cx-common-module` to search registered capabilities and real callers.
26. Every common package, stable interface, protocol, data process, feature system, and technical direction has an independent numbered topic document under `docs/cx/docs/`.
27. Every research effort saves its question-specific current conclusion under `docs/cx/notes/` and explains it plainly.
28. Run the narrowest effective verification first, then broader validation as needed, and record commands and results in the original task.
29. After any deliverable, use `$cx-review` for artifact quality and the completion-evidence gate. A failure in either stage keeps the task unfinished and the current change file present.

## docs/cx Layout

```text
docs/cx/
docs/cx/00.project.md
docs/cx/docs/
docs/cx/docs/00.index.md
docs/cx/docs/01.market_data_server_protocol.md
docs/cx/notes/
docs/cx/notes/01.choose_time_series_model.md
docs/cx/01.create_user/
docs/cx/01.create_user/00.use_case.md
docs/cx/01.create_user/00.design.md
docs/cx/01.create_user/tasks/
docs/cx/01.create_user/tasks/01.write_user_entity.md
docs/cx/01.create_user/changes/
docs/cx/01.create_user/changes/adjust_user_entity_constraints.md  # exists only while unfinished
```

Do not create scattered `spec.md`, `plan.md`, `tasks.md`, or design documents. Plans belong in the original task or active unfinished change. Verification belongs in the original task. Delete the change file after completion. Durable documents describe only current state.

## Prompt Contract

A coding-agent prompt should include goal, context, constraints, required workflow, verification, deliverables, and branch expectations.

## Skill Routing

- `$cx-workflow`: workflow routing and skill orchestration.
- `$cx-story`: use cases, main-success scenarios, conditional substeps, fixed task sets, and current task documents.
- `$cx-tdd`: explicit test-first implementation and verification evidence.
- `$cx-changelog`: registration, commit, execution, and completion deletion of temporary `changes/` files.
- `$cx-doc`: topic documents, common-package documentation, stable technical processes, and research notes.
- `$cx-version`: project-local `tools/semver.py`, SemVer, `VERSION`, `docs/VERSIONS.md`, and annotated tags.
- `$cx-research`: model selection, paper research, source filtering, and cited synthesis.
- `$cx-design`: object-oriented design, responsibility splitting, domain objects, class naming, inheritance/composition, database-access boundaries, field enums, and implementation-path tradeoffs.
- `$cx-pytorch-tdd`: adds Python, PyTorch, and Lightning tools, layout, real data, and tensor checks to the `$cx-tdd` main workflow.
- `$cx-pytorch-quick-hpo`: quick PyTorch tuning and candidate screening.
- `$cx-pytorch-full-hpo`: full PyTorch tuning and release candidate selection.
- `$cx-timeseries-modeling`: heterogeneous multivariate time-series modeling.
- `$cx-rust-tdd`: adds Rust built-in tests, shared real-data fixtures, and `cargo` checks to the `$cx-tdd` main workflow.
- `$cx-common-module`: reusable features, reusable classes, and functional entrypoint design.
- `$cx-review`: artifact-quality review, the completion-evidence gate, current-state consistency, and residual risk.
- A failure in either `$cx-review` stage means the task is incomplete and the active change file remains.

## Python Rules

- Source code lives under `src/<subsystem>/`.
- Use project-level `uv` environments and `uv run`.
- Check official Python and PyTorch stable versions before creating or rebuilding Python/PyTorch environments.
- `NumPy`, PyTorch, indicator matrices, training data, level values, category values, ids, row ids, and index arrays must use type objects from the config subsystem; except in config definitions, tests that assert config defaults, and config documentation that explains defaults, do not hard-code numeric types in business code, performance paths, test fixtures, or documentation examples.
- Use full object-oriented design for domain logic. Tiny purely stateless logic may remain as short functions; state, lifecycle, invariants, and domain collaboration use object-oriented design.
- Constructors and functions express configuration defaults with default parameters, for example `path=Config.default_config_file()` or `batch_size=config.train.batch_size`, and store parameters on same-named fields.
- Common packages must have independent numbered topic documents under `docs/cx/docs/` that explain current public entries and usage. Other documents link to the topic without copying details.
- Do not add command-line argument parsing to target-project scripts; use config items with defaults.
- Do not default to dynamic reflection.
- When Python unit tests are explicitly requested, use `unittest`. Do not introduce `pytest` unless the current user request explicitly requires it.
- When unit tests are explicitly requested, tests mirror `src` one-to-one.
- `src/` and its subdirectories contain blank `__init__.py` files. Root `tests/__init__.py` loads the test database and constructs shared real-data objects and must not be blank; other test-package directories contain blank `__init__.py` files.
- Project imports use absolute imports from the repository root, such as `from src.config.config import Config`; tests must not modify `sys.path`.
- Explicit Python unit tests must be discoverable and runnable from the VS Code test view; use unittest discovery arguments `-v -s ./tests -p *_test.py -t .`.
- Tensor tests cover shape, dtype, device, determinism, and edge cases.
- Training tests stay tiny.
- Data-related Python tests use real test-database records loaded once by `tests/__init__.py`; individual test files never reread the database. Do not write mock tests unless the current user request explicitly requires them.

## Rust / GPUI Rules

- When Rust unit tests are explicitly requested, use built-in test mechanisms and `cargo test`.
- Run `cargo fmt` after Rust changes. Run `cargo test` only when unit tests or TDD are explicitly required, and run `cargo clippy --all-targets --all-features` when practical.
- Data-related Rust tests use real test-database records through one shared fixture module and a one-time initialization mechanism; individual test modules never reread the database. Do not use mocks or fake repositories unless the current user request explicitly requires them.
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
python -m unittest discover -v -s ./tests -p "*_test.py" -t .
cargo fmt --check
cargo test
cargo clippy --all-targets --all-features
```

If the project installs cx validation tools, run `python tools/validate_single_source.py`.
