# cx Codex BDD/TDD Pack

这是 cx 的中文包，用于在 Codex App、Codex CLI 和 ChatGPT 辅助规划中执行 BDD/TDD 工作流。目标是把研发固定在 docs 文档集、可执行测试和可复用 skills 上。

如果团队希望 `AGENTS.md`、`SKILL.md`、模板和指南使用英文，请安装英文包。不要把中英文两个包同时安装到同一个目标项目，因为两套包的 skill 和 agent 名称故意保持完全一致。

## 本仓库提供什么

```text
AGENTS.md
.agents/skills/cx-*/SKILL.md
.codex/agents/cx-*.toml
.codex/config.toml
templates/ENGINEERING_SPEC.md
templates/CHANGELOG.md
templates/DOCS_INDEX.md
tools/validate_single_source.py
tools/validate_skill_pack.py
tools/validate_cx_pack.py
tools/new_change.py
```

仓库根目录的 `SKILLS/zh` 是面向用户发布的 shskills 安装源。本目录保留完整中文包源码、模板、指南和验证工具，用于开发与发布校验。

## 快速开始

先准备 `shskills`：

```powershell
uv tool install shskills
```

安装或更新中文 skills 到全局：

```powershell
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:USERPROFILE\.codex\skills" --subpath zh --ref main --force --clean
```

如果使用 `CODEX_HOME`：

```powershell
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:CODEX_HOME\skills" --subpath zh --ref main --force --clean
```

更新时重复同一条命令。目标项目不需要复制本包的 `.agents/skills`、`.codex/agents`、tools、templates 或脚本；项目特殊规则写在项目自己的 `AGENTS.md`。

## 如何与 ChatGPT 和 Codex 互动

提示词中使用稳定的 cx 名称。中英文包的名称完全一致。

### 功能或缺陷需求

```text
请使用 $cx-workflow。判断需要哪些 cx skills，选择或创建目标 docs 文档集，更新对应的 ENGINEERING_SPEC.md 和 CHANGELOG.md，推导主成功场景、分支场景、异常场景和失败测试，最后实现。不要创建单独的 spec/plan/task 文档。
```

### Python / PyTorch / Lightning 需求

```text
请使用 $cx-bdd-tdd 和 $cx-pytorch-tdd。涉及 tensor 时也判断是否需要 $cx-ragged-tensor。使用 unittest，遵循 Black 默认格式，测试保持 CPU 优先和小规模，并在 API 或版本敏感时核对官方最新文档。
```

### Rust / GPUI / gpui-component 需求

```text
请使用 $cx-bdd-tdd 和 $cx-rust-ui。将纯状态和 reducer 与渲染代码分离。先写测试，再运行 cargo fmt、cargo test，可行时运行 cargo clippy。
```

### 通用组件封装需求

```text
请使用 $cx-common-module。先搜索当前项目、相关 skills、历史项目和目标文档集中的 Reusable Component Registry，设计 API，先写测试，迁移重复代码，并把组件登记到注册表。
```

### Subagent 工作流

Codex 不会自动启动自定义 subagent，必须明确要求。可以这样提示：

```text
请启动 cx-spec 更新目标 docs 文档集，启动 cx-tdd 设计失败测试，启动 cx-review 做证据审查。等待所有结果后，再实现最小改动。
```

### 在 Codex 外单独使用 ChatGPT

ChatGPT 不会自动读取本地 Codex skills，除非你上传或粘贴相关文件。做规划讨论时，上传或粘贴 `AGENTS.md`、相关 `SKILL.md`、`docs/INDEX.md` 以及目标文档集的 `ENGINEERING_SPEC.md` 和 `CHANGELOG.md`，然后要求 ChatGPT 按指定 cx 工作流执行。

## Skill 对照表

| Skill | 用途 |
| --- | --- |
| `$cx-workflow` | 流程处理、任务分流和 cx skills 编排入口 |
| `$cx-bdd-tdd` | BDD/TDD 文档集主流程 |
| `$cx-changelog` | `CHANGE-*` 条目和变更记录一致性 |
| `$cx-pytorch-tdd` | Python、PyTorch、Lightning、tensor、ML 测试 |
| `$cx-ragged-tensor` | 变长 tensor、mask、padding、collation |
| `$cx-progress-ui` | 多任务进度 UI、ETA、取消、适配器 |
| `$cx-rust-ui` | Rust、GPUI、gpui-component 桌面 UI |
| `$cx-common-module` | 复用组件、通用模块抽取和公共 API 设计 |
| `$cx-evidence` | 交付前证据审查 |

## Agent 对照表

| Agent | 用途 |
| --- | --- |
| `cx-spec` | 维护目标文档集的 `ENGINEERING_SPEC.md` 和 `CHANGELOG.md` |
| `cx-bdd` | 将行为扩展为 BDD 场景 |
| `cx-tdd` | 设计失败测试和测试矩阵 |
| `cx-python-ml` | Python/PyTorch/Lightning 实现 |
| `cx-rust-ui` | Rust/GPUI 实现 |
| `cx-common` | 复用组件 API 和抽取 |
| `cx-review` | 只读证据与合规审查 |

## 多语言发布策略

更好的方式是：在一个 GitHub 仓库中同时发布中英文包，但任何目标代码仓库只安装其中一种语言包。

推荐发布结构：

```text
README.md
README.zh-CN.md
packages/en/...
packages/zh/...
tools/validate_release.py
```

中英文包中的 skill 和 agent 名称保持完全一致：`cx-bdd-tdd` 在中文和英文中都代表同一套工作流。只本地化 description、instructions、templates 和 guides。这样提示词、教程和自动化脚本都能保持稳定，同时让团队成员阅读自己偏好的语言。

## 验证

在本包根目录运行：

```bash
python -m unittest discover -s tests
python tools/validate_skill_pack.py .
python tools/validate_cx_pack.py .
python tools/validate_single_source.py examples/python_ml_project
```

目标仓库不需要复制本包的验证工具。

## 关键规则

单功能项目可以使用 `docs/ENGINEERING_SPEC.md` 和 `docs/CHANGELOG.md`。多功能组项目应使用 `docs/INDEX.md` 做根索引，并将具体功能文档放入 `docs/<feature-group>/ENGINEERING_SPEC.md` 和同目录 `CHANGELOG.md`。需求、主成功场景、分支场景、异常场景、架构决策、任务队列、测试矩阵和验证证据都应该进入目标文档集，而不是散落在一堆 feature 文档里。
