---
name: cx-rust-ui
description: Use for Rust desktop apps, GPUI, gpui-component, UI state models, Render or RenderOnce components, event reducers, and Rust component testing.
version: 1.0.0
---

# cx Rust / GPUI / gpui-component TDD

## Purpose

Use this for Rust desktop UI work with GPUI and gpui-component. Keep pure state logic separate from rendering so behavior can be tested before UI wiring.

## Required workflow

1. Read the engineering spec and related BDD scenarios.
2. Extract pure state, reducers, validation, and command logic before UI rendering.
3. Use Rust's built-in test mechanism for state and event handling, such as `#[cfg(test)] mod tests` and `cargo test`.
4. Before adding reusable UI state, component APIs, or reducers, add `$cx-common-module` and search existing components and registries.
5. Implement the smallest change.
6. Run `cargo fmt`, `cargo test`, and `cargo clippy --all-targets --all-features` when practical.

## GPUI/gpui-component rules

- Keep `Render` and `RenderOnce` focused on rendering.
- Prefer stateless component elements when possible.
- Let views own state and pass snapshots to components.
- Avoid hiding async side effects inside rendering code.
- Use gpui-component primitives consistently with project style.
- Keep component APIs small and composable.

## Testing strategy

Unit test state transitions, reducers, validation, and command generation. Add integration tests only for flows that cannot be proven through pure state. When persistence or data loading is involved, prefer real but reduced test data, such as a small SQLite fixture. Use mocks sparingly, only for external boundaries that cannot be controlled realistically. Do not rely on screenshots as the only proof of correctness.
