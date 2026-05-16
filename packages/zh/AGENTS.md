# AGENTS.md

## 仓库工作约定

本仓库使用 cx 单一研发文档 BDD/TDD 工作流。

1. 规划或修改代码前，先阅读 `docs/ENGINEERING_SPEC.md` 和 `docs/CHANGELOG.md`。
2. 功能、缺陷、需求、架构和实现规划任务优先使用 `$cx-bdd-tdd`。
3. 不要为每个需求新建 `spec.md`、`plan.md`、`tasks.md` 或零散设计文档，除非用户明确要求单独产物。
4. 新需求、BDD 场景、架构说明、任务拆解、测试映射和验证证据都回写到 `docs/ENGINEERING_SPEC.md`。
5. `docs/CHANGELOG.md` 只做历史记录。每个 `CHANGE-*` 条目都必须能映射回研发主文档。
6. 从 BDD 行为开始，先写失败测试，再实现最小改动，然后重构。
7. 优先封装可复用通用模块，新增工具前先检查 Common Module Registry。
8. 修改后先运行最窄的有效测试，再按需要运行更宽的验证，并记录命令和结果。

## Skill 路由

- `$cx-bdd-tdd`：功能、缺陷、规划和需求任务的默认入口。
- `$cx-changelog`：变更记录、发布说明、`CHANGE-*` 一致性。
- `$cx-pytorch-tdd`：Python、PyTorch、Lightning、tensor、训练与 ML 测试。
- `$cx-ragged-tensor`：padding、mask、length、collate、变长 tensor。
- `$cx-progress-ui`：多任务进度状态、取消、ETA、CLI 适配器、GPUI 进度组件。
- `$cx-rust-ui`：Rust、GPUI、gpui-component、UI 状态和组件测试。
- `$cx-common-module`：通用模块抽取和公共 API 设计。
- `$cx-evidence`：合并或交付前的证据审查。

## Python 规则

- 默认用函数组织 Python 代码；只有在设计更清楚或用户要求时才使用类。
- 代码格式遵循 Black 默认规范。
- 测试默认使用 Python 自带的 `unittest`，除非项目已有明确例外。
- PyTorch 和 Lightning API 或版本相关行为必须查官方最新文档。
- tensor 测试要覆盖 shape、dtype、device、确定性和边界场景。
- 训练测试必须很小：优先 CPU、小 batch、小模型、`fast_dev_run` 或有限 batch。

## Rust / GPUI 规则

- Rust 修改后运行 `cargo fmt` 和 `cargo test`，可行时运行 `cargo clippy --all-targets --all-features`。
- 将纯状态、reducer 和 GPUI 渲染代码分离。
- 尽可能使用无状态 gpui-component 元素，由 view 持有状态。
- UI 组件 API 保持小而可复用。

## 文档策略

目标仓库中允许长期存在的研发文档只有：

```text
docs/ENGINEERING_SPEC.md
docs/CHANGELOG.md
```

其他生成文档默认视为临时文件，除非用户明确批准。需要计划时，写入 `docs/ENGINEERING_SPEC.md` 的 Task Queue 章节。

## 推荐验证命令

```bash
python -m unittest discover -s tests
cargo fmt --check
cargo test
cargo clippy --all-targets --all-features
```

如果项目自行安装了 cx 验证工具，也可以运行 `python tools/validate_single_source.py .`。
