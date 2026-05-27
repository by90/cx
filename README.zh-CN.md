# cx Codex BDD/TDD 工作流包

cx 是用于规范人类与 AI 协作研发的 Codex skill 包。它的核心目标是让 AI 辅助研发严格遵循长期可维护的 BDD/TDD 协作流程：先用 BDD 发现行为，再用 TDD 证明行为，记录变更历史，使用标准发布版本机制，并保留验证证据。

cx 不是组件库。Progress UI 组件、ragged tensor 工具、Rust UI 组件这类实现域，应该在各自项目或组件目录中维护 README、API 文档和测试，不应该作为 cx 核心 skills 发布。

当前包版本：`0.1.2`。cx 仍处于实验阶段，尚未经过验证成为稳定的 1.0 工作流。

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

本地 Codex skills 只能从仓库默认的 `main` 分支安装或更新。不要传 `--ref`，也不要从工作分支更新本机 skills。

安装中文 cx skills 到全局 Codex skills 目录：

```powershell
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:USERPROFILE\.codex\skills" --subpath zh --force --clean
```

如果设置了 `CODEX_HOME`，可以改成：

```powershell
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:CODEX_HOME\skills" --subpath zh --force --clean
```

英文版只需要把 `--subpath zh` 改成 `--subpath en`。

## 核心工作流

1. `$cx-workflow` 判断请求类型，先在对话中创建可见待办事项列表，并选择最小必要 skills。
2. `$cx-bdd` 在需要行为发现时创建或更新编号功能文件夹和 BDD 场景；普通、非编程任务不要自行创建 BDD。
3. 完成 `BDD.md`、`ENGINEERING_SPEC.md` 和 `CHANGELOG.md` 后必须停止，向用户汇报文档结果和下一步实现计划，等待明确确认。
4. 用户确认后，继续逐项更新待办事项；`$cx-tdd` 将 BDD 场景映射到失败测试，执行 red/green/refactor，并记录证据。
5. `$cx-pytorch-tdd`、`$cx-rust-tdd`、`$cx-common-module` 等专项 skills 补充语言和设计约束。
6. `$cx-changelog`、`$cx-version`、`$cx-evidence` 保证交付或发布前可审计；收尾前所有待办事项都必须完成、取消或明确阻塞。

## 分支与发布门禁

任何功能组都应该在短生命周期本地工作分支上开发。功能组完成并经过用户确认后，把该分支合并到 `main`，删除本地工作分支，并且只 push `main`。

pre-1.0 阶段新增并完成一个功能组后，只更新 minor，例如 `0.1.3` 到 `0.2.0`。既有功能组内的修改、bug 修复或调整只更新 patch，例如 `0.1.3` 到 `0.1.4`。创建发布前必须先和用户确认该版本已经完成。

用户只要求更新、递增或准备版本号时，默认只更新 patch；只有用户明确要求新增功能组、minor、major、稳定版或不兼容发布时，才更新前面的版本号。

发布顺序是强制的：

1. 完成本地功能组分支。
2. 用户确认版本完成后，将该分支合并到 `main` 并删除本地分支。
3. 只有在 `main` 上，才允许创建版本提交、创建带注释的 `vX.Y.Z` tag，然后 push `main` 和发布 tag。

禁止在工作分支上创建 release commit 或 tag。
远端仓库应该只保留 `main` 和版本 tag。不要 push 工作分支，除非用户在当前对话中明确覆盖这条 main-only 远端策略。

## 运行环境与 UI 检查

长时间构建、测试、安装或 UI 实机检查前，agent 应先查找并启动项目提供的当前平台防睡眠或会话保持机制，并在结束、阻塞或交接前恢复。macOS 桌面或 GUI 项目完成 UI 修改后，必须先按项目方式打包、安装或启动真实应用，再用 Computer Use 或项目指定方式完成实机观察，并把命令、结果和剩余风险记录为验证证据。

Python 命令优先使用项目 `uv` 工作流或 `uv` 安装管理的解释器，例如 `uv run python ...` 或 `uv run --python <version> ...`；系统自带 Python 只用于确认环境，不作为测试、构建或工具命令的默认运行时。

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

提示词应尽量说明目标功能文件夹、要使用的 cx skills、必须通过的命令，以及需要留下哪些证据。如果缺少验收标准、目标环境或验证要求，`$cx-workflow` 应先问最小必要澄清问题。对需要文档集的研发任务，文档完成后必须等待用户确认，确认后才进入测试和实现。

如果项目同时使用 Claude Code，请把 `AGENTS.md` 作为仓库规则的共同来源，让 `CLAUDE.md` 引用或指向它，不要维护两份会漂移的规则。

安装中文 cx 包时，所有 cx 生成或维护的文档必须使用简体中文。用户要求提交、交付、发 PR 或发布时，AGENTS 模板要求把当前工作区作为一个整体提交，不按“谁修改的”或“是否未跟踪”拆分。

所有项目都按多个功能组组织。功能文档文件夹必须使用三位序号、小写英文和下划线命名：

```text
docs/001_config_system/
docs/002_user_sessions/
docs/003_model_evaluation/
```

文件夹内的 BDD 文档必须使用同一个名字：

