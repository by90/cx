# cx Codex BDD/TDD Workflow Pack

cx is a Codex skill package for disciplined human-AI software development. Its core goal is to make AI-assisted work follow a durable BDD/TDD collaboration workflow: discover behavior with BDD, prove it with TDD, record change history, keep release versions standard, and preserve verification evidence.

cx is not a component library. Implementation domains such as progress UI widgets, ragged tensor utilities, or Rust UI components should live in their own project/component directories with their own README, API docs, and tests. They are not core cx skills.

Current package version: `0.1.0`. cx is still experimental and has not yet been validated as a stable 1.0 workflow.

For Chinese documentation, see [README.zh-CN.md](README.zh-CN.md).

## What cx Installs

This repository publishes two language packs for the same workflow:

- `SKILLS/en`: English skills.
- `SKILLS/zh`: Chinese skills.

Users do not need to clone this repository or install a separate `cx` command. Installation and updates are handled by `shskills`, which reads the repository `SKILLS/` directory from GitHub.

## Prepare shskills

Use it temporarily:

```powershell
uvx shskills --help
```

Install it long-term:

```powershell
uv tool install shskills
```

## Install Or Update

Install the English cx skills into the global Codex skills directory:

```powershell
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:USERPROFILE\.codex\skills" --subpath en --ref main --force --clean
```

If `CODEX_HOME` is set, use:

```powershell
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:CODEX_HOME\skills" --subpath en --ref main --force --clean
```

For Chinese, change `--subpath en` to `--subpath zh`.

## Core Workflow

1. `$cx-workflow` classifies the request and selects the smallest necessary set of skills.
2. `$cx-bdd` creates or updates the ordered feature folder and BDD scenarios.
3. After `BDD.md`, `ENGINEERING_SPEC.md`, and `CHANGELOG.md` are complete, the agent must stop, report the document result and next implementation plan, and wait for explicit user confirmation.
4. After confirmation, `$cx-tdd` maps BDD scenarios to failing tests, runs red/green/refactor, and records evidence.
5. Specialist skills such as `$cx-pytorch-tdd`, `$cx-rust-tdd`, or `$cx-common-module` add language or design constraints.
6. `$cx-changelog`, `$cx-version`, and `$cx-evidence` keep the work auditable before release or delivery.

## Branch And Release Gates

Every feature group must be developed on its own branch. When the feature group is complete, merge that branch into `dev`; do not merge feature branches directly into `main`.

When one feature group is complete during pre-1.0 development, the version moves from `0.0.x` to the next minor line such as `0.1.0`. Confirm the completed version with the user before creating a release.

Release order is strict:

1. Finish the feature group branch and merge it into `dev`.
2. After the user confirms the version is complete, merge `dev` into `main`.
3. Only on `main`, create the version commit, create the annotated `vX.Y.Z` tag, then push `main` and the release tag.

Do not create release commits or tags on feature branches or `dev`.
This gate does not forbid pushing feature branches or `dev` for collaboration, backup, or CI; it only restricts release-version actions to `main`.

## Prompt Contract

cx works best when the human prompt gives the agent a small, explicit contract instead of a vague task. Use this structure for Codex, Claude Code, or any coding agent:

```text
Goal:
Context:
Constraints:
Required workflow:
Verification:
Deliverables:
```

The prompt should name the target feature folder when known, the cx skills to use, commands that must pass, and what evidence should be left behind. If the prompt is missing acceptance criteria, target environment, or verification requirements, `$cx-workflow` should ask the smallest clarifying question. For development tasks that need a documentation set, the agent must wait for user confirmation after documents are complete and before tests or implementation.

For projects that also use Claude Code, keep `AGENTS.md` as the shared source of repository rules and have `CLAUDE.md` import or point to it. Do not maintain two divergent instruction files.

When the Chinese cx package is installed, every cx-generated or cx-maintained document must be Simplified Chinese. When the user asks to commit, deliver, open a PR, or release, the AGENTS template treats the current working tree as one commit and does not split files by who changed them or whether they are untracked.

Feature documentation folders should be ordered and named by business capability:

```text
docs/1.Configuration System/
docs/2.User Sessions/
docs/3.Model Evaluation/
```

The BDD document inside the folder must use the same name:

