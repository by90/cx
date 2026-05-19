# cx 中文 BDD/TDD 工作流包

本目录是 cx 中文包源码。cx 是用于人类与 AI 协作研发的 Codex workflow pack，公共安装源是仓库根目录的 `SKILLS/zh`；本目录保留完整源码、模板、指南、agents 和发布验证工具。

不要把中英文包同时安装到同一个目标项目。两套包的 skill 和 agent 名称故意保持一致。

## 核心契约

cx 是工作流包，不是组件库。它规范人类和 AI 如何发现行为、先写测试、实现代码、研究技术选择、管理发布版本和审查证据。

功能文件夹按业务能力编号：

```text
docs/1.配置系统/
docs/1.配置系统/BDD.md
docs/1.配置系统/ENGINEERING_SPEC.md
docs/1.配置系统/CHANGELOG.md
```

`BDD.md` 的标题和 `Feature:` 名称必须与文件夹名一致。

## 快速开始

```powershell
uv tool install shskills
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:USERPROFILE\.codex\skills" --subpath zh --ref main --force --clean
```

如果设置了 `CODEX_HOME`，目标目录改为 `$env:CODEX_HOME\skills`。

## 提示词模式

高质量 coding-agent 提示词应先给出明确契约：

```text
目标：
上下文：
约束：
必须遵循的流程：
验证方式：
交付物：
```

优先说明目标功能文件夹、要使用的 cx skills、必须通过的命令，以及要记录的证据。使用 Claude Code 的项目，应把 `AGENTS.md` 作为共同规则来源，让 `CLAUDE.md` 引用或指向它。

功能或缺陷：

```text
请使用 $cx-workflow，选择最小必要 cx skills。先用 $cx-bdd 创建或更新编号功能文件夹和 BDD.md，再用 $cx-tdd 在实现前写失败测试。
```

Python / PyTorch / Lightning：

```text
请使用 $cx-bdd、$cx-tdd 和 $cx-pytorch-tdd。对状态和不变量使用明确 OOP 设计，先写 unittest，使用确定性小数据，禁止默认使用 getattr/setattr 等动态反射。
```

Rust：

```text
请使用 $cx-bdd、$cx-tdd 和 $cx-rust-tdd。用 struct/enum/trait 表达状态，先写失败的 #[test] 或集成测试，再运行 cargo test、cargo fmt，可行时运行 clippy。
```

研究：

```text
请使用 $cx-research。先定义研究问题、搜索窗口、纳入/排除标准、学术来源、官方来源和解读来源。每个非显然主张都要引用来源。
```

发布：

```text
请使用 $cx-version。新项目或未经验证的项目从 0.0.1 开始，主版本号保持 0，直到项目被明确声明稳定。判断 SemVer 升级，更新 VERSION 和 manifests，更新 CHANGELOG.md，验证后创建带注释 vX.Y.Z tag。
```

## Skill 对照表

| Skill | 用途 |
| --- | --- |
| `$cx-workflow` | 流程分流和 skill 选择 |
| `$cx-bdd` | BDD 发现、编号功能文件夹、业务规则、场景 |
| `$cx-tdd` | Red-green-refactor、测试矩阵、代码质量门槛 |
| `$cx-changelog` | `CHANGE-*` 条目和变更记录一致性 |
| `$cx-version` | SemVer、`VERSION`、changelog、发布 tag |
| `$cx-research` | 模型选择、模型原理、近期论文、带来源综合分析 |
| `$cx-pytorch-tdd` | Python/PyTorch/Lightning 实现和测试 |
| `$cx-rust-tdd` | Rust 实现、所有权设计、cargo test/fmt/clippy |
| `$cx-common-module` | 通用模块抽取和 API 设计 |
| `$cx-evidence` | 交付前证据审查 |

## 验证

```bash
python -m unittest discover -s tests
python tools/validate_skill_pack.py .
python tools/validate_cx_pack.py .
python tools/validate_single_source.py examples/python_ml_project
```
