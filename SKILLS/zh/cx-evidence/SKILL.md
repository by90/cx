---
name: cx-evidence
description: 用于任务、分支或 PR 交付前检查 BDD/TDD compliance、test output、changelog/spec consistency 和 document-sprawl problems。
version: 0.1.0
---

# cx 证据审查

## 目的

审查工作是否真的有测试和目标研发文档集支撑。这是交付门槛，不是只看风格的 review。

## 审查清单

1. 每个变更是否都有 `CHANGE-*` 条目？
2. 每个 `CHANGE-*` 条目是否映射到同一文档集的 `ENGINEERING_SPEC.md`？
3. 行为变化是否新增或更新了 BDD 场景？
4. 每个 BDD 场景是否映射到测试？
5. 文档完成后、测试或实现开始前，是否有用户明确确认？
6. 实现前是否展示了预期 red failure？
7. 测试命令和结果是否记录？
8. 多功能组项目是否把 `docs/` 根目录限制为索引和说明，并把具体文档放入 `docs/<feature-group>/`？
9. 是否创建了孤立规划文档？
10. 可复用组件是否先搜索已有实现、相关 skills 和 Common Module Registry，再抽取或说明不抽取理由？
11. Python 测试是否默认使用 `unittest`，除非项目有例外？
12. Rust 代码变更是否运行了必要 cargo 命令？
13. 工作是否满足提示词契约：目标、上下文、约束、必须遵循的流程、验证方式和交付物？
14. 最终摘要是否报告已运行命令、结果、跳过检查及原因、残留风险？

## 输出格式

```text
Findings:
1. [severity] file:line - issue
   Evidence:
   Fix:

Verified:
- command -> result

Missing evidence:
- ...
```
