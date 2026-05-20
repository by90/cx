# docs/INDEX.md

本文件是 `docs/` 根目录的索引和说明。所有项目都按多个功能组组织，`docs/` 根目录只长期保留索引、说明和版本索引；具体研发文档放入各功能组目录。

## 文档布局

```text
docs/INDEX.md
docs/VERSIONS.md
docs/001_project_template/ENGINEERING_SPEC.md
docs/001_project_template/CHANGELOG.md
docs/001_project_template/GUIDE.md
docs/002_next_feature/ENGINEERING_SPEC.md
docs/002_next_feature/CHANGELOG.md
docs/002_next_feature/GUIDE.md
```

## 功能组索引

| Group ID | Folder | Goal | Changelog | BDD IDs | Reusable components | Status | Dependencies |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 001 | `docs/001_project_template/` | TODO | `docs/001_project_template/CHANGELOG.md` | TODO | TODO | planned | TODO |

## 版本索引

完成一组功能并合并到 `dev` 后，使用版本工具在 `docs/VERSIONS.md` 中追加版本条目，例如 `v0.0.1 "创建项目模板"`。

## 说明

- 每个功能组目录都必须使用三位序号、小写、下划线分隔的名字，并维护自己的 `ENGINEERING_SPEC.md`、`CHANGELOG.md` 和 `GUIDE.md`。
- 具体变更编号只写入同一功能组的 `CHANGELOG.md`，不要复制进 BDD 或研发主文档。
- 普通、非编程任务不要自行创建 BDD；不确定是否需要行为发现时先询问用户。
- 理论上一个功能组或一次变更使用单独工作分支，完成后合并到 `dev` 并删除工作分支。
- 可复用功能、类或组件先登记到所在功能组的 Reusable Capability Registry；跨功能组复用时，也在本索引中标注。
