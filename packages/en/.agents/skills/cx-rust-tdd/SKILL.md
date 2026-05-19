---
name: cx-rust-tdd
description: Use for Rust code implementation and TDD, including ownership-aware design, structs/enums/traits, Result-based errors, cargo test, rustfmt, clippy, and high-quality non-UI Rust code.
version: 1.0.0
---

# cx Rust Code And TDD

## Purpose

Use this skill for Rust implementation work after behavior is defined by `$cx-bdd`. It is a general Rust code-quality and TDD skill, not a UI component skill.

## Required Workflow

1. Read `BDD.md`, `ENGINEERING_SPEC.md`, `CHANGELOG.md`, and the relevant Rust modules.
2. Map one BDD ID to one narrow Rust test.
3. Write the failing test first using `#[test]`, integration tests under `tests/`, or doc tests when the behavior is public API documentation.
4. Run `cargo test <filter>` or the narrowest project command and record the red failure.
5. Implement the smallest Rust change.
6. Run the narrow test, then `cargo test`.
7. Run `cargo fmt --check` or `cargo fmt`.
8. Run `cargo clippy --all-targets --all-features` when practical.
9. Refactor only after tests are green.
10. Record verification evidence.

## Rust Design Rules

- Model domain state with named `struct` and `enum` types. Do not pass loose maps, stringly typed state, or unvalidated tuples when a type can express the invariant.
- Use traits for stable behavior boundaries, not as a substitute for unclear design.
- Prefer `Result<T, E>` and explicit error enums for recoverable failures.
- Avoid `unwrap`, `expect`, and `panic!` in production paths unless the invariant is local, proven, and documented.
- Avoid cloning to appease the borrow checker. Decide ownership deliberately.
- Keep functions small, but do not fragment logic into meaningless wrappers.
- Keep modules cohesive and public APIs narrow.
- Use `Option` for absence and `Result` for failure; do not encode errors as magic strings or sentinel values.
- Document unsafe code with `SAFETY:` comments and tests around the safe boundary. Do not add unsafe code unless there is no safe design.

## Test Strategy

- Unit-test pure logic close to the module with `#[cfg(test)]`.
- Use integration tests for public workflows across modules.
- Use doc tests for public examples that should compile.
- Cover success, boundary, invalid input, error propagation, and ownership-sensitive behavior.
- Keep tests deterministic and fast.
- Prefer real small fixtures over mocks. Use test doubles only at external boundaries.

## Output

- BDD ID to Rust test mapping.
- Expected red failure command and output summary.
- Minimal Rust implementation.
- `cargo test` result.
- Formatting and clippy result or a recorded reason they were not run.
