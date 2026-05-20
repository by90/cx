# AGENTS.md

## 仓库工作约定

本仓库使用 cx 文档集 BDD/TDD 工作流：`docs/` 根目录负责索引和说明，编号功能组拥有自己的研发文档集。

1. 规划或修改代码前，先阅读 `docs/INDEX.md` 或 `docs/README.md`，再阅读目标功能文件夹的 `BDD.md`、`ENGINEERING_SPEC.md` 和 `CHANGELOG.md`。
2. 流程处理、任务分流和不确定应使用哪个 cx skill 时，优先使用 `$cx-workflow`。
3. 行为发现使用 `$cx-bdd`，测试先行实现使用 `$cx-tdd`。
4. 不要为每个需求新建孤立的 `spec.md`、`plan.md`、`tasks.md` 或零散设计文档；多组功能使用 `docs/<feature-group>/` 文档集。
5. 新需求、BDD 场景、架构说明、任务拆解、测试映射和验证证据都回写到目标文档集的 `ENGINEERING_SPEC.md`。
6. 目标文档集的 `CHANGELOG.md` 只做历史记录。每个 `CHANGE-*` 条目都必须能映射回同一文档集的研发主文档。
7. 完成 BDD、研发主文档、实现计划或变更记录后必须停止，向用户汇报文档结果和下一步实现计划，等待用户明确确认；确认前不能写测试、不能改实现、不能进入 TDD。
8. 用户确认后，从 BDD 行为开始，先写失败测试，再实现最小改动，然后重构。
9. 优先封装可复用组件和通用模块；新增工具、数据结构、测试夹具或 UI state 前，先搜索已有实现、相关 skills 和 Common Module Registry。
10. 任何功能组都必须使用独立分支。完成的功能组分支先合并到 `dev`，不得直接合并到 `main`。
11. 只有用户确认版本完成后，才允许将 `dev` 合并到 `main`；只有 `main` 可用于版本提交、release tag 和 release tag push。功能分支和 `dev` 仍然可以为了协作、备份或 CI 正常 push。
12. 修改后先运行最窄的有效测试，再按需要运行更宽的验证，并记录命令和结果。
13. 新增或修改代码时，代码文件、类、函数和关键语句都必须写面向初学者的相近说明注释；默认逐行解释代码意图，除非该行是纯格式或重复结构。

## 提示词契约

coding-agent 提示词应说明：

- 目标：要改变的行为或结果。
- 上下文：目标功能文件夹、相关文件、分支或环境。
- 约束：API、语言规则、性能、兼容性或风格限制。
- 必须遵循的流程：要使用的 cx skills，以及是否需要 BDD、TDD、研究、版本管理或证据审查。
- 验证方式：期望执行的命令、测试、截图或检查。
- 交付物：代码、文档、changelog、证据或最终摘要。
- 分支：功能组分支名、合并目标 `dev`，以及是否请求发布交接到 `main`。

如果仓库也使用 Claude Code，请把本 `AGENTS.md` 作为共同规则来源，让 `CLAUDE.md` 引用或指向它，不要重复维护两份规则。

## Skill 路由

- `$cx-workflow`：流程处理、任务分流和多个 cx skills 的编排入口。
- `$cx-bdd`：BDD 发现、编号功能文件夹、业务规则和场景。
- `$cx-tdd`：测试先行实现、red-green-refactor 和测试矩阵证据。
- `$cx-changelog`：变更记录、发布说明、`CHANGE-*` 一致性。
- `$cx-version`：用 SemVer、VERSION、changelog 和带注释 tag 管理发布版本。
- `$cx-research`：模型选择、AI 论文研究、来源筛选和带引用综合分析。
- `$cx-pytorch-tdd`：Python、PyTorch、Lightning、tensor、训练与 ML 测试。
- `$cx-rust-tdd`：Rust 实现、所有权设计和 cargo test/fmt/clippy。
- `$cx-common-module`：复用组件、通用模块抽取和公共 API 设计。
- `$cx-evidence`：合并或交付前的证据审查。

## Python 规则

