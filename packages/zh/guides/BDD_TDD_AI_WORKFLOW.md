# BDD/TDD AI 辅助开发流程

## 核心思想

BDD 定义行为和共同语言。TDD 只用于编程任务，用可执行测试证明代码行为。非编程任务不使用 TDD，而是用检查清单、审阅证据或交付确认来验证。AI 编程 agent 只有在被长期文档和验证证据约束时，才真正可靠。

cx 工作流采用这个顺序：

1. 接收用户需求。
2. 选择或创建目标文档集；多功能组项目使用 `docs/<feature-group>/ENGINEERING_SPEC.md`、同目录 `CHANGELOG.md` 和可选 `GUIDE.md`。
3. 在目标 `CHANGELOG.md` 中更新 `CHANGE-*` 条目；具体变更编号不要写入 `ENGINEERING_SPEC.md`。
4. 在目标 `ENGINEERING_SPEC.md` 中更新行为、主成功场景、分支场景、异常场景、架构说明和测试矩阵。
5. 编程任务编写预期失败的测试；非编程任务改写检查清单或验收证据。
6. 编程任务运行最窄测试并记录 red failure。
7. 实现或整理最小改动。
8. 运行测试或检查直到通过。
9. 只在测试或检查保持通过的情况下重构或整理。
10. 记录验证证据。
11. 搜索已有实现、相关 skills、历史项目和 registry，判断重复逻辑是否应该成为复用组件。
12. 完成功能组后合并到 `dev`，并使用版本工具更新 `docs/VERSIONS.md`。

## 为什么坚持 docs 文档集

很多 AI 工作流会为每个需求生成新的 spec、plan 或 task 文件。单看一次任务似乎清楚，但长期项目会变成无法搜索的文档垃圾。cx 让所有新工作进入明确的 `docs/` 文档集：小项目可以只有一个文档集，大项目按功能组拆成多个目录，并用 `docs/INDEX.md` 统一索引。变更任务顺序只在各功能组 `CHANGELOG.md` 中维护。

## 推荐提示词

```text
请使用 $cx-bdd-tdd。先选择或创建目标 docs 文档集，更新其中的 ENGINEERING_SPEC.md 和 CHANGELOG.md。推导主成功场景、分支场景、异常场景；编程任务推导失败测试并展示预期 red failure，非编程任务不要使用 TDD。实现最小改动，运行验证并记录证据。不要创建单独规划文档。
```

## 专项提示词

Python ML 工作组合 `$cx-bdd-tdd`、`$cx-pytorch-tdd`，涉及变长 tensor 时再加 `$cx-ragged-tensor`。

Rust 桌面 UI 工作组合 `$cx-bdd-tdd`、`$cx-rust-ui`，涉及进度状态或任务监控时再加 `$cx-progress-ui`。

最终审查使用 `$cx-evidence`，或明确启动只读 subagent `cx-review`。
