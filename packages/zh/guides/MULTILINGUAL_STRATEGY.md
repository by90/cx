# 多语言策略

## 建议

用一个 GitHub 仓库维护两个可安装语言包：

```text
packages/en
packages/zh
```

中英文包的 skill 名称和 agent 名称必须完全一致，并且都以 `cx-` 开头。语言只影响面向人的内容：description、instructions、templates、guides 和 examples。

## 为什么不要把两种语言同时安装到目标项目

Codex 会从当前工作目录向仓库根目录扫描 `.agents/skills`。如果两个 skill 使用相同 `name`，它们不会合并，可能同时出现在选择器中。这会造成歧义并浪费上下文。所以目标仓库只安装一种语言包。

## GitHub README 做法

仓库根目录放简洁的 `README.md`，并链接到 `README.zh-CN.md`。GitHub 会把根目录 README 作为主要访问页展示；使用相对链接可以保证仓库 clone 后仍然可用。

## 稳定命名

除非发布大版本，否则保持这些名称不变：

- `$cx-bdd-tdd`
- `$cx-changelog`
- `$cx-pytorch-tdd`
- `$cx-ragged-tensor`
- `$cx-progress-ui`
- `$cx-rust-ui`
- `$cx-common-module`
- `$cx-evidence`

稳定名称让用户只写一次提示词、教程和自动化脚本，然后单独选择语言包。
