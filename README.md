# cx Codex BDD/TDD Packages

This repository publishes two language packs for the same cx workflow:

- `SKILLS/en`: English skills.
- `SKILLS/zh`: Chinese skills.

Users do not need to clone this repository or install a separate `cx` command. Installation and updates are handled directly by `shskills`, which reads the repository `SKILLS/` directory from GitHub.

For Chinese documentation, see [README.zh-CN.md](README.zh-CN.md).

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

Run the same command again to update. `shskills` fetches the latest `SKILLS/en` from GitHub and cleans removed old `cx-*` skills.

For Chinese, change `--subpath en` to `--subpath zh`.

## Project Configuration

cx skills should be installed globally. Target projects do not need `.agents/skills`, `.codex/agents`, tools, templates, or scripts copied into them.

Project-specific guidance belongs in the target project's own `AGENTS.md`. To reuse this repository's project working agreement, copy from:

- English template: `packages/en/AGENTS.md`
- Chinese template: `packages/zh/AGENTS.md`

## Available Skills

```text
$cx-bdd-tdd
$cx-changelog
$cx-pytorch-tdd
$cx-ragged-tensor
$cx-progress-ui
$cx-rust-ui
$cx-common-module
$cx-evidence
```

## Release Validation

```bash
python tools/validate_release.py .
```
