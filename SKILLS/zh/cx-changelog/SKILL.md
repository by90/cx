---
name: cx-changelog
description: 用于 changelog、release notes、change IDs、audit trails，以及确保 CHANGE 条目映射回目标文档集的 ENGINEERING_SPEC 研发主文档。
version: 0.1.0
---

# cx 变更记录维护

## 目的

将目标文档集的 `CHANGELOG.md` 维护为简洁的历史索引。它不能变成第二份需求文档，也不能复制长篇行为说明。所有项目都按多个功能组组织，每个 `docs/001_feature_name/CHANGELOG.md` 只记录该功能组历史，`docs/INDEX.md` 负责跨功能组索引。

## 规则

1. 每个条目必须有稳定的 `CHANGE-YYYY-NNN` ID。
2. 每个条目必须包含日期、类型、摘要、相关研发主文档章节、BDD 场景、测试和证据。
3. 如果变更记录条目没有对应目标研发主文档内容，先更新同一文档集的 `ENGINEERING_SPEC.md`。
4. 不要把长需求复制进变更记录。
5. 除非用户明确要求，不要创建单独 release note 文档。
6. 条目要足够短，便于扫描；同时足够具体，便于审计。

## 条目模板

```markdown
### CHANGE-YYYY-NNN - Title

- Date:
- Type: feature | bugfix | refactor | test | docs | research
- Summary:
- Engineering spec sections:
- Related BDD scenarios:
- Related tests:
- Verification evidence:
```
