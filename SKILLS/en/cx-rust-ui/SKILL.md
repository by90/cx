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
3. Write Rust unit tests for state and event handling.
4. Implement the smallest change.
5. Run `cargo fmt`, `cargo test`, and `cargo clippy --all-targets --all-features` when practical.

## GPUI/gpui-component rules

- Keep `Render` and `RenderOnce` focused on rendering.
- Prefer stateless component elements when possible.
- Let views own state and pass snapshots to components.
- Avoid hiding async side effects inside rendering code.
- Use gpui-component primitives consistently with project style.
- Keep component APIs small and composable.

## Testing strategy

Unit test state transitions, reducers, validation, and command generation. Add integration tests only for flows that cannot be proven through pure state. Do not rely on screenshots as the only proof of correctness.
