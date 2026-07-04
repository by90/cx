# 多语言策略

## 建议

用一个 GitHub 仓库维护两个可安装语言包：

```text
packages/en
packages/zh
```

中英文包的 skill 名称和 agent 名称必须完全一致，并且都以 `cx-` 开头。语言只影响面向人的内容：description、instructions、templates、guides 和 examples。

## 同步顺序

本项目修改流程规则、技能说明、模板或示例时，先完成中文包，再同步英文包。中文包是规则源，英文包必须保持同构结构和同等约束。

## 文档语言强约束

目标项目只安装一种语言包。安装中文包时，cx 生成或维护的所有长期文档必须使用简体中文，包括 `00.项目说明.md`、`00.用例.md`、`00.设计.md`、任务文档、变更文档、实现计划和验证证据。人工智能代理在对话、说明、计划、总结、审查结论和证据记录中也必须使用完整中文表达，不得写成中英文混杂的句子。代码标识符、命令、接口名、库名和外部专名可以保留原文；保留英文时，必须在同句或相邻句用中文详细解释其含义、作用和当前上下文。

## 为什么不要同时安装两种语言

Codex 会从当前工作目录向仓库根目录扫描 `.agents/skills`。如果两种语言包使用相同 `name`，它们不会合并，可能同时出现在选择器中。这会造成歧义并浪费上下文，所以目标仓库只安装一种语言包。

## 命名稳定性

中英文包必须保持名称一致。当前 skill 名称包括：

- `$cx-workflow`
- `$cx-story`
- `$cx-tdd`
- `$cx-changelog`
- `$cx-version`
- `$cx-research`
- `$cx-pytorch-tdd`
- `$cx-pytorch-quick-hpo`
- `$cx-pytorch-full-hpo`
- `$cx-timeseries-modeling`
- `$cx-rust-tdd`
- `$cx-common-module`
- `$cx-review`
- `$cx-evidence`

一致名称让用户只写一套提示词、教程和自动化脚本，然后单独选择语言包。
