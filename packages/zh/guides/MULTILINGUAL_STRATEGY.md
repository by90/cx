# 多语言策略

## 建议

用一个 GitHub 仓库维护两个可安装语言包：

```text
packages/en
packages/zh
```

中英文包的 skill 名称和 agent 名称必须完全一致，并且都以 `cx-` 开头。语言只影响面向人的内容：description、instructions、templates、guides 和 examples。

## 文档语言强约束

目标项目只安装一种语言包。安装中文包时，cx 生成或维护的所有长期文档必须使用简体中文，包括 BDD、研发主文档、变更记录、索引、实现计划、测试矩阵和验证证据。代码标识符、命令、API 名称和外部英文专名可以保留原文。

## 为什么不要把两种语言同时安装到目标项目

Codex 会从当前工作目录向仓库根目录扫描 `.agents/skills`。如果两个 skill 使用相同 `name`，它们不会合并，可能同时出现在选择器中。这会造成歧义并浪费上下文。所以目标仓库只安装一种语言包。

## GitHub README 做法

仓库根目录放简洁的 `README.md`，并链接到 `README.zh-CN.md`。GitHub 会把根目录 README 作为主要访问页展示；使用相对链接可以保证仓库 clone 后仍然可用。

## 命名稳定性

中英文包必须保持名称一致。pre-1.0 阶段接口和工作流变化使用 minor，主版本号保持 `0`；`1.0.0` 之后，不兼容重命名才需要 major：

- `$cx-bdd`
- `$cx-tdd`
- `$cx-changelog`
- `$cx-version`
- `$cx-research`
- `$cx-pytorch-tdd`
- `$cx-rust-tdd`
- `$cx-common-module`
- `$cx-evidence`

一致名称让用户只写一次提示词、教程和自动化脚本，然后单独选择语言包。
