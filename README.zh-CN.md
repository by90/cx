# cx Codex 用例驱动工作流包

cx 是用于规范人类与人工智能协作研发的 Codex 技能包。它要求每个项目在根目录维护补充全局规则的 `AGENTS.md`，并为每个通用包提供调用者教程；人工智能代理先按项目规则读取当前领域教程和已登记公共入口，再用 `docs/cx` 中的当前用例、设计、固定任务和临时变更文件推进工作。单元测试和测试先行开发只有明确声明时才进入任务范围。

cx 不是组件库，也不是某个项目的业务实现。它只约束协作流程、文档结构、任务拆分、完整面向对象、极简复用、发布版本和交付证据。

项目说明、用例、设计、任务、专题文档和研究笔记只表达当前有效状态。已有 story 的变化、实现改向和代码错误先写入 `changes/`，变更文件先提交到 Git；交付审查通过后删除变更文件并再次提交，历史由 Git 保存。

开发代码只实现当前最新意图。除非用户在当前请求中明确要求具体校验或异常处理，否则不自行校验后抛出异常，不捕获、转换、包装、吞掉或兜底异常；底层异常保持原始类型、信息和调用栈并自然中止程序。旧接口、别名、适配层、桥接层、兼容分支、旧参数、旧配置、旧路径、旧行为和相关痕迹必须全部删除，调用方同步使用当前入口。

代码、文档、教程、研究、设计或流程交付物完成后，必须由 `$cx-review` 连续完成交付物质量审查和完成证据门禁。任一阶段不通过时任务仍未完成，当前变更文件不得删除。

当前包版本：`0.1.2`。cx 仍处于实验阶段，尚未声明稳定的 `1.0.0` 工作流。

英文说明见 [README.md](README.md)。维护本仓库时，中文规则先完成并通过验证，再同步英文规则。

## 安装内容

本仓库发布同一套工作流的两个语言包：

- `SKILLS/zh`：中文 skills。
- `SKILLS/en`：英文 skills。

用户不需要先安装 `cx` 命令。安装和更新直接使用 `shskills` 从 GitHub 读取 `SKILLS/` 目录。

## 安装或更新

本地 Codex skills 只能从仓库默认的 `main` 分支安装或更新。不要从工作分支安装本机长期使用的 skills。

