---
name: cx-rust-tdd
description: 用于 Rust 代码实现和 TDD，包括 ownership-aware design、struct/enum/trait、Result 错误、cargo test、rustfmt、clippy 和高质量非 UI Rust 代码。
version: 0.1.0
---

# cx Rust 编码与 TDD

## 目的

在 `$cx-bdd` 已经定义行为后，用本 skill 处理 Rust 实现。它是通用 Rust 代码质量和 TDD skill，不是 UI 组件 skill。

## 必须执行的流程

1. 阅读 `BDD.md`、`ENGINEERING_SPEC.md`、`CHANGELOG.md` 和相关 Rust 模块。
2. 将一个 BDD ID 映射到一个最窄 Rust 测试。
3. 先写失败测试：可以使用 `#[test]`、`tests/` 下的集成测试，或用于公共 API 文档的 doc test。
4. 运行 `cargo test <filter>` 或项目中最窄命令，并记录 red failure。
5. 实现最小 Rust 改动。
6. 先运行最窄测试，再运行 `cargo test`。
7. 运行 `cargo fmt --check` 或 `cargo fmt`。
8. 可行时运行 `cargo clippy --all-targets --all-features`。
9. 只有测试 green 后才重构。
10. 记录验证证据。

## Rust 设计规则

- 用有名字的 `struct` 和 `enum` 表达领域状态。只要类型能表达不变量，就不要传松散 map、字符串状态或未验证 tuple。
- trait 用于稳定行为边界，不能用来掩盖不清楚的设计。
- 可恢复失败使用 `Result<T, E>` 和明确错误 enum。
- 生产路径避免 `unwrap`、`expect` 和 `panic!`，除非不变量局部、已证明并写明原因。
- 不要为了绕过 borrow checker 乱 `clone`。所有权必须有明确设计。
- 函数保持小，但不要拆成没有意义的空壳包装。
- 模块保持高内聚，公共 API 保持窄。
- 缺失用 `Option`，失败用 `Result`；不要用魔法字符串或哨兵值编码错误。
- unsafe 代码必须有 `SAFETY:` 注释，并围绕安全边界写测试。除非没有安全设计，否则不要新增 unsafe。

## 测试策略

- 纯逻辑优先在模块旁边用 `#[cfg(test)]` 单元测试。
- 跨模块公共流程使用 `tests/` 下的集成测试。
- 公共示例需要能编译时使用 doc test。
- 覆盖成功、边界、非法输入、错误传播和所有权敏感行为。
- 测试必须确定、快速。
- 优先真实小 fixture，只有外部边界才使用 test double。

## 输出

- BDD ID 到 Rust 测试的映射。
- 预期 red failure 命令和输出摘要。
- 最小 Rust 实现。
- `cargo test` 结果。
- 格式化和 clippy 结果，或未运行原因。
