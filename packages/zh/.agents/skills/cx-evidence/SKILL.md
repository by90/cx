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
12. Python 源码是否位于 `src/<subsystem>/`，测试是否在 `tests/` 下镜像 `src` 结构，并按 `xx.py` -> `xx_test.py` 一一对应？
13. 新增或修改的代码文件、类、函数和每一行业务代码是否都有说明注释？
14. Python 默认行为是否通过默认参数、配置对象、dataclass、factory 或小方法表达，而不是在 `__init__` 中堆叠大量分支？
15. 代码是否保持极简、短小、直接，并且可复用逻辑已经先使用 `$cx-common-module` 搜索和登记？
16. 是否避免了非 OOP 的动态访问方式，例如 `getattr`、`setattr`、`delattr`、monkey patch、动态注入或字符串分发；如不可避免，是否记录理由、隔离实现并测试？
17. Rust 代码变更是否运行了必要 cargo 命令？
18. 工作是否满足提示词契约：目标、上下文、约束、必须遵循的流程、验证方式和交付物？
19. 最终摘要是否报告已运行命令、结果、跳过检查及原因、残留风险？

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
