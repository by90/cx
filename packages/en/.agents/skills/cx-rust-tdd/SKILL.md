---
name: cx-rust-tdd
description: Use together with cx-tdd only when Rust TDD, unit tests, or failing tests are explicitly required. Adds only Rust built-in tests, cargo commands, a centralized real test-database fixture, and ownership, Result, and type checks.
version: 0.1.0
---

# cx Rust Test Supplement

## Boundary

This skill does not own general Rust implementation and does not redefine test-first steps. Execute `$cx-tdd` completely, then add these Rust rules to the same test cycle.

Without an explicit test requirement, do not use this skill and do not create, edit, or run Rust unit tests.

## Rust Test Tools

- Use Rust's built-in `#[cfg(test)]` and `#[test]` for pure module behavior, integration tests under `tests/` for cross-module public entrypoints, and doc tests when public examples must compile.
- In the failing stage, run the narrowest `cargo test <filter>` and record the target failure. In the passing stage, rerun the same command before broader `cargo test` when needed.
- After Rust edits, run `cargo fmt --check` and, when practical, `cargo clippy --all-targets --all-features`.
- Test success values, error enums, boundary values, and ownership-sensitive behavior. Every assertion follows `$cx-tdd` constant-right-hand-side and ordered-collection sampling rules.
- Do not use `unwrap`, `expect`, or `panic!` to hide production failures. Match an explicit `Result` or error enum when failure behavior must be tested.

## Real Test Data

- Data-related Rust tests must use real records from the test database. Do not fabricate replacement data inside test modules.
- Centralize database opening, fixed-range reads, and shared-domain-object construction in one common test-fixture module, such as `tests/common/mod.rs` or the repository's existing equivalent.
- Use `std::sync::OnceLock` or the repository's existing one-time initialization mechanism so each test process reads once. Test modules reuse shared objects and never reopen the database or reconstruct the same data independently.
- If the test database or required records are missing, report the missing prerequisite instead of substituting an in-memory database, fake repository, or mocked data-access layer.
- Unless the current user request explicitly requires them, do not use mocks, test doubles, or fake repository tests.

## Output

In addition to the `$cx-tdd` record, report the narrow `cargo test` command, broader test result, shared test-database entry, `cargo fmt --check` result, and the `clippy` result or reason it was not run.
