---
name: cx-rust-tdd
description: Use for Rust code implementation, optional explicit TDD, ownership-aware design, structs/enums/traits, Result-based errors, cargo fmt, clippy, cargo test, GPUI/macOS real-device checks, and high-quality Rust code. Create unit or failing tests only when explicitly requested.
version: 0.1.0
---

# cx Rust Code And Explicit Tests

## Purpose

Use this skill for Rust implementation work after the current `docs/cx` task is known. It is a general Rust code-quality skill; enter test-first flow only when the current request, task document, or change document explicitly asks for TDD, unit tests, or failing tests. For GPUI/macOS desktop UI work, it adds real-device verification discipline without replacing a dedicated UI component design process.

## Required Workflow

1. Confirm that the current task edits one Rust production code file; if a second code file is needed, split another task first.
2. Read the target use-case document, design document, current task document, current change document, and the relevant Rust modules.
3. By default, do not create or edit Rust unit tests; only when tests are explicitly requested, map the current class/type measure to one narrow Rust test.
4. When tests are explicitly requested, write the failing test first using `#[test]`, integration tests under `tests/`, or doc tests when the behavior is public API documentation.
5. When tests are explicitly requested, run `cargo test <filter>` or the narrowest project command and record the red failure.
6. Implement the smallest Rust change.
7. When tests are explicitly requested, run the narrow test and then `cargo test` as needed; otherwise run project-required build, formatting, or static checks.
8. Run `cargo fmt --check` or `cargo fmt`.
9. Run `cargo clippy --all-targets --all-features` when practical.
10. Refactor only after verification passes.
11. After code and required verification are done, run `$cx-evidence` mandatory review. Focus on docs agreement, duplication smells, full Rust type modeling, minimal implementation, and business semantics.
12. If review fails, do not mark the task complete; fix implementation or docs, then rerun verification and review.
13. Record verification evidence and review decision.

## Minimal Implementation Discipline

Iron rule: absolutely no unmaintainable pile-up code.

- Default to the least code that satisfies the current need; do not frameworkize, generalize, or abstract early.
- Keep file, type, function, and variable names short and clear; avoid sentence-like identifiers, and extract responsibilities or reuse domain terms when names grow too long.
- Do not create functions, classes, constants, or validators for one-line forwarding, one-off logic, or flows without real reuse value.
- Unless business rules explicitly require it, do not hide exceptions, silently fall back, or turn errors that would harm the product into defaults, empty results, skipped records, fake successful retries, or warnings; during development, let these errors stop execution.
- Use a simple test: if the same bug shipped to the product would cause a problem, it must surface as a failure. Only add explicit handling when the business requires degradation, recovery, or user-visible guidance, and cover that path with tests.
- Do not add validation that only "looks safer" but is not required, such as filename allowlists, path validity checks, extra AST scans, or duplicate config rule checks.
- Do not put per-item data-validity checks inside large loops, training loops, hot paths, or batch processing to fall back or slow the system down. Handle data validity at entrypoints, data preparation, test fixtures, or separate diagnostic tasks, and never use those checks to replace real failures.
- By default, do not catch or wrap exceptions yourself; when the underlying library already gives clear exceptions, let the original exception propagate.
- Do not create custom exception types unless callers truly need to distinguish that exception and already have a clear handling path.
- Prefer expressing defaults through function or constructor parameters; do not promote simple paths, filenames, or one-off defaults to module-level constants.
- Keep only the public API needed for current behavior; do not add debug entrypoints, memory validation entrypoints, scan entrypoints, or interfaces for future needs.
- During project development, never keep compatibility interfaces, old entrypoints, aliases, adapter layers, bridge functions, or new/old coexistence branches for old code. Do not optimize for old/new code compatibility; remove all unused code, old paths, obsolete tests, and stale documents after the change.
- Let YAML, JSON, database, filesystem, and similar parsing errors be handled by the corresponding library or standard library by default; add semantic checks only when business rules explicitly require them.
- Every helper function must satisfy all of these: clear name, reduces duplication or isolates real complexity, and either has more than one call site or significantly improves readability. Otherwise inline it.
- Refactoring should delete code, reduce branches, and shrink the public surface, not move logic into more small functions.

## Rust Design Rules

