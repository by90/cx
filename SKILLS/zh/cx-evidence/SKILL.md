---
name: cx-evidence
description: 用于任务、分支或 PR 交付前检查 BDD/TDD compliance、test output、changelog/spec consistency 和 document-sprawl problems。
version: 1.0.0
---

# cx 证据审查

## 目的

审查工作是否真的有测试和单一研发文档策略支撑。这是交付门槛，不是只看风格的 review。

## 审查清单

1. 每个变更是否都有 `CHANGE-*` 条目？
2. 每个 `CHANGE-*` 条目是否映射到 `docs/ENGINEERING_SPEC.md`？
3. 行为变化是否新增或更新了 BDD 场景？
4. 每个 BDD 场景是否映射到测试？
5. 实现前是否展示了预期 red failure？
6. 测试命令和结果是否记录？
7. 是否创建了孤立规划文档？
8. 重复逻辑是否被抽取或说明理由？
9. Python 测试是否默认使用 `unittest`，除非项目有例外？
10. Rust 代码变更是否运行了必要 cargo 命令？

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
