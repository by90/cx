---
name: cx-workflow
description: Use for workflow handling, task routing, end-to-end development orchestration, selecting the right cx skills, and deciding whether BDD, TDD, changelog, release versioning, research, evidence review, or clarification is needed.
version: 0.1.0
---

# cx Workflow Handling

## Purpose

Use this skill as the cx workflow entry point and skills command officer. It must analyze the user's request, recommend the smallest suitable cx skill combination, order the work, and ask for clarification when missing requirements would make implementation unsafe.

## Entry Flow

1. As the skills command officer, classify the task: requirements discussion, feature implementation, bug fix, refactor, specialist technical work, documentation update, evidence review, or installation/use question.
2. For any multi-step task, create a todo list in the conversation first; during execution, update each item until it is completed, canceled, or explicitly blocked.
3. For any feature-group work, require a short-lived local work branch before changing files. Completed work branches merge into `main`, then are deleted locally; the remote keeps only `main` and version tags.
4. Check whether the project already has `docs/INDEX.md` or `docs/README.md`, one or more documentation sets, and `AGENTS.md`.
5. Decide whether the request changes behavior, public APIs, data structures, user workflows, release mechanics, or research conclusions.
6. Based on task type, impact scope, user-named skills, and existing project rules, recommend the smallest necessary cx skill combination and execution order. Do not apply every skill by default.
7. Select the target documentation set. Every project is organized as multiple feature groups, and concrete engineering documents must live under numbered lowercase underscore folders such as `docs/001_feature_name/`.
8. If the task involves a generic capability, reusable feature, reusable class, shared tool, configuration, logging, paths, cache, environment probing, or data-access entrypoint, enter the "generic/reusable capability gate" before BDD/TDD or implementation.
9. State the current step or execute directly. Ask first only when a missing requirement would likely cause the wrong implementation.

## Hard Constraints

1. For development work that needs BDD, an engineering spec, an implementation plan, or a changelog entry, stop after updating the documents, report the document result to the user, and wait for explicit user confirmation. Do not write tests, edit implementation, or enter TDD before that confirmation.
2. Any task that needs cx skills must first use `$cx-workflow` as the skills command officer to analyze the user's task and recommend the smallest suitable skill combination and execution order in the conversation. If the user explicitly names a skill, include that skill in the combination and add only the necessary cooperating skills.
3. When the target project has the Chinese cx package installed, every cx-generated or cx-maintained document must be Simplified Chinese, including `BDD.md`, `ENGINEERING_SPEC.md`, `CHANGELOG.md`, `docs/INDEX.md`, plans, test matrices, and verification evidence. Code identifiers, commands, API names, and quoted external names may remain in their source language.
4. When the user asks to commit, deliver, open a PR, or release, treat the working tree as one change set: stage tracked and untracked files and make one commit. Do not analyze which files were changed by the assistant versus the user, and do not split commits by ownership; stop first only for obvious secrets, build artifacts, or unrelated large files.
5. After work is complete and user-confirmed, merge the related work branch into `main` and delete the local branch. Do not push work branches to the remote unless the user explicitly overrides the main-only remote policy in the current conversation; by default, push only `main` and version tags.
6. Use "verified basis" or "verification evidence" for information backed by documents, tests, command output, or cited sources. Do not use the unclear phrase "engineering facts."
7. Any implementation, fix, refactor, generic capability, reusable feature, reusable class, or reusable-capability extraction task must follow the corresponding implementation skill's `## Minimal Implementation Discipline`: absolutely no unmaintainable pile-up code, and default to the least code that satisfies the current need.
8. Programming tasks default to fast failure during development: unless the business explicitly needs degradation, recovery, or user-visible guidance, do not catch, swallow, fall back, silently skip, or wrap exceptions that would cause product problems; those errors must stop execution and surface to tests or callers.
9. Programming tasks must not use broad prechecks, per-item validity checks inside large loops, hot-path fallbacks, or silent batch filtering to hide data errors or slow performance. Put data-validity checks at entrypoints, data preparation, test fixtures, or separate diagnostic tasks.
10. Before implementing a generic capability, reusable feature, or reusable class, first define the calling model; until that model is written into BDD/ENGINEERING_SPEC, do not write internal loading, validation, conversion, caching, or persistence code.
11. Before long-running execution, builds, tests, installation, or UI real-device checks, find and start the project-provided keep-awake or session-preservation mechanism for the current platform; it must be temporary and reversible, and must be stopped before ending, blocking, or handing off the turn.
12. When running Python tests, builds, or tooling commands, prefer the project `uv` workflow or a Python interpreter installed and managed by `uv`, such as `uv run python ...` or `uv run --python <version> ...`; do not default to the system Python as a substitute.

## Generic/Reusable Capability Gate

When a task involves a generic capability, reusable feature, reusable class, or shared tool, first organize and record this contract:

```text
Public entrypoint:
Normal call style:
Special-case entrypoint:
Instance or state lifecycle:
State source:
How tests cover all source call sites:
Non-goals:
```

- Public entrypoint states what callers import or instantiate first.
- Normal call style states the default use path in production code.
- Special-case entrypoint states how tests, alternate folders, temporary data, or environment overrides are supplied when they are truly needed.
- Instance or state lifecycle states whether the capability is per object, a shared instance, lazy property, cache, context, or stateless function.
- State source states whether values come from constructor parameters, instance attributes, files, environment probing, database, or caller-provided data.
- How tests cover all source call sites states how tests redirect the public entrypoint without relying on hidden global mutation.
- Non-goals list validation, exception wrapping, dynamic discovery, persistence, or future extension points that are not required by the current task.

