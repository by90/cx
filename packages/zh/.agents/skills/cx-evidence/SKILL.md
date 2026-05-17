---
name: cx-evidence
description: 用于任务、分支或 PR 交付前检查 BDD/TDD compliance、非编程任务验证、test output、changelog/spec single-source consistency、branch flow 和 document-sprawl problems。
version: 1.0.0
---

# cx 证据审查

## 目的

审查工作是否真的有测试和目标研发文档集支撑。这是交付门槛，不是只看风格的 review。

## 审查清单

1. 每个变更是否都有目标文档集 `CHANGELOG.md` 中的 `CHANGE-*` 条目？
2. 同一文档集的 `ENGINEERING_SPEC.md` 是否没有出现具体 `CHANGE-*` 编号？
3. 行为变化是否新增或更新了 BDD 场景？
4. 编程行为的每个 BDD 场景是否映射到测试？
5. 编程任务实现前是否展示了预期 red failure？
6. 非编程任务是否没有启动 TDD，并改用检查清单、审阅证据或交付确认？
7. 测试命令和结果是否记录？
8. 多功能组项目是否把 `docs/` 根目录限制为索引、说明和 `VERSIONS.md`，并把具体文档放入 `docs/<feature-group>/`？
9. 功能组目录是否按需要包含 `ENGINEERING_SPEC.md`、`CHANGELOG.md` 和 `GUIDE.md`？
10. 是否创建了孤立规划文档？
11. 可复用组件是否先搜索已有实现、相关 skills、历史项目和 Common Module Registry，再抽取或说明不抽取理由？
12. 工作是否在功能组或变更分支完成，合并到 `dev` 后删除工作分支？
13. 完成功能组准备发布时，是否使用版本工具更新 `docs/VERSIONS.md`？
14. Python 测试是否默认使用 `unittest`，除非项目有例外？
15. Rust 代码变更是否运行了必要 cargo 命令？

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
