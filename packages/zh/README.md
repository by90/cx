# cx 中文用例驱动工作流包

本目录是 cx 中文包源码。公共安装源是仓库根目录的 `SKILLS/zh`，本目录保留完整源码、模板、指南、agents 和发布验证工具。

不要把中文包和英文包同时安装到同一个目标项目。两套包的 skill 和 agent 名称保持一致，语言只影响面向人的说明、模板和示例。

## 核心约定

cx 是工作流包，不是组件库。它规定人类和人工智能如何先读取 `docs/cx/docs/` 专题文档和已登记通用能力，再用当前用例、设计、固定任务和临时变更文件推进工作。正式文档只保留最新状态，变更历史由 Git 保存。

代码、文档、教程、研究、设计或流程交付物完成后必须由 `$cx-review` 连续执行交付物质量审查和完成证据门禁；任一阶段不通过时任务仍未完成，当前变更文件不得删除。

所有 cx 文档只属于 `docs/cx`：

```text
docs/cx/00.项目说明.md
docs/cx/01.创建用户/00.用例.md
docs/cx/01.创建用户/00.设计.md
docs/cx/01.创建用户/tasks/01.编写用户实体.md
docs/cx/01.创建用户/changes/调整用户实体约束.md
```

每个任务的基本量具是类或类型组合。一个任务只处理一份任务文档和一个生产代码文件；需要第二个代码文件时先拆成下一个任务。默认完整面向对象、极简、复用优先，避免过长文件、过长变量名和重复实现。
新 story 建立时一次性确定 `tasks/NN.中文任务名.md` 任务集合。已有 story 的任务文件数量和身份保持不变。`changes/中文变更名.md` 只指导当前工作，先提交到 Git，完成审查后删除并再次提交。

用例粒度必须围绕用户目标：一个主成功场景文件夹只承载一个用户目标用例。主成功场景从触发写到目标达成，通常 3 到 9 个主步骤；每一步是参与者和系统之间的可观察交互。条件、替代和异常必须用 `1.1`、`2.1` 这类子编号挂到具体主步骤下，并写明后续是返回某一步、结束本用例，还是进入其它独立用例。不要把首页上的多个按钮、多个互斥选择或多个完整任务塞进一个主成功场景。复杂条件流程如果需要自己的参与者、步骤和完成标准，应拆成单独用例，并在项目说明中维护索引。

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
请使用 $cx-workflow 选择最小必要的 cx 技能。开始工作时先用 $cx-doc 读取 docs/cx/docs 中的专题文档，并搜索项目已经登记的通用包和真实调用点；再用 $cx-story 定位当前用例、设计和原任务。已有 story 的变化、实现改向或代码错误先用 $cx-changelog 建立临时变更文件并提交到 Git，然后修改原任务和实现。正式文档只写当前状态。默认不创建或修改单元测试；只有我明确要求测试先行开发、单元测试或失败测试时，才使用 $cx-tdd。除非我在当前请求中明确要求具体校验或异常处理，否则禁止自行校验后抛出异常，也禁止捕获、转换、包装、吞掉或兜底异常；底层异常必须原样抛出并中止程序。交付物完成后用 $cx-review 连续执行质量审查和完成证据门禁；通过后删除当前变更文件并提交删除动作。
```

Python / PyTorch：

```text
请使用 $cx-story。Python 使用 uv 管理的解释器和项目 uv 工作流。对状态、生命周期、不变量和领域对象协作使用完整面向对象设计；默认不写单元测试。只有我明确要求 Python / PyTorch 单元测试、TDD 或 tensor 测试时，才叠加 $cx-tdd 和 $cx-pytorch-tdd，并使用 unittest、确定性小数据，禁止默认使用 getattr/setattr 等动态反射。
```

Rust：

```text
请使用 $cx-story 和 $cx-rust-tdd。用 struct/enum/trait 表达领域状态，默认只实现当前任务绑定的一个 Rust 代码文件。默认不写单元测试；只有我明确要求 Rust 单元测试或 TDD 时，才先写失败的 #[test] 或集成测试，再运行 cargo test。无论是否测试，都运行 cargo fmt，可行时运行 clippy。
```

发布：

```text
请使用 $cx-version。工作必须在短生命周期本地分支完成，并且只在用户确认后合并到 main。不要 push 工作分支；远端只保留 main 和版本 tag。只有在 main 上才更新 VERSION、manifest、根 changelog、验证、创建带注释 vX.Y.Z tag，然后 push main 和发布 tag。
```

## Skill 对照表

| Skill | 用途 |
| --- | --- |
| `$cx-workflow` | 流程分流和 skill 选择 |
| `$cx-story` | 用例、主成功场景、条件子步骤、任务和变更 |
| `$cx-tdd` | 明确声明时的测试先行、最窄失败测试、最小实现和重构 |
| `$cx-changelog` | `changes/` 临时变更文件的登记、提交、执行和完成删除 |
| `$cx-doc` | `docs/cx/docs/` 专题文档、通用包说明和 `docs/cx/notes/` 研究笔记 |
| `$cx-version` | 项目内 `tools/semver.py`、SemVer、`VERSION`、`docs/VERSIONS.md` 和发布 tag |
| `$cx-research` | 模型选择、模型原理、近期论文和带来源综合分析 |
| `$cx-design` | 面向对象设计、职责拆分、领域对象、类命名、继承组合和数据访问边界 |
| `$cx-pytorch-tdd` | 明确声明时的 Python、PyTorch、Lightning 测试 |
| `$cx-pytorch-quick-hpo` | PyTorch 快速调参、字段贡献研究、特征组合和候选初筛 |
| `$cx-pytorch-full-hpo` | PyTorch 全量调参、完整训练、评估、回测和候选模型选择 |
| `$cx-timeseries-modeling` | 异构多变量时间序列建模和 PyTorch Forecasting 选型 |
| `$cx-rust-tdd` | Rust 类型设计、所有权设计、可选显式测试和 cargo fmt/clippy/test |
| `$cx-common-module` | 通用功能、可复用类和功能入口设计 |
| `$cx-review` | 交付物质量审查、完成证据门禁和剩余风险 |

## 验证

```bash
python -m unittest discover -v -s ./tests -p "*_test.py" -t .
python tools/validate_skill_pack.py .
python tools/validate_cx_pack.py .
python tools/validate_single_source.py
```