```text
docs/001_config_system/BDD.md
# BDD: 001_config_system

Feature: 001_config_system
```

英文项目使用同样文件夹命名约定：

```text
docs/001_configuration_system/
docs/001_configuration_system/BDD.md
# BDD: 001_configuration_system
Feature: 001_configuration_system
```

`docs/` 根目录只保留 `INDEX.md`、`README.md` 和 `VERSIONS.md` 这类索引与说明；具体研发文档放入编号功能组目录。非编程请求是否需要 BDD 不确定时，`$cx-workflow` 应先询问用户。

## 可用 Skills

| Skill | 用途 |
| --- | --- |
| `$cx-workflow` | 任务分流入口，判断是否需要 BDD、TDD、研究、发布版本、证据审查或人工澄清。 |
| `$cx-bdd` | BDD 发现、编号功能文件夹命名、业务规则、Gherkin 风格示例、验收标准、主成功/分支/异常场景。 |
| `$cx-tdd` | BDD 明确后的测试先行实现：red-green-refactor、最窄失败测试、Test Matrix、代码质量门槛和验证证据。 |
| `$cx-changelog` | `CHANGE-*` 条目、变更记录一致性，以及变更到同一功能文档集的映射。 |
| `$cx-version` | 使用目标项目内 `tools/semver.py`、SemVer、`VERSION`、`docs/VERSIONS.md`、带注释 `vX.Y.Z` Git tag 和 GitHub Release 管理发布版本。 |
| `$cx-research` | 模型选择、模型原理研究、近期 AI 论文扫描、学术/博客综合分析和带引用建议。 |
| `$cx-pytorch-tdd` | Python、PyTorch、Lightning、tensor 工具、ML 测试、确定性小测试数据，以及严格 Python OOP/TDD 质量规则。 |
| `$cx-rust-tdd` | Rust 实现和 TDD：struct/enum/trait、ownership、`Result` 错误、`cargo test`、`rustfmt`、`clippy` 和非 UI Rust 代码质量。 |
| `$cx-common-module` | 通用功能、可复用功能、可复用类、稳定 API、迁移计划和重复逻辑控制。 |
| `$cx-evidence` | 交付前审查 BDD/TDD 合规、测试输出、changelog/spec 一致性和缺失证据。 |

## 发布版本管理

cx 使用标准发布机制：

- `VERSION` 是唯一版本来源，只保存不带 `v` 的 SemVer 值。
- `packages/en/manifest.json` 和 `packages/zh/manifest.json` 必须与 `VERSION` 一致。
- 根目录 `CHANGELOG.md` 遵循 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)。
- 发布 tag 使用带注释 Git tag，名称为 `vX.Y.Z`。
- GitHub Release 使用对应 changelog 章节作为发布说明。

版本号使用 `MAJOR.MINOR.PATCH`：

- 新项目或未经验证的项目默认从 `0.0.1` 开始，除非用户明确说明项目已经达到 `1.0.0`。
- 主版本号 `0` 表示尚未正式发布；这个阶段接口和工作流契约变化是正常的。
- 当主版本号为 `0` 时，新增功能组只更新 minor，例如 `0.1.3` 到 `0.2.0`。
- 当主版本号为 `0` 时，既有功能组内修改、bug 修复或调整只更新 patch，例如 `0.1.3` 到 `0.1.4`。
- `1.0.0` 表示项目完成并被明确声明稳定后的第一版公开工作流/API 契约。
- `1.0.0` 之后，兼容性新增使用 `1.1.0` 这类 minor；破坏兼容性使用 `2.0.0` 这类 major。

对当前 cx 而言，`$cx-bdd-tdd` 拆成 `$cx-bdd` 和 `$cx-tdd` 仍属于 pre-1.0 实验线内的调整。本次分支/发布门禁功能组发布为 `0.1.0`；它不是 `1.0.0` 稳定声明，也不是 `2.0.0` 破坏性发布。

常用命令：

```bash
python tools/cx_version.py show .
python tools/cx_version.py check .
python tools/validate_release.py .  # release commit/tag 前必须在 main 上运行
```

目标项目从 `SKILLS/<language>/cx-version/scripts/semver.py` 复制到项目内 `tools/semver.py` 后，使用：

```bash
python tools/semver.py next feature-group --root .
python tools/semver.py next patch --root .
python tools/semver.py prepare <version> "<标题>" --root .
```

## 调研依据

BDD 规则遵循 Cucumber/Gherkin 约定：BDD 是 discovery、collaboration 和 examples；Gherkin 使用 `Feature`、`Rule`、`Scenario`、`Given`、`When`、`Then`；一个 feature 文档只包含一个 feature，场景应保持聚焦。参考 [Cucumber introduction](https://cucumber.io/docs)、[Gherkin reference](https://cucumber.io/docs/gherkin/reference/) 和 [Three Amigos guidance](https://cucumber.io/docs/bdd/who-does-what/)。

发布规则遵循 [Semantic Versioning](https://semver.org/)、[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 和 Git 带注释 tag。研究工作流参考 [Semantic Scholar](https://www.semanticscholar.org/product/api) 等学术发现工具和 PRISMA 风格筛选纪律。

## 发布前验证

```bash
python tools/cx_version.py check .
python tools/validate_release.py .
```
