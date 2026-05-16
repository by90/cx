---
name: cx-workflow
description: 用于流程处理、任务分流、端到端研发编排、选择应使用的 cx skills、决定是否需要 BDD/TDD、changelog、证据审查、专项技术 skill 或人工澄清。
version: 1.0.0
---

# cx 流程处理

## 目的

使用本 skill 作为 cx 工作流入口。它负责判断用户请求属于哪类工作、选择需要组合的 cx skills、安排执行顺序，并在需求不清或风险过高时先澄清。

## 流程入口

1. 先判断任务类型：需求讨论、功能实现、缺陷修复、重构、专项技术实现、文档更新、证据审查或安装使用问题。
2. 识别项目是否已经存在 `docs/ENGINEERING_SPEC.md`、`docs/CHANGELOG.md` 和 `AGENTS.md`。
3. 判断是否会改变代码行为、公共 API、数据结构、用户工作流或发布方式。
4. 根据影响范围选择最小必要的 cx skills，不要一次性套用所有 skills。
5. 给出当前步骤或直接执行；只有需求缺口会导致错误实现时才先提问。

## Skill 选择

- 行为变更、缺陷修复、架构调整、实现规划：使用 `$cx-bdd-tdd`。
- 只更新变更记录或检查 change ID：使用 `$cx-changelog`。
- Python、PyTorch、Lightning、tensor 或 ML 测试：叠加 `$cx-pytorch-tdd`。
- 变长 tensor、mask、padding、collation：叠加 `$cx-ragged-tensor`。
- Rust、GPUI、gpui-component 桌面 UI：叠加 `$cx-rust-ui`。
- 多任务进度、ETA、取消、后台任务适配器：叠加 `$cx-progress-ui`。
- 抽取公共模块、稳定 API、迁移重复逻辑：叠加 `$cx-common-module`。
- 交付前检查、测试证据、文档一致性：使用 `$cx-evidence`。

## 执行顺序

1. 对普通研发任务，先走 `$cx-bdd-tdd`，再叠加专项 skill。
2. 对已有实现的收尾任务，先检查文档和测试证据，再使用 `$cx-evidence`。
3. 对仅安装、更新、语言切换或 shskills 使用问题，直接回答命令，不启动 BDD/TDD。
4. 对只读分析或代码审查，先读相关文件并列出风险，不做代码改动，除非用户要求修复。
5. 对跨多个模块的大改动，先把任务拆成可验证的小步骤，并把顺序写入研发主文档的 Task Queue。

## 停止条件

- 缺少关键业务规则、目标环境或验收标准，并且继续实现会造成明显返工。
- 用户要求的实现与现有 `AGENTS.md`、技术约束或公开 API 冲突。
- 需要联网核对高风险或易变信息，但当前环境无法验证。

遇到停止条件时，先说明阻塞点和需要用户确认的最少问题。