- Rust code must also follow comprehensive comments: source files need file-level explanations, structs/enums/traits need responsibility explanations, functions need responsibility explanations, and every line of business code needs an adjacent intent comment; only blank lines, pure formatting lines, or repeated structural lines may omit comments.
- Model domain state with named `struct` and `enum` types. Do not pass loose maps, stringly typed state, or unvalidated tuples when a type can express the invariant.
- Use traits for stable behavior boundaries, not as a substitute for unclear design.
- Prefer `Result<T, E>` and explicit error enums for recoverable failures.
- Avoid `unwrap`, `expect`, and `panic!` in production paths unless the invariant is local, proven, and documented.
- Avoid cloning to appease the borrow checker. Decide ownership deliberately.
- Keep functions small, direct, and minimal. Keep files cohesive and reasonably sized. Do not create bloated, long, hard-to-maintain code, and do not fragment logic into meaningless wrappers.
- Keep modules cohesive and public APIs narrow.
- Any potentially reusable feature, class, or logic must first invoke `$cx-common-module` to search existing implementation and design the public entrypoint.
- Use `Option` for absence and `Result` for failure; do not encode errors as magic strings or sentinel values.
- Document unsafe code with `SAFETY:` comments and tests around the safe boundary. Do not add unsafe code unless there is no safe design.

## Test Strategy

- When unit tests are explicitly requested, test pure logic close to the module with `#[cfg(test)]`.
- Use integration tests for public workflows across modules.
- Use doc tests for public examples that should compile.
- Cover success, boundary, invalid input, error propagation, and ownership-sensitive behavior.
- Keep tests deterministic and fast.
- Prefer real small fixtures over mocks. Use test doubles only at external boundaries.

## GPUI/macOS Real-Device Checks

- After Rust/GPUI desktop UI changes, run explicitly requested unit tests, `cargo fmt`, and `cargo clippy` as usual, then package, install, or launch the real app with the project workflow and observe the result with screenshots or Computer Use.
- macOS Accessibility authorization must cover both the automation host and the tested app; common entries include `Codex`, `Codex Computer Use`, the tested `.app`, and the terminal or runtime host that launches click scripts. After changing permissions, restart the automation host and tested app first.
- GPUI content buttons are often not fully exposed as `AXButton` nodes in the Accessibility tree; use `System Events` first for menu bar items, window controls, and page-menu actions, but do not assume it can locate every GPUI content-area button.
- Before clicking GPUI content, save a screenshot under the project `temp/` directory, then confirm window logical coordinates, display bounds, and Retina scaling; screenshot pixel coordinates are not direct `CGEvent` logical points.
- When `osascript click at {x, y}` is unreliable for GPUI content, use CoreGraphics HID events instead: call `CGWarpMouseCursorPosition(point)`, then post `mouseMoved`, `leftMouseDown`, and `leftMouseUp` events to `.cghidEventTap`.
- `postToPid(pid)` is only a supporting probe that events can reach the process; the final judgment must come from screenshot changes and UI behavior after a global HID click.
- Treat all coordinates as temporary values for the current window, screen, and scale state; recalibrate after window-size changes, system-scale changes, multi-display layout changes, notification banners, or sidebar state changes.
- Temporary screenshots, coordinate calibration images, installers, and UI verification artifacts must live in project `temp/` or the project-defined temporary directory and must not enter source control.

Use this minimal HID click template only after replacing `point` with the current global logical point calibrated from screenshots:

```bash
swift - <<'SWIFT'
import CoreGraphics
import Foundation

let point = CGPoint(x: 247, y: 134)
CGWarpMouseCursorPosition(point)
Thread.sleep(forTimeInterval: 0.12)

let source = CGEventSource(stateID: .combinedSessionState)
for type in [CGEventType.mouseMoved, .leftMouseDown, .leftMouseUp] {
    let event = CGEvent(
        mouseEventSource: source,
        mouseType: type,
        mouseCursorPosition: point,
        mouseButton: .left
    )
    event?.post(tap: .cghidEventTap)
    Thread.sleep(forTimeInterval: 0.08)
}
SWIFT
```

## Output

- Current task to Rust code mapping, and test mapping only when tests are explicitly requested.
- Expected red failure command and output summary when tests are explicitly requested; otherwise state that no unit test was created.
- Minimal Rust implementation.
- `cargo test` result.
- Formatting and clippy result or a recorded reason they were not run.
- `$cx-evidence` review decision. FAIL means the task remains incomplete.
- For GPUI/macOS UI work, real app launch method, Accessibility permission status, click method, screenshot path, and observation conclusion.
