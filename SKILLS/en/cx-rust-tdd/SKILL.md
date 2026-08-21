---
name: cx-rust-tdd
description: Use with cx-tdd only when Rust TDD, unit tests, or failing tests are explicitly required. Adds one-to-one external tests that mirror src, cargo commands, a centralized real test-database fixture, and ownership, Result, and type checks.
version: 0.1.0
---

# cx Rust Test Supplement

## Boundary

This skill does not own general Rust implementation and does not redefine test-first steps. Execute `$cx-tdd` completely, then add these Rust rules to the same test cycle.

Without an explicit test requirement, do not use this skill and do not create, edit, or run Rust unit tests.

## Separate Tests From Production Code

- Production source must never contain `#[cfg(test)]`, inline `mod tests`, test functions, fixtures, test data, or test-only entrypoints. Test code belongs only under repository-root `tests/`, alongside `src/`.
- Mirror `src/` directories under `tests/` as closely as possible. `src/<subsystem>/foo.rs` maps only to `tests/<subsystem>/foo_test.rs`; `src/foo.rs` maps only to `tests/foo_test.rs`.
- Each tested source file has at most one matching `_test.rs` file. Do not cover several source files with one large test file or split one source file across arbitrarily named test files.
- `tests/common/` may contain only shared real-data fixtures and discovery entrypoints, never behavior tests for a source file. When Cargo cannot discover a nested test file automatically, use an explicit `[[test]]` path or a thin discovery entrypoint with no test logic; never move the test back into `src/`.
- External tests exercise the package's real public API. Do not add test-only `pub` visibility, bridges, conditional-compilation entrypoints, or duplicate source inclusion to reach private implementation. Verify unobservable private details through the public entrypoint that owns their behavior.

## Rust Test Tools

- Use Rust's built-in `#[test]` and standard test tools in the matching file under `tests/`; use doc tests when public examples must compile. Do not introduce another test framework unless the current user request explicitly requires it.
- In the failing stage, run the narrowest `cargo test <filter>` and record the target failure. In the passing stage, rerun the same command before broader `cargo test` when needed.
- After Rust edits, run `cargo fmt --check` and, when practical, `cargo clippy --all-targets --all-features`.
- Test success values, error enums, boundary values, and ownership-sensitive behavior. Every assertion follows `$cx-tdd` constant-right-hand-side and ordered-collection sampling rules.
- Do not use `unwrap`, `expect`, or `panic!` to hide production failures. Match an explicit `Result` or error enum when failure behavior must be tested.

## Real Test Data

- Data-related Rust tests use real records from the test database. Do not fabricate replacement data inside test files.
- Centralize database opening, fixed-range reads, and shared-domain-object construction in one common test-fixture module, such as `tests/common/mod.rs` or the repository's existing equivalent.
- Use `std::sync::OnceLock` or the repository's existing one-time initialization mechanism so each test process reads once. Test files reuse shared objects and never reopen the database or reconstruct the same data independently.
- If the test database or required records are missing, report the missing prerequisite instead of substituting an in-memory database, fake repository, or mocked data-access layer.
- Unless the current user request explicitly requires them, do not use mocks, test doubles, or fake repository tests.

## Review Gates

1. Search all of `src/`; any production file containing test code fails the Rust test deliverable.
2. Check the path and name mapping for every test file in scope. Correct any many-to-one, one-to-many, or cross-source large test file.
3. Confirm `cargo test` discovers the targets and production interfaces were not expanded for tests.

## Output

In addition to the `$cx-tdd` record, report the source-to-test mapping, the search proving `src/` contains no test code, the narrow `cargo test` command, broader test result, shared test-database entry, `cargo fmt --check` result, and the `clippy` result or reason it was not run.
