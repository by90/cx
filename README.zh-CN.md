# cx Codex BDD/TDD 工作流包

cx 是用于规范人类与 AI 协作研发的 Codex skill 包。它的核心目标是让 AI 辅助研发严格遵循长期可维护的 BDD/TDD 协作流程：先用 BDD 发现行为，再用 TDD 证明行为，记录变更历史，使用标准发布版本机制，并保留验证证据。

cx 不是组件库。Progress UI 组件、ragged tensor 工具、Rust UI 组件这类实现域，应该在各自项目或组件目录中维护 README、API 文档和测试，不应该作为 cx 核心 skills 发布。

当前包版本：`2.0.0`。`2.x` 已将旧的合并式 BDD/TDD 概念拆成独立的 `$cx-bdd` 和 `$cx-tdd`。

英文说明见 [README.md](README.md)。

## cx 安装什么

本仓库发布同一套工作流的两个语言包：

- `SKILLS/zh`：中文 skills。
- `SKILLS/en`：英文 skills。

用户不需要 clone 本仓库，也不需要先安装一个 `cx` 命令。安装和更新直接使用 `shskills` 从 GitHub 读取 `SKILLS/` 目录。

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

英文版只需要把 `--subpath zh` 改成 `--subpath en`。

## 核心工作流

1. `$cx-workflow` 判断请求类型，并选择最小必要 skills。
2. `$cx-bdd` 创建或更新编号功能文件夹和 BDD 场景。
3. `$cx-tdd` 将 BDD 场景映射到失败测试，执行 red/green/refactor，并记录证据。
4. `$cx-pytorch-tdd`、`$cx-rust-tdd`、`$cx-common-module` 等专项 skills 补充语言和设计约束。
5. `$cx-changelog`、`$cx-version`、`$cx-evidence` 保证交付或发布前可审计。

## 提示词契约

cx 最适合配合小而明确的任务契约，而不是含混的一句话需求。无论使用 Codex、Claude Code 还是其他 coding agent，都建议按这个结构写：

```text
目标：
上下文：
约束：
必须遵循的流程：
验证方式：
交付物：
```

提示词应尽量说明目标功能文件夹、要使用的 cx skills、必须通过的命令，以及需要留下哪些证据。如果缺少验收标准、目标环境或验证要求，`$cx-workflow` 应先问最小必要澄清问题，再进入实现。

如果项目同时使用 Claude Code，请把 `AGENTS.md` 作为仓库规则的共同来源，让 `CLAUDE.md` 引用或指向它，不要维护两份会漂移的规则。

功能文档文件夹必须按业务能力编号命名：

```text
docs/1.配置系统/
docs/2.用户会话/
docs/3.模型评估/
```

文件夹内的 BDD 文档必须使用同一个名字：

```text
docs/1.配置系统/BDD.md
# BDD: 1.配置系统

Feature: 1.配置系统
```

英文项目使用同样约定：

```text
docs/1.Configuration System/
docs/1.Configuration System/BDD.md
# BDD: 1.Configuration System
Feature: 1.Configuration System
```

## 可用 Skills

| Skill | 用途 |
| --- | --- |
| `$cx-workflow` | 任务分流入口，判断是否需要 BDD、TDD、研究、发布版本、证据审查或人工澄清。 |
| `$cx-bdd` | BDD 发现、编号功能文件夹命名、业务规则、Gherkin 风格示例、验收标准、主成功/分支/异常场景。 |
| `$cx-tdd` | BDD 明确后的测试先行实现：red-green-refactor、最窄失败测试、Test Matrix、代码质量门槛和验证证据。 |
| `$cx-changelog` | `CHANGE-*` 条目、变更记录一致性，以及变更到同一功能文档集的映射。 |
| `$cx-version` | 使用 SemVer、根 `VERSION`、Keep a Changelog、带注释 `vX.Y.Z` Git tag 和 GitHub Release 管理发布版本。 |
| `$cx-research` | 模型选择、模型原理研究、近期 AI 论文扫描、学术/博客综合分析和带引用建议。 |
| `$cx-pytorch-tdd` | Python、PyTorch、Lightning、tensor 工具、ML 测试、确定性小测试数据，以及严格 Python OOP/TDD 质量规则。 |
| `$cx-rust-tdd` | Rust 实现和 TDD：struct/enum/trait、ownership、`Result` 错误、`cargo test`、`rustfmt`、`clippy` 和非 UI Rust 代码质量。 |
| `$cx-common-module` | 复用组件抽取、通用模块设计、稳定 API、迁移计划和重复逻辑控制。 |
| `$cx-evidence` | 交付前审查 BDD/TDD 合规、测试输出、changelog/spec 一致性和缺失证据。 |

## 发布版本管理

cx 使用标准发布机制：

- `VERSION` 是唯一版本来源，只保存不带 `v` 的 SemVer 值。
- `packages/en/manifest.json` 和 `packages/zh/manifest.json` 必须与 `VERSION` 一致。
- 根目录 `CHANGELOG.md` 遵循 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)。
- 发布 tag 使用带注释 Git tag，名称为 `vX.Y.Z`。
- GitHub Release 使用对应 changelog 章节作为发布说明。

版本号使用 `MAJOR.MINOR.PATCH`：

- `1.0.0` 表示第一版稳定公开工作流/API 契约。
- `1.1.0` 表示新增向后兼容的公开接口或工作流能力。
- `1.0.1` 表示 bugfix、文案、示例、翻译或验证脚本修复，且不改变公开契约。
- `2.0.0` 表示不兼容的公开契约变化，例如删除或重命名公开 skill、agent、安装路径、CLI 命令、文档集规则或提示词/工作流 API。

所以，“接口发生变化”只有在向后兼容时才对应 `1.1.0`；破坏兼容性的接口变化必须升 major。

常用命令：

```bash
python tools/cx_version.py show .
python tools/cx_version.py check .
python tools/validate_release.py .
```

## 调研依据

BDD 规则遵循 Cucumber/Gherkin 约定：BDD 是 discovery、collaboration 和 examples；Gherkin 使用 `Feature`、`Rule`、`Scenario`、`Given`、`When`、`Then`；一个 feature 文档只包含一个 feature，场景应保持聚焦。参考 [Cucumber introduction](https://cucumber.io/docs)、[Gherkin reference](https://cucumber.io/docs/gherkin/reference/) 和 [Three Amigos guidance](https://cucumber.io/docs/bdd/who-does-what/)。

发布规则遵循 [Semantic Versioning](https://semver.org/)、[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 和 Git 带注释 tag。研究工作流参考 [Semantic Scholar](https://www.semanticscholar.org/product/api) 等学术发现工具和 PRISMA 风格筛选纪律。

## 发布前验证

```bash
python tools/cx_version.py check .
python tools/validate_release.py .
```
