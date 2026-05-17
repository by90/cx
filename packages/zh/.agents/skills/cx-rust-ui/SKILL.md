---
name: cx-rust-ui
description: 用于 Rust desktop apps、GPUI、gpui-component、UI state models、Render/RenderOnce components、event reducers 和 Rust component testing。
version: 1.0.0
---

# cx Rust / GPUI / gpui-component TDD

## 目的

用于 Rust 桌面 UI、GPUI 和 gpui-component 工作。将纯状态逻辑与渲染分离，这样行为可以先测试，再接 UI。

## 必须执行的流程

1. 阅读研发主文档和相关 BDD 场景。
2. 在 UI 渲染前先抽取纯状态、reducer、validation 和 command 逻辑。
3. 使用 Rust 内置测试机制为状态和事件处理编写单元测试，例如 `#[cfg(test)] mod tests` 和 `cargo test`。
4. 新增可复用 UI state、组件 API 或 reducer 前，先叠加 `$cx-common-module` 搜索已有组件和 registry。
5. 实现最小改动。
6. 可行时运行 `cargo fmt`、`cargo test` 和 `cargo clippy --all-targets --all-features`。

## GPUI/gpui-component 规则

- `Render` 和 `RenderOnce` 专注渲染。
- 尽量使用无状态 component elements。
- 由 view 持有状态，并将快照传给组件。
- 不要把异步副作用隐藏在渲染代码中。
- 按项目风格一致地使用 gpui-component primitives。
- 组件 API 保持小而可组合。

## 测试策略

单元测试状态转换、reducer、validation 和 command generation。只有纯状态无法证明的流程才增加集成测试。涉及持久化或数据读取时，优先使用真实但缩小的测试数据，例如小型 SQLite fixture；只在外部边界难以真实控制时少量使用 mock。不要把截图作为唯一正确性证据。
