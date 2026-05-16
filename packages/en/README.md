# cx Codex BDD/TDD Pack

This is the English cx package for AI-assisted BDD/TDD development with Codex App, Codex CLI, and ChatGPT-assisted planning. It keeps development anchored to one engineering specification, one changelog, executable tests, and reusable skills.

Use the Chinese package instead when your team wants Chinese instructions in `AGENTS.md`, `SKILL.md`, templates, and guides. Do not install both language packs into the same target project, because the skill and agent names are intentionally identical.

## What this repository provides

```text
AGENTS.md
.agents/skills/cx-*/SKILL.md
.codex/agents/cx-*.toml
.codex/config.toml
templates/ENGINEERING_SPEC.md
templates/CHANGELOG.md
tools/validate_single_source.py
tools/validate_skill_pack.py
tools/validate_cx_pack.py
tools/new_change.py
```

The repository root `SKILLS/en` directory is the shskills installation source for users. This package directory keeps the complete English package source, templates, guides, and validation tools for development and release checks.

## Quick Start

Prepare `shskills`:

```powershell
uv tool install shskills
```

Install or update the English skills globally:

```powershell
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:USERPROFILE\.codex\skills" --subpath en --ref main --force --clean
```

If `CODEX_HOME` is set:

```powershell
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:CODEX_HOME\skills" --subpath en --ref main --force --clean
```

Run the same command again to update. Target projects do not need `.agents/skills`, `.codex/agents`, tools, templates, or scripts copied from this package; project-specific guidance belongs in the target project's own `AGENTS.md`.

## How to interact with ChatGPT and Codex

Use stable cx names in your prompts. The names stay the same in both language packs.

### Feature or bugfix request

```text
Use $cx-bdd-tdd. Update docs/ENGINEERING_SPEC.md and docs/CHANGELOG.md first. Derive BDD scenarios and failing tests before implementation. Do not create separate spec/plan/task documents.
```

### Python / PyTorch / Lightning request

```text
Use $cx-bdd-tdd and $cx-pytorch-tdd. For tensor code, also check whether $cx-ragged-tensor applies. Use unittest, Black-compatible formatting, tiny CPU-first tests, and verify current official APIs when version-sensitive.
```

### Rust / GPUI / gpui-component request

```text
Use $cx-bdd-tdd and $cx-rust-ui. Keep pure state and reducers separate from rendering. Add tests first, then run cargo fmt, cargo test, and cargo clippy when practical.
```

### Reusable component request

```text
Use $cx-common-module. Check the Common Module Registry in docs/ENGINEERING_SPEC.md. Design the API, add tests first, migrate duplicated code, and record the module in the registry.
```

### Subagent workflow

Codex does not spawn custom subagents unless you explicitly ask. Use a prompt like:

```text
Spawn cx-spec to update the single engineering spec, cx-tdd to design failing tests, and cx-review to check evidence. Wait for all results, then implement the smallest change.
```

### ChatGPT outside Codex

ChatGPT will not automatically discover local Codex skills unless the relevant files are attached or pasted. For planning conversations, attach or paste `AGENTS.md`, the relevant `SKILL.md`, `docs/ENGINEERING_SPEC.md`, and `docs/CHANGELOG.md`, then ask ChatGPT to follow the cx workflow by name.

## Skill map

| Skill | Use for |
| --- | --- |
| `$cx-bdd-tdd` | Main BDD/TDD single-source workflow |
| `$cx-changelog` | `CHANGE-*` entries and changelog consistency |
| `$cx-pytorch-tdd` | Python, PyTorch, Lightning, tensor, ML tests |
| `$cx-ragged-tensor` | Variable-length tensors, masks, padding, collation |
| `$cx-progress-ui` | Multi-task progress UI, ETA, cancellation, adapters |
| `$cx-rust-ui` | Rust, GPUI, gpui-component desktop UI work |
| `$cx-common-module` | Reusable module extraction and API design |
| `$cx-evidence` | Final evidence review before delivery |

## Agent map

| Agent | Use for |
| --- | --- |
| `cx-spec` | Maintaining `ENGINEERING_SPEC.md` and `CHANGELOG.md` |
| `cx-bdd` | Expanding behavior into BDD scenarios |
| `cx-tdd` | Designing failing tests and test matrix entries |
| `cx-python-ml` | Python/PyTorch/Lightning implementation |
| `cx-rust-ui` | Rust/GPUI implementation |
| `cx-common` | Common module API and extraction |
| `cx-review` | Read-only evidence and compliance review |

## Multilingual publishing strategy

Best deployment method: publish both language packages in one GitHub repository, but install only one language package into any target codebase.

Recommended publishing layout:

```text
README.md
README.zh-CN.md
packages/en/...
packages/zh/...
tools/validate_release.py
```

Keep skill and agent names identical across languages: `cx-bdd-tdd` means the same workflow in English and Chinese. Localize descriptions, instructions, templates, and guides. This lets prompts, tutorials, and automation stay stable while humans read the language they prefer.

## Validation

Run inside this package:

```bash
python -m unittest discover -s tests
python tools/validate_skill_pack.py .
python tools/validate_cx_pack.py .
python tools/validate_single_source.py examples/python_ml_project
```

Target repositories do not need package validation tools copied into them.

## Important rule

`docs/ENGINEERING_SPEC.md` is the only long-lived engineering specification. `docs/CHANGELOG.md` is only a historical index. Requirements, BDD scenarios, architecture decisions, task queues, test matrix entries, and verification evidence belong in the engineering spec, not in scattered feature documents.