推荐在已经 clone 本仓库的机器上使用安装脚本；它会从远端 `main` 更新 skills，并自动覆盖全局 `AGENTS.md`：

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install_cx_zh.ps1
```

只使用 `shskills` 时，需要另外同步本语言包的 `AGENTS.md`：

```powershell
uv tool install shskills
shskills install --url git@github.com:by90/cx.git --agent custom --dest "$env:USERPROFILE\.codex\skills" --subpath zh --force --clean
```

如果设置了 `CODEX_HOME`，把目标目录改为 `$env:CODEX_HOME\skills`。

## 核心流程

1. `$cx-workflow` 判断请求类型，先在对话中创建可见待办事项列表，并选择最小必要 skills。
2. `$cx-doc` 先读取或建立项目 `AGENTS.md`，再按领域导航读取全部通用包教程和已登记公共入口；`$cx-story` 随后维护当前用例、设计和固定任务集合。
3. 每个主成功场景一个文件夹，例如 `docs/cx/01.创建用户/`。
4. 场景文件夹固定包含 `00.用例.md`、`00.设计.md`、`tasks/` 和 `changes/`。
5. 每个任务是一个 Markdown 文件，例如 `tasks/01.编写用户实体.md`。
6. 已有 story 的每次变化、实现改向和代码错误写入 `changes/<中文变更名>.md`；文件先提交到 Git，完成审查后删除并再次提交。
7. 新 story 建立时一次性确定任务集合；story 建立后任务文件数量、编号、文件名和身份不得改变。实现改向和代码错误直接修改原任务。
8. 一个主成功场景文件夹只承载一个用户目标用例；主成功场景通常 3 到 9 个主步骤，从触发写到目标达成，不把多个互斥选择、页面按钮或完整任务堆进同一个场景。
9. 条件、替代和异常必须用 `1.1`、`2.1` 这类子编号挂到具体主步骤下，并写明后续是返回某一步、结束本用例，还是进入其它独立用例。
10. 如果主成功场景某一步本身需要参与者、前置条件、步骤和条件子步骤，说明它已经是子用例或独立用例，应拆成新的主成功场景文件夹，并在 `docs/cx/00.项目说明.md` 中维护索引。
11. 默认执行模式是完成当前任务文档后只编辑该任务绑定的一个生产代码文件，完成后汇报；只有用户明确要求连续推进多个任务时，才进入下一个代码文件。
12. 默认不创建、不修改、不运行单元测试；只有用户请求、既有任务文档或变更文档明确声明 TDD、单元测试或失败测试时，才由 `$cx-tdd` 执行显式测试流程。
13. 开发代码只实现当前最新意图，调用方同步使用当前入口；除非用户明确要求具体校验或异常处理，否则让底层异常保持原始类型、信息和调用栈并自然中止程序，不保留任何兼容或兜底痕迹。
14. 任一交付物完成后必须由 `$cx-review` 连续执行交付物质量审查和完成证据门禁；通过后删除当前变更文件。
15. 只有用户明确选择逐任务确认时，才在每个任务完成并记录验证证据和 review 结论后停止等待核对。
16. `$cx-tdd` 统一处理测试先行主流程；明确声明 Python、PyTorch 或 Lightning 测试时叠加 `$cx-pytorch-tdd`，明确声明 Rust 测试时叠加 `$cx-rust-tdd`；两个语言技能不处理普通实现流程。

## docs/cx 结构

```text
AGENTS.md
docs/cx/
docs/cx/00.项目说明.md
docs/cx/docs/
docs/cx/docs/00.索引.md
docs/cx/docs/01.通达信服务器协议.md
docs/cx/notes/
docs/cx/notes/01.选择时间序列模型.md
docs/cx/01.创建用户/
docs/cx/01.创建用户/00.用例.md
docs/cx/01.创建用户/00.设计.md
docs/cx/01.创建用户/tasks/
docs/cx/01.创建用户/tasks/01.编写用户实体.md
docs/cx/01.创建用户/changes/
docs/cx/01.创建用户/changes/调整用户实体约束.md
```

项目 `AGENTS.md` 根据项目目标、编程语言、工具链和通用包补充全局规则，并列出各领域必须先读的教程。`docs/cx/docs/` 为每个通用包保存站在调用者角度的独立编号教程，并保存稳定技术过程的专题文档；`docs/cx/notes/` 保存针对具体研究问题的当前结论。所有正式文档只写当前状态，不保存新旧差异或完成变更历史。

## 可用 Skills

| Skill | 用途 |
| --- | --- |
| `$cx-workflow` | 流程分流、任务编排和最小 skill 组合选择 |
| `$cx-story` | 用例、主成功场景、条件子步骤、任务文档和变更文档 |
| `$cx-tdd` | 明确声明时的测试先行、最窄失败测试、最小实现和重构 |
| `$cx-changelog` | `changes/` 临时变更文件的登记、提交、执行和完成删除 |
| `$cx-doc` | 通用包调用者教程、稳定专题文档、研究笔记和项目 `AGENTS.md` 教程导航 |
| `$cx-version` | 项目内 `tools/semver.py`、`VERSION`、`docs/VERSIONS.md`、发布 tag 和发布验证 |
| `$cx-research` | 模型选择、论文研究、来源筛选和带引用综合分析 |
| `$cx-design` | 面向对象设计、职责拆分、领域对象、类命名、继承组合和数据访问边界 |
| `$cx-pytorch-tdd` | 在 `$cx-tdd` 主流程上补充 `unittest`、镜像测试布局、共享真实测试数据和张量检查 |
| `$cx-pytorch-quick-hpo` | PyTorch 快速调参、字段贡献研究、特征组合和候选方案初筛 |
| `$cx-pytorch-full-hpo` | PyTorch 全量调参、完整训练、测试集评估、回测和候选模型选择 |
| `$cx-timeseries-modeling` | 异构多变量时间序列建模、协变量、泄漏检查和 PyTorch Forecasting 选型 |
| `$cx-rust-tdd` | 在 `$cx-tdd` 主流程上补充 Rust 内置测试、共享真实测试数据和 `cargo` 检查 |
| `$cx-common-module` | 可复用功能、可复用类、功能入口和重复逻辑收敛 |
| `$cx-review` | 交付物质量审查、完成证据门禁、文档一致性和剩余风险 |

## 提示词契约

高质量 coding-agent 提示词应说明：

- 目标：要改变的行为或结果。
- 上下文：目标 `docs/cx` 场景、任务、变更、相关文件、分支或环境。
- 约束：接口、语言规则、性能、兼容性或风格限制。
- 必须遵循的流程：要使用的 cx 技能，以及是否明确声明单元测试或测试先行开发、研究、版本管理或统一交付审查。
- 验证方式：期望执行的命令、测试、截图或检查。
- 交付物：代码、当前状态文档、验证证据或最终摘要；未完成变更文件不作为长期交付物。

## 发布版本

cx 使用标准发布机制：

- `VERSION` 是唯一版本来源，只保存不带 `v` 的 SemVer 值。
- `packages/en/manifest.json` 和 `packages/zh/manifest.json` 必须与 `VERSION` 一致。
- 根目录 `CHANGELOG.md` 遵循 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)。
- 发布 tag 使用带注释 Git tag，名称为 `vX.Y.Z`。

常用命令：

```bash
python tools/cx_version.py show .
python tools/cx_version.py check .
python tools/validate_release.py .
```

目标项目复制 `$cx-version` 的 `scripts/semver.py` 到 `tools/semver.py` 后使用：

```bash
python tools/semver.py next feature-group --root .
python tools/semver.py next patch --root .
python tools/semver.py prepare <version> "<标题>" --root .
```

## 发布前验证

```bash
python tools/cx_version.py check .
python tools/validate_release.py .
```
