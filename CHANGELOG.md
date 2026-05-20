# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Added a hard workflow gate requiring agents to stop after BDD/spec/changelog updates and wait for explicit user confirmation before tests or implementation.
- Strengthened Chinese-pack documentation rules so all cx-maintained documents must be Simplified Chinese when the Chinese package is installed.
- Expanded AGENTS guidance for Git submission: stage tracked and untracked files as one working-tree change set and create a single commit without splitting by file ownership.
- Added post-completion Git flow rules: merge feature branches into `dev`, delete local feature branches after merge, and push feature branches only on explicit user request.
- Added Windows toolchain guidance to install a required `ng` CLI instead of replacing it with PowerShell or `ps` substitutes.
- Documented "verified basis" or "verification evidence" as the replacement wording for the unclear phrase "engineering facts".

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
- Added ordered feature-folder naming such as `docs/1.配置系统/`, with matching `BDD.md` heading and `Feature:` name.

### Removed

- Removed Progress UI, Rust UI, and Ragged Tensor as installable cx skills. Those are implementation/component domains and should be documented by the component README when such components exist, not shipped as core workflow skills.
- Removed the combined `$cx-bdd-tdd` skill in favor of separate `$cx-bdd` and `$cx-tdd` skills.
