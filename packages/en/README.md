# cx English BDD/TDD Workflow Pack

This package contains the English source for cx, a Codex workflow pack for human-AI BDD/TDD collaboration. The installable public source is `SKILLS/en`; this package directory keeps the full source, templates, guides, agents, and validation tools used to prepare releases.

Do not install both language packs into the same target project. English and Chinese packages intentionally share the same skill and agent names.

## Core Contract

cx is a workflow package, not a component library. It standardizes how humans and AI agents discover behavior, write documents first, wait for confirmation, then write tests and implementation code, while managing research, release versions, and evidence review.

Every project is organized as multiple feature groups. Feature folders are ordered by business capability and use a three-digit prefix, lowercase words, and underscores:

```text
docs/001_configuration_system/
docs/001_configuration_system/BDD.md
docs/001_configuration_system/ENGINEERING_SPEC.md
docs/001_configuration_system/CHANGELOG.md
docs/001_configuration_system/GUIDE.md
```

The BDD document heading and `Feature:` name must match the folder name. Do not create BDD automatically for ordinary non-programming tasks; ask the user first when behavior discovery is unclear.

## Quick Start

Local Codex skills must be installed or updated only from the repository's default `main` branch; do not pass `--ref` in the install command.

Prefer the installer script from the repository root. It updates skills from remote `main` and automatically overwrites the global `AGENTS.md`:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install_cx_en.ps1
```

`shskills install` currently installs skills only; it does not overwrite `$env:USERPROFILE\.codex\AGENTS.md` or `$env:CODEX_HOME\AGENTS.md`. If you run the raw command, sync this package's `AGENTS.md` separately.

```powershell
uv tool install shskills
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:USERPROFILE\.codex\skills" --subpath en --force --clean
```

If `CODEX_HOME` is set, use `$env:CODEX_HOME\skills` as the destination.

## Prompt Patterns

Best coding-agent prompts give the agent an explicit contract:

```text
Goal:
Context:
Constraints:
Required workflow:
Verification:
Deliverables:
```

Prefer naming the target feature folder, the cx skills to use, commands that must pass, and the evidence that should be recorded. For Claude Code projects, keep `AGENTS.md` as the shared rule source and have `CLAUDE.md` import or reference it. When the Chinese pack is installed, all cx documents must be Simplified Chinese.

Feature or bugfix:

```text
Use $cx-workflow. Select the smallest required cx skills. Start with $cx-bdd, create or update the ordered feature folder in docs/001_feature_name form, BDD.md, ENGINEERING_SPEC.md, and CHANGELOG.md; after the documents are complete, stop and wait for my confirmation. After confirmation, use $cx-tdd to write the failing test and implement.
```

Git commit:

```text
When committing, follow AGENTS.md: treat the current working tree as one change set, stage tracked and untracked files, create one commit, and do not analyze who changed which files.
```

Python / PyTorch / Lightning:

```text
Use $cx-bdd, $cx-tdd, and $cx-pytorch-tdd. Use a uv-installed and uv-managed Python interpreter through the project uv workflow. Use explicit OOP design for state and invariants, unittest-first tests, deterministic tiny data, and avoid dynamic reflection such as getattr/setattr unless no static API works.
```

Rust:

```text
Use $cx-bdd, $cx-tdd, and $cx-rust-tdd. Model state with structs/enums/traits, write the failing #[test] or integration test first, then run cargo test, cargo fmt, and clippy when practical.
```

Research:

```text
Use $cx-research. Define the research question, search window, inclusion/exclusion criteria, academic sources, official sources, and interpretation sources. Cite every non-obvious claim.
```

Release:

```text
Use $cx-version. Feature-group work must happen on its own short-lived local branch and merge to main only after user confirmation. Do not push work branches; the remote keeps only main and version tags. Only on main update VERSION/manifests/CHANGELOG, validate, create the annotated vX.Y.Z tag, then push main and the release tag.

Target projects must use their project-local `tools/semver.py`; if the project does not have the tool yet, copy it from `$cx-version`'s `scripts/semver.py`. When the user only asks to bump the version, default to patch; bump earlier segments only for an explicit new feature group, minor, major, stable, or incompatible release. During `0.x.x`, use `python tools/semver.py next feature-group --root .` to compute the next minor for a new feature group; use `python tools/semver.py next patch --root .` to compute the next patch for changes, bug fixes, or adjustments inside an existing feature group. When preparing a release, use `python tools/semver.py prepare <version> "<title>" --root .` to update `VERSION`, optional `pyproject.toml`, and `docs/VERSIONS.md`.
```

## Skill Map

| Skill | Use for |
| --- | --- |
| `$cx-workflow` | Workflow routing and skill selection |
| `$cx-bdd` | BDD discovery, ordered feature folders, business rules, scenarios |
| `$cx-tdd` | Red-green-refactor, test matrices, code quality gates |
| `$cx-changelog` | `CHANGE-*` entries and changelog consistency |
| `$cx-version` | Project-local `tools/semver.py`, SemVer, `VERSION`, `docs/VERSIONS.md`, release tags |
| `$cx-research` | Model choice, model mechanisms, recent papers, sourced synthesis |
| `$cx-pytorch-tdd` | Python/PyTorch/Lightning implementation and tests |
| `$cx-pytorch-quick-hpo` | PyTorch quick tuning, field-contribution research, feature sets, window length, labels, training hyperparameters, and model-capacity screening |
| `$cx-pytorch-full-hpo` | PyTorch full-data tuning, complete-data training, test-set evaluation, backtesting, top-3 candidate comparison, and release-candidate model selection |
| `$cx-timeseries-modeling` | Heterogeneous multivariate time-series modeling, field semantics, covariates, leakage checks, and PyTorch Forecasting selection |
| `$cx-rust-tdd` | Rust implementation, ownership-aware design, cargo test/fmt/clippy |
| `$cx-common-module` | Generic capabilities, reusable features/classes, and API design |
| `$cx-evidence` | Final evidence review |

## Validation

```bash
python -m unittest discover -s tests
python tools/validate_skill_pack.py .
python tools/validate_cx_pack.py .
python tools/validate_single_source.py examples/python_ml_project
```
