# AGENTS.md

## 仓库工作约定

本仓库使用 cx 文档集 BDD/TDD 工作流：`docs/` 根目录负责索引和说明，具体功能组可以拥有自己的研发文档集。

1. 规划或修改代码前，先阅读 `docs/INDEX.md` 或 `docs/README.md`，再阅读目标文档集的 `ENGINEERING_SPEC.md` 和 `CHANGELOG.md`。
2. 流程处理、任务分流和不确定应使用哪个 cx skill 时，优先使用 `$cx-workflow`。
3. 功能、缺陷、需求、架构和实现规划任务使用 `$cx-bdd-tdd`。
4. 不要为每个需求新建孤立的 `spec.md`、`plan.md`、`tasks.md` 或零散设计文档；多组功能使用 `docs/<feature-group>/` 文档集。
5. 新需求、BDD 场景、架构说明、任务拆解、测试映射和验证证据都回写到目标文档集的 `ENGINEERING_SPEC.md`。
6. 目标文档集的 `CHANGELOG.md` 只做历史记录。每个 `CHANGE-*` 条目都必须能映射回同一文档集的研发主文档。
7. 从 BDD 行为开始，先写失败测试，再实现最小改动，然后重构。
8. 优先封装可复用组件和通用模块；新增工具、数据结构、测试夹具或 UI state 前，先搜索已有实现、相关 skills 和 Common Module Registry。
9. 修改后先运行最窄的有效测试，再按需要运行更宽的验证，并记录命令和结果。
10. 新增或修改代码时，代码文件、类、函数和关键语句都必须写面向初学者的相近说明注释；默认逐行解释代码意图，除非该行是纯格式或重复结构。

## Skill 路由

- `$cx-workflow`：流程处理、任务分流和多个 cx skills 的编排入口。
- `$cx-bdd-tdd`：功能、缺陷、规划和需求任务的 BDD/TDD 主流程。
- `$cx-changelog`：变更记录、发布说明、`CHANGE-*` 一致性。
- `$cx-pytorch-tdd`：Python、PyTorch、Lightning、tensor、训练与 ML 测试。
- `$cx-ragged-tensor`：padding、mask、length、collate、变长 tensor。
- `$cx-progress-ui`：多任务进度状态、取消、ETA、CLI 适配器、GPUI 进度组件。
- `$cx-rust-ui`：Rust、GPUI、gpui-component、UI 状态和组件测试。
- `$cx-common-module`：复用组件、通用模块抽取和公共 API 设计。
- `$cx-evidence`：合并或交付前的证据审查。

## Python 规则

- 使用项目级 `uv` 虚拟环境；安装依赖和运行 Python 命令优先使用 `uv sync`、`uv run` 或项目已有的 `uv` 工作流。
- 创建或重建 Python / PyTorch 环境前，访问 Python 官网和 PyTorch 官网，确认 Python、PyTorch 与 CUDA 组合为当前官方稳定版本；不要默认使用 nightly、预发布或非官方轮子。
- 默认用函数组织 Python 代码；只有在设计更清楚或用户要求时才使用类。
- 代码格式遵循 Black 默认规范。
- 测试使用 Python 自带的 `unittest`，不要引入 `pytest`，除非项目已经明确采用它。
- PyTorch 和 Lightning API 或版本相关行为必须查官方最新文档。
- tensor 测试要覆盖 shape、dtype、device、确定性和边界场景。
- 训练测试必须很小：优先 CPU、小 batch、小模型、`fast_dev_run` 或有限 batch。
- 单元测试尽量使用真实的小型测试数据；涉及数据库时优先使用缩小的 SQLite 数据库或 fixture，只有外部服务、时间、随机性等边界难以真实控制时才少量使用 mock。

## Rust / GPUI 规则

- Rust 单元测试使用语言内置测试机制和 `cargo test`，不要引入额外测试框架，除非项目已经明确采用。
- Rust 修改后运行 `cargo fmt` 和 `cargo test`，可行时运行 `cargo clippy --all-targets --all-features`。
- 将纯状态、reducer 和 GPUI 渲染代码分离。
- 新增可复用 UI state、组件 API 或 reducer 前，先搜索 Common Module Registry 和已有实现。
- 尽可能使用无状态 gpui-component 元素，由 view 持有状态。
- UI 组件 API 保持小而可复用。

## 文档策略

单功能项目可以使用一个根文档集：

```text
docs/ENGINEERING_SPEC.md
docs/CHANGELOG.md
```

多功能组项目使用多个功能目录，`docs/` 根目录只保留索引和说明：

```text
docs/INDEX.md
docs/<feature-group>/ENGINEERING_SPEC.md
docs/<feature-group>/CHANGELOG.md
```

其他生成文档默认视为临时文件，除非用户明确批准。需要计划时，写入目标文档集 `ENGINEERING_SPEC.md` 的 Task Queue 章节。

中文版本或中文交付物中的所有文档必须使用简体中文，并且长期保留的文档必须放在项目的 `docs/` 文件夹下。

BDD 场景、测试矩阵、实现计划和验证证据必须写入项目 `docs/` 文件夹中的目标研发文档集。

## 推荐验证命令

```bash
python -m unittest discover -s tests
cargo fmt --check
cargo test
cargo clippy --all-targets --all-features
```

如果项目自行安装了 cx 验证工具，也可以运行 `python tools/validate_single_source.py .`。
