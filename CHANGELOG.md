# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
