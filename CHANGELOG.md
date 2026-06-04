# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Added a Python development iron rule requiring target-project scripts to avoid command-line arguments and route adjustable behavior through config-subsystem items with defaults.
- Added PowerShell cx installers that update skills from remote `main` and overwrite the global Codex `AGENTS.md` with the matching language package template.
- Added `$cx-pytorch-hpo` for broad PyTorch experiment tuning with Optuna as the default primary tool and Ray Tune/BoTorch as scoped alternatives.
- Added `$cx-timeseries-modeling` for heterogeneous multivariate time-series design with PyTorch Forecasting as the primary reference framework.
- Added a development-stage no-legacy-compatibility iron rule to AGENTS, `$cx-pytorch-tdd`, and `$cx-rust-tdd`.

## [0.1.2] - 2026-05-27

### Changed

- Added GPUI/macOS real-device verification guidance to `$cx-rust-tdd`, including Accessibility permission checks, screenshot-based coordinate calibration, and CoreGraphics HID click fallback for GPUI content controls.
- Added the same GPUI/macOS click and temporary-artifact rules to the English and Chinese AGENTS templates so coding agents know how to test real desktop UI interactions.

## [0.1.1] - 2026-05-26

### Changed

- Added a visible todo-list workflow rule requiring agents to create a conversation checklist before multi-step work, update item status during execution, and finish only after every item is completed, canceled, or explicitly blocked.
- Added platform runtime rules for temporary keep-awake mechanisms, macOS GUI real-app checks through Computer Use or project-defined real-device checks, and evidence recording for those observations.
- Clarified that Python commands should use the project `uv` workflow or a Python interpreter installed and managed by `uv`, rather than defaulting to system Python.
- Clarified the default version policy: when users only ask to update, bump, or prepare a version, use a patch bump unless an earlier version segment is explicitly requested.
- Added a hard workflow gate requiring agents to stop after BDD/spec/changelog updates and wait for explicit user confirmation before tests or implementation.
- Strengthened Chinese-pack documentation rules so all cx-maintained documents must be Simplified Chinese when the Chinese package is installed.
- Expanded AGENTS guidance for Git submission: stage tracked and untracked files as one working-tree change set and create a single commit without splitting by file ownership.
- Added Windows toolchain guidance to install a required `ng` CLI instead of replacing it with PowerShell or `ps` substitutes.
- Added non-negotiable AGENTS rules for complete commits, comprehensive comments, document confirmation, Chinese documentation, source/test mapping, default-parameter design, minimal code, and OOP access. These rules explicitly override other workflow instructions unless the user overrides a specific rule in the current conversation.
- Added coding and TDD layout rules requiring subsystem source under `src/<subsystem>/`, mirrored one-to-one tests under `tests/`, and explanatory comments for code files, classes, functions, and each line of business code.
- Tightened the comment gate so source files and unit tests must include file-level purpose notes, class notes, function parameter/return explanations, and line-by-line intent comments; also made Black checks mandatory after Python source or test edits.
- Documented "verified basis" or "verification evidence" as the replacement wording for the unclear phrase "engineering facts".
- Refocused `$cx-common-module` and related workflow gates on generic capabilities, reusable features, reusable classes, public entrypoints, lifecycle/state sources, and minimal code instead of module-only abstractions.
- Replaced single-feature/root documentation sets with mandatory numbered feature-group folders such as `docs/001_feature_name/`, and clarified that ordinary non-programming tasks must not create BDD automatically.
- Replaced the target-project version helper with project-local `tools/semver.py`, updated `$cx-version` to require that tool, and clarified the `0.x.x` rule: new feature groups bump minor, while changes inside existing feature groups bump patch.
- Clarified that local cx skills must be installed or updated only from the repository's default `main` branch, without passing `--ref`.
- Replaced the previous `dev` integration branch workflow with a main-only remote policy: local work branches merge into `main`, then the remote keeps only `main` and version tags.

## [0.1.0] - 2026-05-19

### Changed

- Documented mandatory feature-group branching: feature work must happen on its own branch, completed feature branches merge to `dev`, and only user-confirmed releases flow from `dev` to `main`.
- Clarified that completed pre-1.0 feature groups move the package from the `0.0.x` line to the next minor line such as `0.1.0`, while release commits and annotated tags are allowed only on `main`; normal pushes of feature branches and `dev` remain allowed.

## [0.0.1] - 2026-05-19

### Added

- Added `VERSION` as the single source of truth for the cx package release version.
- Added `$cx-version` to define the standard release workflow: SemVer version values, `vX.Y.Z` annotated Git tags, Keep a Changelog release notes, and GitHub Releases.
- Added `$cx-bdd` as a standalone BDD discovery and scenario-documentation skill.
- Added `$cx-tdd` as a standalone test-first implementation skill.
- Added `$cx-research` for model selection, model mechanism research, recent AI paper scans, and citation-backed synthesis.
- Added `$cx-rust-tdd` for general Rust coding and TDD guidance.
- Added root release validation that checks `VERSION`, both language package manifests, and the root changelog agree.

### Changed

- Refocused the package description on the core cx goal: a BDD/TDD human-AI collaboration workflow anchored in durable docs, test evidence, changelog entries, and release evidence.
- Rewrote the English and Chinese root READMEs with detailed explanations for each installable workflow skill.
- Added a coding-agent prompt contract for goal, context, constraints, workflow, verification, and deliverables, aligned with Codex and Claude Code instruction-file practices.
- Rebased cx as an experimental pre-1.0 package starting at `0.0.1`; while major version is `0`, interface and workflow contract changes use minor bumps.
- Strengthened Python/PyTorch guidance with explicit OOP design and dynamic-reflection restrictions.
- Added ordered feature-folder naming such as `docs/001_config_system/`, with matching `BDD.md` heading and `Feature:` name.

### Removed

- Removed Progress UI, Rust UI, and Ragged Tensor as installable cx skills. Those are implementation/component domains and should be documented by the component README when such components exist, not shipped as core workflow skills.
- Removed the combined `$cx-bdd-tdd` skill in favor of separate `$cx-bdd` and `$cx-tdd` skills.
