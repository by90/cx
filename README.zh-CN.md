# cx Codex BDD/TDD Packages

本仓库发布同一套 cx 工作流的两个语言包：

- `SKILLS/zh`：中文 skills。
- `SKILLS/en`：英文 skills。

用户不需要 clone 本仓库，也不需要先安装一个 `cx` 命令。安装和更新直接使用 `shskills` 从 GitHub 读取 `SKILLS/` 目录。

英文说明见 [README.md](README.md)。

## 准备 shskills

临时使用：

```powershell
uvx shskills --help
```

长期使用：

```powershell
uv tool install shskills
```

## 安装或更新

安装中文 cx skills 到全局 Codex skills 目录：

```powershell
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:USERPROFILE\.codex\skills" --subpath zh --ref main --force --clean
```

如果设置了 `CODEX_HOME`，可以改成：

```powershell
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:CODEX_HOME\skills" --subpath zh --ref main --force --clean
```

更新时重复同一条命令即可。`shskills` 会从 GitHub 拉取最新 `SKILLS/zh` 并清理已经移除的旧 `cx-*` skills。

英文版只需要把 `--subpath zh` 改成 `--subpath en`。

## 项目配置

cx skills 建议全局安装。目标项目不需要复制 `.agents/skills`、`.codex/agents`、tools、templates 或脚本。

项目特殊规则只放在项目自己的 `AGENTS.md`。如果需要引入本仓库的项目工作约定，可以参考：

- 中文模板：`packages/zh/AGENTS.md`
- 英文模板：`packages/en/AGENTS.md`

## 可用 skills

```text
$cx-workflow
$cx-bdd-tdd
$cx-changelog
$cx-pytorch-tdd
$cx-ragged-tensor
$cx-progress-ui
$cx-rust-ui
$cx-common-module
$cx-evidence
```

## 发布前验证

```bash
python tools/validate_release.py .
```