```text
docs/1.Configuration System/BDD.md
# BDD: 1.Configuration System

Feature: 1.Configuration System
```

Chinese projects use the same convention:

```text
docs/1.配置系统/
docs/1.配置系统/BDD.md
# BDD: 1.配置系统
Feature: 1.配置系统
```

## Available Skills

| Skill | Use for |
| --- | --- |
| `$cx-workflow` | Entry point for task routing, workflow selection, and deciding whether BDD, TDD, research, release versioning, or evidence review is needed. |
| `$cx-bdd` | BDD discovery, ordered feature-folder naming, business rules, Gherkin-style examples, acceptance criteria, and main/alternate/exception scenarios. |
| `$cx-tdd` | Test-first implementation after BDD: red-green-refactor, narrow failing tests, Test Matrix updates, code quality gates, and verification evidence. |
| `$cx-changelog` | `CHANGE-*` entries, changelog consistency, and mapping changes back to the same feature documentation set. |
| `$cx-version` | Release version management using SemVer, root `VERSION`, Keep a Changelog, annotated `vX.Y.Z` Git tags, and GitHub Releases. |
| `$cx-research` | Model selection, model mechanism research, recent AI paper scans, academic/blog synthesis, and citation-backed recommendations. |
| `$cx-pytorch-tdd` | Python, PyTorch, Lightning, tensor utilities, ML tests, deterministic small test data, and strict Python OOP/TDD quality rules. |
| `$cx-rust-tdd` | Rust implementation and TDD: structs/enums/traits, ownership, `Result` errors, `cargo test`, `rustfmt`, `clippy`, and non-UI Rust code quality. |
| `$cx-common-module` | Generic capabilities, reusable features, reusable classes, stable APIs, migration plans, and duplicate logic control. |
| `$cx-evidence` | Final delivery review for BDD/TDD compliance, test output, changelog/spec consistency, and missing evidence. |

## Version Management

cx uses standard release mechanics:

- `VERSION` is the single source of truth and stores a SemVer value without a leading `v`.
- `packages/en/manifest.json` and `packages/zh/manifest.json` must match `VERSION`.
- Root `CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
- Release tags use annotated Git tags named `vX.Y.Z`, consistent with Git release tagging practice.
- GitHub Releases can use the matching changelog section as release notes.

Version numbers use `MAJOR.MINOR.PATCH`:

- New or unproven projects start at `0.0.1` unless the user explicitly says the project has reached `1.0.0`.
- Major version `0` means the project is not formally released. Interface and workflow contract changes are expected during this phase.
- While major version is `0`, minor bumps such as `0.1.0` represent interface or workflow contract changes.
- While major version is `0`, patch bumps such as `0.0.2` represent bugfixes, wording fixes, examples, translations, or validation fixes that do not change the public contract.
- `1.0.0` means the first stable public workflow/API contract after the project is complete and explicitly declared stable.
- After `1.0.0`, compatible public additions use minor versions such as `1.1.0`, and incompatible public contract changes use major versions such as `2.0.0`.

For cx specifically, the split from `$cx-bdd-tdd` into `$cx-bdd` and `$cx-tdd` remains in the pre-1.0 experimental line. The branch/release-gate feature group is released as `0.1.0`; it is not a `1.0.0` stability declaration or a `2.0.0` breaking release.

Useful commands:

```bash
python tools/cx_version.py show .
python tools/cx_version.py check .
python tools/validate_release.py .  # must run on main for release commits/tags
```

## Research Basis

The BDD rules follow Cucumber/Gherkin conventions: BDD is discovery, collaboration, and examples; Gherkin uses `Feature`, `Rule`, `Scenario`, `Given`, `When`, and `Then`; a feature file has one feature and scenarios should stay focused. See the [Cucumber introduction](https://cucumber.io/docs), [Gherkin reference](https://cucumber.io/docs/gherkin/reference/), and [Three Amigos guidance](https://cucumber.io/docs/bdd/who-does-what/).

The release rules follow [Semantic Versioning](https://semver.org/), [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and Git annotated tags. The research workflow uses academic-source discovery patterns from sources such as [Semantic Scholar](https://www.semanticscholar.org/product/api) and PRISMA-style screening discipline.

## Release Validation

```bash
python tools/cx_version.py check .
python tools/validate_release.py .
```
