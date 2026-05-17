# docs/INDEX.md

本文件是 `docs/` 根目录的索引和说明。多功能组项目中，`docs/` 根目录只长期保留索引、说明和版本索引；具体研发文档放入各功能组目录。

## 文档布局

```text
docs/INDEX.md
docs/VERSIONS.md
docs/<feature-group>/ENGINEERING_SPEC.md
docs/<feature-group>/CHANGELOG.md
docs/<feature-group>/GUIDE.md
```

单功能项目可以暂时使用：

```text
docs/ENGINEERING_SPEC.md
docs/CHANGELOG.md
docs/GUIDE.md
```

## 功能组索引

| Group ID | Folder | Goal | Changelog | BDD IDs | Reusable components | Status | Dependencies |
| --- | --- | --- | --- | --- | --- | --- | --- |
| core | `docs/core/` | TODO | `docs/core/CHANGELOG.md` | TODO | TODO | planned | TODO |

## 版本索引

完成一组功能并合并到 `dev` 后，使用版本工具在 `docs/VERSIONS.md` 中追加版本条目，例如 `v0.0.1 "创建项目模板"`。

## 说明

- 每个功能组目录维护自己的 `ENGINEERING_SPEC.md`、`CHANGELOG.md` 和可选 `GUIDE.md`。
- 具体变更编号只写入同一功能组的 `CHANGELOG.md`，不要复制进 BDD 主文档。
- 理论上一个功能组或一次变更使用单独工作分支，完成后合并到 `dev` 并删除工作分支。
- 可复用组件先登记到所在功能组的 Reusable Component Registry；跨功能组复用时，也在本索引中标注。
