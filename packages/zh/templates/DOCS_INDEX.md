# docs/INDEX.md

本文件是 `docs/` 根目录的索引和说明。多功能组项目中，`docs/` 根目录只长期保留索引和说明；具体研发文档放入各功能组目录。

## 文档布局

```text
docs/INDEX.md
docs/<feature-group>/ENGINEERING_SPEC.md
docs/<feature-group>/CHANGELOG.md
```

单功能项目可以暂时使用：

```text
docs/ENGINEERING_SPEC.md
docs/CHANGELOG.md
```

## 功能组索引

| Group ID | Folder | Goal | Changes | BDD IDs | Reusable components | Status | Dependencies |
| --- | --- | --- | --- | --- | --- | --- | --- |
| core | `docs/core/` | TODO | TODO | TODO | TODO | planned | TODO |

## 说明

- 每个功能组目录维护自己的 `ENGINEERING_SPEC.md` 和 `CHANGELOG.md`。
- `CHANGE-*` 条目必须能映射回同一功能组的研发主文档。
- 可复用组件先登记到所在功能组的 Reusable Component Registry；跨功能组复用时，也在本索引中标注。