- 使用项目级 `uv` 虚拟环境；安装依赖和运行 Python 命令优先使用 `uv sync`、`uv run` 或项目已有的 `uv` 工作流。
- 创建或重建 Python / PyTorch 环境前，访问 Python 官网和 PyTorch 官网，确认 Python、PyTorch 与 CUDA 组合为当前官方稳定版本；不要默认使用 nightly、预发布或非官方轮子。
- 默认用函数组织 Python 代码；只有在设计更清楚或用户要求时才使用类。
- 对状态、生命周期、不变量和领域对象协作使用面向对象设计。
- 禁止默认使用 `getattr`、`setattr`、`delattr`、monkey patch 或动态注入方法；只有没有明确静态 API 时才允许，并且必须记录理由、隔离实现和测试。
- 代码格式遵循 Black 默认规范。
- 测试使用 Python 自带的 `unittest`，不要引入 `pytest`，除非项目已经明确采用它。
- PyTorch 和 Lightning API 或版本相关行为必须查官方最新文档。
- tensor 测试要覆盖 shape、dtype、device、确定性和边界场景。
- 训练测试必须很小：优先 CPU、小 batch、小模型、`fast_dev_run` 或有限 batch。
- 单元测试尽量使用真实的小型测试数据；涉及数据库时优先使用缩小的 SQLite 数据库或 fixture，只有外部服务、时间、随机性等边界难以真实控制时才少量使用 mock。

## Windows 工具链规则

- 在 Windows 上，如果任务明确需要 `ng` 命令但本机没有安装，先安装项目要求的 `ng` CLI，再继续执行；不要用 PowerShell 脚本、`ps` 别名或临时替代命令绕过 `ng`。
- 优先使用项目锁定的包管理器安装 `ng`，例如已有 `package-lock.json` 时使用 `npm`，已有 `pnpm-lock.yaml` 时使用 `pnpm`，已有 `yarn.lock` 时使用 `yarn`；没有项目约束时，说明假设后安装 Angular CLI。
- 安装后运行 `ng version` 或项目约定的等效版本命令，确认 CLI 可用，再运行后续生成、构建或测试命令。

## Rust / GPUI 规则

- Rust 单元测试使用语言内置测试机制和 `cargo test`，不要引入额外测试框架，除非项目已经明确采用。
- Rust 修改后运行 `cargo fmt` 和 `cargo test`，可行时运行 `cargo clippy --all-targets --all-features`。
- 用 struct/enum/trait 和明确 `Result` 错误表达领域状态。
- 生产路径避免 `unwrap`、`expect` 和 `panic!`，除非不变量局部、已证明并记录。
- 将纯状态、reducer 和渲染代码分离。
- 新增可复用 UI state、组件 API 或 reducer 前，先搜索 Common Module Registry 和已有实现。
- 尽可能使用无状态 gpui-component 元素，由 view 持有状态。
- UI 组件 API 保持小而可复用。

## 文档策略

单功能项目可以使用一个根文档集：

```text
docs/ENGINEERING_SPEC.md
docs/CHANGELOG.md
```

多功能组项目使用编号功能目录，`docs/` 根目录只保留索引和说明：

```text
docs/INDEX.md
docs/1.配置系统/BDD.md
docs/1.配置系统/ENGINEERING_SPEC.md
docs/1.配置系统/CHANGELOG.md
```

其他生成文档默认视为临时文件，除非用户明确批准。需要计划时，写入目标文档集 `ENGINEERING_SPEC.md` 的 Task Queue 章节。

安装中文 cx 包时，所有 cx 生成或维护的文档必须使用简体中文，并且长期保留的文档必须放在项目的 `docs/` 文件夹下。代码标识符、命令、API 名称和外部英文专名可以保留原文。

BDD 场景、测试矩阵、实现计划和验证证据必须写入项目 `docs/` 文件夹中的目标研发文档集。

## Git 提交规则

- 用户要求提交、交付、发 PR 或发布时，把当前工作区视为一次整体变更，不要分析哪些文件是自己修改的、哪些是用户修改的、哪些是尚未跟踪的。
- 提交前运行 `git status --short` 只用于确认工作区内容和发现明显风险，不用于按来源拆分文件。
- 默认暂存所有已跟踪和未跟踪文件，并创建一个提交；不要把同一任务拆成多个提交，除非用户明确要求。
- 只有发现明显密钥、凭据、本地环境文件、构建产物、依赖目录或无关大文件时，才先停止并请求用户确认。
- 提交信息应描述用户请求对应的整体结果，而不是逐文件列出来源。
- 工作完成后，把功能分支合并到 `dev`，随后删除本地功能分支。
- 只有用户明确要求时，才允许把功能分支推送到远端；默认不要 push 功能分支。
- 默认只推送 `dev`；只有用户明确要求发布交接或合并到 `main` 时，才合并并推送 `main`。

## 推荐验证命令

```bash
python -m unittest discover -s tests
cargo fmt --check
cargo test
cargo clippy --all-targets --all-features
```

如果项目自行安装了 cx 验证工具，也可以运行 `python tools/validate_single_source.py .`。
