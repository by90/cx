# BDD/TDD AI 辅助开发流程

## 核心思想

BDD 定义行为和共同语言。TDD 用可执行测试证明行为。AI 编程 agent 只有在被长期文档和验证证据约束时，才真正可靠。

cx 工作流采用这个顺序：

1. 接收用户需求。
2. 在 `docs/CHANGELOG.md` 中更新 `CHANGE-*` 条目。
3. 在 `docs/ENGINEERING_SPEC.md` 中更新行为、BDD 场景、架构说明、任务队列和测试矩阵。
4. 编写预期失败的测试。
5. 运行最窄测试并记录 red failure。
6. 实现最小改动。
7. 运行测试直到 green。
8. 只在测试保持 green 的情况下重构。
9. 记录验证证据。
10. 判断重复逻辑是否应该成为通用模块。

## 为什么坚持一个研发主文档

很多 AI 工作流会为每个需求生成新的 spec、plan 或 task 文件。单看一次任务似乎清楚，但长期项目会变成无法搜索的文档垃圾。cx 让所有新工作都增强同一个研发主文档，而不是制造更多孤立文件。

## 推荐提示词

```text
请使用 $cx-bdd-tdd。先更新 docs/ENGINEERING_SPEC.md 和 docs/CHANGELOG.md。推导 BDD 场景和失败测试，展示预期 red failure，实现最小改动，运行验证并记录证据。不要创建单独规划文档。
```

## 专项提示词

Python ML 工作组合 `$cx-bdd-tdd`、`$cx-pytorch-tdd`，涉及变长 tensor 时再加 `$cx-ragged-tensor`。

Rust 桌面 UI 工作组合 `$cx-bdd-tdd`、`$cx-rust-ui`，涉及进度状态或任务监控时再加 `$cx-progress-ui`。

最终审查使用 `$cx-evidence`，或明确启动只读 subagent `cx-review`。
