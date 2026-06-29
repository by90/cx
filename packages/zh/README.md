# cx 中文用例驱动 TDD 工作流包

本目录是 cx 中文包源码。公共安装源是仓库根目录的 `SKILLS/zh`，本目录保留完整源码、模板、指南、agents 和发布验证工具。

不要把中文包和英文包同时安装到同一个目标项目。两套包的 skill 和 agent 名称保持一致，语言只影响面向人的说明、模板和示例。

## 核心约定

cx 是工作流包，不是组件库。它规定人类和 AI 如何用 `docs/cx` 保存用例、设计、任务、变更和验证证据。开工前先选择执行模式；用户未明确选择逐任务确认时，AI 默认直接完成文档、严格 TDD、实现和验证。

所有 cx 文档只属于 `docs/cx`：

```text
docs/cx/00.项目说明.md
docs/cx/01.创建用户/00.用例.md
docs/cx/01.创建用户/00. 设计.md
docs/cx/01.创建用户/tasks/01.编写用户实体/00.任务.md
docs/cx/01.创建用户/changes/20260629T120000-任务01-编写用户实体.md
```

每个任务的基本量具是类或类型组合。一个任务只处理一份任务文档、一个代码文件，以及必要时一个一一对应的单元测试文件。

用例粒度必须围绕用户目标：一个主成功场景文件夹只承载一个用户目标用例。主成功场景从触发写到目标达成，通常 3 到 9 步；每一步是参与者和系统之间的可观察交互。不要把首页上的多个按钮、多个互斥选择或多个完整任务塞进一个主成功场景。复杂分支如果需要自己的参与者、步骤和完成标准，应拆成单独用例，并在项目说明中维护索引。

## 快速开始

本地 Codex skills 只能从仓库默认的 `main` 分支安装或更新；安装命令不要传 `--ref`。

推荐使用仓库根目录的安装脚本，它会从远端 `main` 更新 skills，并自动覆盖全局 `AGENTS.md`：

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install_cx_zh.ps1
```

只运行原始命令时，需要额外同步本包的 `AGENTS.md`：

```powershell
uv tool install shskills
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:USERPROFILE\.codex\skills" --subpath zh --force --clean
```

## 提示词模式

功能或缺陷：

```text
请使用 $cx-workflow，选择最小必要 cx skills。开工前先询问我是要直接做完文档、测试、实现和验证，还是每完成一个任务后征求同意；如果我没有选择逐任务确认，默认直接做完。先用 $cx-story 在 docs/cx 下创建或更新用例、设计、任务和变更文档，再用 $cx-tdd 写失败测试并实现。
```

Python / PyTorch：

```text
请使用 $cx-story、$cx-tdd 和 $cx-pytorch-tdd。Python 使用 uv 管理的解释器和项目 uv 工作流。对状态、生命周期、不变量和领域对象协作使用严格面向对象设计，先写 unittest，使用确定性小数据，禁止默认使用 getattr/setattr 等动态反射。
```

Rust：

```text
请使用 $cx-story、$cx-tdd 和 $cx-rust-tdd。用 struct/enum/trait 表达领域状态，先写失败的 #[test] 或集成测试，再运行 cargo test、cargo fmt，可行时运行 clippy。
```

发布：

```text
请使用 $cx-version。工作必须在短生命周期本地分支完成，并且只在用户确认后合并到 main。不要 push 工作分支；远端只保留 main 和版本 tag。只有在 main 上才更新 VERSION、manifest、根 changelog、验证、创建带注释 vX.Y.Z tag，然后 push main 和发布 tag。
```

## Skill 对照表

| Skill | 用途 |
| --- | --- |
| `$cx-workflow` | 流程分流和 skill 选择 |
| `$cx-story` | 用例、主成功场景、分支场景、任务和变更 |
| `$cx-tdd` | 严格测试先行、最窄失败测试、最小实现和重构 |
| `$cx-changelog` | `changes/` 变更文档和发布说明一致性 |
| `$cx-version` | 项目内 `tools/semver.py`、SemVer、`VERSION`、`docs/VERSIONS.md` 和发布 tag |
| `$cx-research` | 模型选择、模型原理、近期论文和带来源综合分析 |
| `$cx-pytorch-tdd` | Python、PyTorch、Lightning 实现和测试 |
| `$cx-pytorch-quick-hpo` | PyTorch 快速调参、字段贡献研究、特征组合和候选初筛 |
| `$cx-pytorch-full-hpo` | PyTorch 全量调参、完整训练、评估、回测和候选模型选择 |
| `$cx-timeseries-modeling` | 异构多变量时间序列建模和 PyTorch Forecasting 选型 |
| `$cx-rust-tdd` | Rust 类型设计、所有权设计和 cargo test/fmt/clippy |
| `$cx-common-module` | 通用功能、可复用类和公共入口设计 |
| `$cx-evidence` | 交付前证据审查 |

## 验证

```bash
python -m unittest discover -s tests
python tools/validate_skill_pack.py .
python tools/validate_cx_pack.py .
python tools/validate_single_source.py
```
