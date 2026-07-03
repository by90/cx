# cx Codex 用例驱动工作流包

cx 是用于规范人类与 AI 协作研发的 Codex skill 包。它的核心目标是让 AI 先用 `docs/cx` 中的用例、设计、任务和变更文档固定需求，再默认按一个任务文档和一个生产代码文件推进 Python、PyTorch 与 Rust 项目；单元测试和 TDD 只有明确声明时才进入任务范围。

cx 不是组件库，也不是某个项目的业务实现。它只约束协作流程、文档结构、任务拆分、完整 OOP、极简复用、发布版本和交付证据。

代码、文档、教程、研究、设计、流程变更或发布说明等交付物完成后，必须先做 `$cx-review`，再认定任务、变更或交付物完成。review 不通过时，当前状态保持未完成，必须先修复文档不一致、重复味道、非 OOP、臃肿实现、多余校验、多余变量传递、多余命名、业务语义偏差、教程不可执行、研究来源不足或设计不可落地等问题。

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
2. `$cx-story` 维护 `docs/cx` 下的用例、设计、任务和变更文档；所有需求都用“主成功场景 + 挂靠具体步骤的条件子步骤”表达。
3. 每个主成功场景一个文件夹，例如 `docs/cx/01.创建用户/`。
4. 场景文件夹固定包含 `00.用例.md`、`00. 设计.md`、`tasks/` 和 `changes/`。
5. 每个任务是一个文件夹，例如 `tasks/01.编写用户实体/00.任务.md`。
6. 每次变更写入 `changes/<时间戳>-任务<编号>-<任务名称>.md`，AI 开始工作前优先检查未完成变更。
7. 一个任务只处理一份任务文档和一个生产代码文件；需要第二个代码文件时先拆成下一个任务。只有明确声明单元测试或 TDD 时，才额外处理一个一一对应的单元测试文件。
8. 一个主成功场景文件夹只承载一个用户目标用例；主成功场景通常 3 到 9 个主步骤，从触发写到目标达成，不把多个互斥选择、页面按钮或完整任务堆进同一个场景。
9. 条件、替代和异常必须用 `1.1`、`2.1` 这类子编号挂到具体主步骤下，并写明后续是返回某一步、结束本用例，还是进入其它独立用例。
10. 如果主成功场景某一步本身需要参与者、前置条件、步骤和条件子步骤，说明它已经是子用例或独立用例，应拆成新的主成功场景文件夹，并在 `docs/cx/00.项目说明.md` 中维护索引。
11. 默认执行模式是完成当前任务文档后只编辑该任务绑定的一个生产代码文件，完成后汇报；只有用户明确要求连续推进多个任务时，才进入下一个代码文件。
12. 默认不创建、不修改、不运行单元测试；只有用户请求、既有任务文档或变更文档明确声明 TDD、单元测试或失败测试时，才由 `$cx-tdd` 执行显式测试流程。
13. 任一交付物完成后必须由 `$cx-review` 执行对应类型本地 review；交付前由 `$cx-evidence` 核验 review 结论和证据。两者通过后才能把任务或变更标记完成。
14. 只有用户明确选择逐任务确认时，才在每个任务完成并记录验证证据和 review 结论后停止等待核对。
15. `$cx-pytorch-tdd` 只在明确声明 Python/PyTorch 测试时叠加；`$cx-rust-tdd` 处理 Rust 实现和显式测试；`$cx-common-module` 补充复用入口约束。

## docs/cx 结构

```text
docs/cx/
docs/cx/00.项目说明.md
docs/cx/01.创建用户/
docs/cx/01.创建用户/00.用例.md
docs/cx/01.创建用户/00. 设计.md
docs/cx/01.创建用户/tasks/
docs/cx/01.创建用户/tasks/01.编写用户实体/00.任务.md
docs/cx/01.创建用户/changes/
docs/cx/01.创建用户/changes/20260629T120000-任务01-编写用户实体.md
```

`docs/cx` 可以放项目说明和重要业务领域文档。所有 cx 场景、任务、流程和变更文档只能放在 `docs/cx` 下；其它位置的文档不属于 cx 流程。

## 可用 Skills

| Skill | 用途 |
| --- | --- |
| `$cx-workflow` | 流程分流、任务编排和最小 skill 组合选择 |
| `$cx-story` | 用例、主成功场景、条件子步骤、任务文件夹和变更文件夹 |
| `$cx-tdd` | 明确声明时的测试先行、最窄失败测试、最小实现和重构 |
| `$cx-changelog` | `changes/` 变更文档、发布说明和审计轨迹 |
| `$cx-version` | 项目内 `tools/semver.py`、`VERSION`、`docs/VERSIONS.md`、发布 tag 和发布验证 |
| `$cx-research` | 模型选择、论文研究、来源筛选和带引用综合分析 |
| `$cx-pytorch-tdd` | Python、PyTorch、Lightning、tensor、训练与机器学习测试 |
| `$cx-pytorch-quick-hpo` | PyTorch 快速调参、字段贡献研究、特征组合和候选方案初筛 |
| `$cx-pytorch-full-hpo` | PyTorch 全量调参、完整训练、测试集评估、回测和候选模型选择 |
| `$cx-timeseries-modeling` | 异构多变量时间序列建模、协变量、泄漏检查和 PyTorch Forecasting 选型 |
| `$cx-rust-tdd` | Rust 类型设计、所有权设计、可选显式测试、`cargo fmt`、`cargo test` 和 `clippy` |
| `$cx-common-module` | 可复用功能、可复用类、公共入口和重复逻辑收敛 |
| `$cx-review` | 代码、文档、教程、研究、设计和流程变更完成后的强制本地 review |
| `$cx-evidence` | 交付前证据审查、review 结论核验、文档一致性和剩余风险 |

## 提示词契约

高质量 coding-agent 提示词应说明：

- 目标：要改变的行为或结果。
- 上下文：目标 `docs/cx` 场景、任务、变更、相关文件、分支或环境。
- 约束：接口、语言规则、性能、兼容性或风格限制。
- 必须遵循的流程：要使用的 cx skills，以及是否明确声明单元测试或 TDD、研究、版本管理或证据审查。
- 验证方式：期望执行的命令、测试、截图或检查。
- 交付物：代码、文档、变更记录、证据或最终摘要。

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
