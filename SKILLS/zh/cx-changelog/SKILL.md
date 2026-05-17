---
name: cx-changelog
description: 用于 changelog、release notes、change IDs、audit trails、按顺序安排变更任务，以及确保 CHANGE 条目只保存在目标文档集的 CHANGELOG 中。
version: 1.0.0
---

# cx 变更记录维护

## 目的

将目标文档集的 `CHANGELOG.md` 维护为唯一按顺序记录变更和变更任务的文档。它不能变成第二份需求文档，也不能复制长篇行为说明。多功能组项目中，每个 `docs/<feature-group>/CHANGELOG.md` 只记录该功能组历史，`docs/INDEX.md` 负责跨功能组索引。

## 规则

1. 每个条目必须有稳定的 `CHANGE-YYYY-NNN` ID。
2. 每个条目必须包含日期、类型、状态、工作分支、目标基线分支、功能组、摘要、相关场景、测试和证据。
3. 具体变更编号只能出现在 `CHANGELOG.md` 或发布索引中，不要复制到同一文档集的 `ENGINEERING_SPEC.md`。
4. 不要把长需求复制进变更记录。
5. 一个功能组或一次变更通常使用单独工作分支，完成后合并到 `dev` 并删除工作分支。
6. 完成一组功能并准备发布时，用版本工具追加 `docs/VERSIONS.md`，例如 `v0.0.1 "创建项目模板"`。
7. 除非用户明确要求，不要创建单独 release note 文档。
8. 条目要足够短，便于扫描；同时足够具体，便于审计和安排任务顺序。

## 条目模板

```markdown
### CHANGE-YYYY-NNN - Title

- Date:
- Type: feature | bugfix | refactor | test | docs | research
- Status: planned | in_progress | done | blocked
- Branch:
- Base branch: dev
- Feature group:
- Task order:
- Summary:
- Related scenarios:
- Related tests:
- Verification evidence:
```