## Prompt Intake Contract

When the user request is vague, normalize it into this contract before planning:

```text
Goal:
Context:
Branch:
Constraints:
Required workflow:
Verification:
Deliverables:
```

- Goal must describe observable behavior or a concrete research/release outcome.
- Context should identify target docs, files, branch, environment, and relevant prior decisions.
- Branch should name the local feature-group branch, confirm the integration target is `main`, and state that the remote keeps only `main` and version tags.
- Constraints should include public APIs, language rules, compatibility, performance, security, or style limits.
- Required workflow names the smallest necessary cx skills.
- Verification lists the commands, checks, screenshots, or evidence expected.
- Deliverables state what will be changed and what summary/evidence is required.

Ask a clarifying question only when a missing field would likely cause wrong behavior, unsafe changes, or unverifiable work. Otherwise proceed and state assumptions briefly.

## Skill Selection

- Behavior discovery, requirements, acceptance criteria, business rules, or scenario writing: use `$cx-bdd`.
- Test-first implementation after BDD is clear: use `$cx-tdd`.
- Behavior changes, bug fixes, architecture changes, or implementation planning: use `$cx-bdd`, then `$cx-tdd`.
- Do not create BDD automatically for ordinary non-programming tasks; if it is unclear whether behavior discovery is needed, ask the user one minimal clarification question.
- Changelog-only updates or change ID checks: use `$cx-changelog`.
- Release version decisions, SemVer bumps, tags, or release notes: use `$cx-version`.
- Model selection, model mechanism research, recent AI papers, academic/blog synthesis, or research reports: use `$cx-research`.
- Python, PyTorch, Lightning, tensor, or ML tests: add `$cx-pytorch-tdd`.
- PyTorch quick tuning, field-contribution research, feature sets, window length, labels, training hyperparameters, optimizer/scheduler choices, or model-capacity screening: add `$cx-pytorch-quick-hpo`, and add `$cx-pytorch-tdd`, `$cx-timeseries-modeling`, `$cx-research`, and `$cx-common-module` as needed.
- PyTorch full-data tuning, complete-data training, test-set evaluation, backtesting, top-3 candidate comparison, or release-candidate model selection: add `$cx-pytorch-full-hpo`, and add `$cx-pytorch-tdd`, `$cx-evidence`, and `$cx-version` as needed.
- Heterogeneous multivariate time series, forecast horizons, covariates, backtesting, or time-series framework choice: add `$cx-timeseries-modeling`.
- Rust implementation or Rust tests: add `$cx-rust-tdd`.
- Generic capability, reusable feature, reusable class, shared tool, stable API, reusable component, or duplicated logic migration: add `$cx-common-module`.
- Final delivery checks, test evidence, or documentation consistency: use `$cx-evidence`.

## Execution Order

1. For multi-step tasks, create a todo list in the conversation first; update item status whenever an item is completed, canceled, or blocked.
2. For normal programming development tasks, start or switch to a dedicated feature-group branch before editing project files.
3. Then use `$cx-bdd`, choose or create the target ordered feature folder, such as `docs/001_config_system/`, and update `BDD.md`, `ENGINEERING_SPEC.md`, and `CHANGELOG.md`.
4. After the document update is complete, stop, report the document changes and next implementation plan to the user, and wait for explicit user confirmation.
5. After user confirmation, use `$cx-tdd` and any specialist skill to write the failing test, record the red failure, implement the smallest change, and validate it.
6. When a feature group is complete and user-confirmed, merge its local branch into `main`, delete the local branch, and do not push the work branch to the remote.
7. For finishing work around an existing implementation, check docs and test evidence before using `$cx-evidence`.
8. For ordinary non-programming tasks, such as installation, updates, language switching, shskills usage, read-only research organization, small wording edits, or maintenance documentation updates, answer or make the update directly and do not start BDD/TDD; if the task boundary may affect business behavior, ask whether BDD is required.
9. For read-only analysis or code review, read the relevant files and list risks before making changes, unless the user asks for fixes.
10. For every project, record multiple feature groups, order, dependencies, and status in `docs/INDEX.md`; never place concrete engineering documents in the `docs/` root as a single-feature documentation set.
11. For potentially reusable features, classes, components, data structures, test harnesses, or UI state models, use `$cx-common-module` first to search existing implementations and registries before adding a new abstraction.
12. For component domains such as progress UI or ragged tensor utilities, do not invent a new cx skill. Treat them as project components with their own README and tests.
13. For release work, use `$cx-version`: after the user confirms the version is complete, merge the completed local work branch into `main`; only `main` may be used for the version commit, annotated release tag, and release-tag push. The remote should retain only `main` and version tags.
14. Before finalizing, confirm the conversation todo list is completed, canceled, or explicitly blocked, and report that the keep-awake mechanism was stopped along with validation results and residual risk.

## Stop Conditions

- Critical business rules, target environment, or acceptance criteria are missing and continuing would create likely rework.
- The requested implementation conflicts with the current `AGENTS.md`, technical constraints, or public API.
- High-risk or fast-changing information must be verified online, but the environment cannot verify it.

When a stop condition applies, state the blocker and ask the smallest set of questions needed to continue.
