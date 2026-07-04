---
name: cx-common-module
description: Use for code duplication, shared utilities, reusable features, reusable classes, reusable components, component extraction, API design, indexed-series-like data structures, and deciding whether repeated implementation logic should become common modules.
version: 0.1.0
---

# cx Reusable Feature, Reusable Class, And Common Module Extraction

## Language Rules

- Use the package language for conversations, explanations, plans, summaries, review decisions, verification evidence, and cx documents. Do not mix languages inside prose fragments or term lists.
- In Chinese-package work, if an English identifier, command, path, API name, library, protocol, standard, proper name, or ambiguity-sensitive term must remain in English, explain its meaning, role, and local context in Chinese in the same sentence or an adjacent sentence. In English-package work, explain unavoidable non-English terms in English.

## Purpose

Turn repeated logic, stable data structures, reusable classes, generic capabilities, test harnesses, and UI state models into small, stable, verifiable reusable capabilities. AI-assisted coding often creates similar code in multiple places; this skill stops that drift by requiring search, calling-model design, API design, migration planning, and verification when duplication becomes meaningful.

## Minimal Implementation Discipline

Iron rule: absolutely no unmaintainable pile-up code. This applies to source code, tests, scripts, tools, examples, and workflow-generated code; common modules cannot use "reuse", "stability", or "future extension" as reasons to bloat.

- Default to the least code that satisfies the current need; do not frameworkize, generalize, or abstract early. Prove real call sites before extracting a functional entrypoint.
- Stable infrastructure starts as one field group, one constructor, and the fewest public methods. If callers can use arrays, tensors, standard slicing, standard-library errors, configuration default parameters, or explicit construction directly, do not wrap it.
- If a public class or public function adds protocol inheritance, convenience wrappers, clone methods, rebuild methods, padding methods, negative-index compatibility, fallback validation, debug entrypoints, or future-extension entrypoints for completeness, delete them unless the current calling model requires them.
- Keep file, class, method, and variable names short and clear; avoid sentence-like identifiers, and extract responsibilities or reuse domain terms when names grow too long.
- Do not create functions, classes, constants, or validators for one-line forwarding, one-off logic, or flows without real reuse value.
- Unless business rules explicitly require it, do not hide exceptions, silently fall back, or turn errors that would harm the product into defaults, empty results, skipped records, fake successful retries, or warnings; during development, let these errors stop execution.
- Use a simple test: if the same bug shipped to the product would cause a problem, it must surface as a failure. Only add explicit handling when the business requires degradation, recovery, or user-visible guidance, and cover that path with tests.
- Do not add validation that only "looks safer" but is not required, such as filename allowlists, path validity checks, extra AST scans, or duplicate config rule checks.
- Do not put per-item data-validity checks inside large loops, training loops, hot paths, or batch processing to fall back or slow the system down. Handle data validity at entrypoints, data preparation, test fixtures, or separate diagnostic tasks, and never use those checks to replace real failures.
- By default, do not catch or wrap exceptions yourself; when the underlying library already gives clear exceptions, let the original exception propagate.
- Do not create custom exception types unless callers truly need to distinguish that exception and already have a clear handling path.
- Prefer expressing defaults through function or constructor parameters. Configuration defaults should be written directly as default parameters, for example `path=Config.default_config_file()` or `batch_size=config.train.batch_size`; the function body stores the parameter on a same-named field, for example `self.batch_size = batch_size`.
- Keep only the functional entrypoint needed for current behavior; do not add debug entrypoints, memory validation entrypoints, scan entrypoints, or interfaces for future needs.
- Let YAML, JSON, database, filesystem, and similar parsing errors be handled by the corresponding library or standard library by default; add semantic checks only when business rules explicitly require them.
- Every helper function must satisfy all of these: clear name, reduces duplication or isolates real complexity, and either has more than one call site or significantly improves readability. Otherwise inline it.
- A generic capability, reusable feature, or reusable class should first abstract the functional entrypoint, call style, lifecycle, state source, and test isolation; do not first abstract one-off file reads, one-off validation, single-field conversion, or future-maybe internal steps.
- Common-module review must ask whether the code can be deleted first. Behavior callers can express directly with arrays, tensors, standard slicing, constructors, configuration default parameters, or library-native errors does not belong in a common module.
- Refactoring should delete code, reduce branches, and shrink the public surface, not move logic into more small functions.

## Calling Model Gate

Before adding or changing a generic capability, reusable feature, reusable class, shared tool, or stable API, write down:

```text
Public entrypoint:
Normal call style:
Special-case entrypoint:
Instance or state lifecycle:
State source:
How verification covers all source call sites:
readme functional entrypoint section:
Non-goals:
```

The abstraction boundary must answer four questions:

1. Does this abstraction hide caller complexity, or create internal complexity?
2. Does the caller need to know one less thing?
3. When adding a peer capability, config section, field, or data source, can we change data declarations rather than control-flow code?
4. Does a helper have at least two real call sites, or truly isolate real complexity?
5. Does this common package include a package-local `readme.md` that explains functional entrypoints and usage?

If the answers do not support abstraction, inline the logic or keep the direct implementation.

## Reuse Discovery

Before adding a new abstraction, search:

1. The current project's `src/`, `tests/`, `docs/cx`, and the target scenario's design document.
2. Enabled related workflow skills such as `$cx-pytorch-tdd`, `$cx-rust-tdd`, `$cx-tdd`, and this skill.
3. Existing projects or prior implementations explicitly mentioned by the user, such as `IndexedSeries` in `rise202604`.
4. Adjacent structures with the same shape, such as indexed series, packed tensor batches, ragged tensors, time-window datasets, or GPUI state reducers.

Record candidates, accept/reject reasons, and migration impact. Do not add a reusable feature, reusable class, or reusable component without search evidence.

## Extract when

Extract a generic capability, reusable class, or common module when at least one is true:

- The same logic appears in two or more places.
- A behavior is important enough to have its own conditional substep, separate use case, or task.
- The logic crosses project areas, such as training and UI.
- The logic is error-prone: indexed series, tensor padding, masks, progress synchronization, cancellation, metrics, checkpoint paths, or UI state reducers.
- A data structure already expresses a stable domain concept, such as grouped long series, window indices, packed batches, state reducers, or test data fixtures.

Do not extract when the abstraction is speculative and has only one unclear use.

## Required output

- Search evidence and candidate comparison.
- Public API proposal with functional entrypoint, normal call style, special-case entrypoint, lifecycle, state source, inputs, outputs, error policy, and a minimal example.
- Package-local `readme.md` that lists functional entrypoints and usage; do not list instance config sections, internal fields, or implementation steps as functional entrypoint documentation.
- Verification approach, preferably covering real small data and edge cases; use tests first only when unit tests or TDD are explicitly requested.
- Backward-compatible migration plan describing which call sites move and which stay unchanged.
- Reusable capability notes in the target `docs/cx` design document.
- Task or change document updates for the verification that proves the reusable capability; record test mapping only when unit tests are explicitly requested.
- `$cx-review` decision after the deliverable is produced, especially whether duplication smells were removed without over-abstracting or adding extra parameter passing, plus `$cx-evidence` evidence review before handoff.

## Code Constraints

- Any reusable-capability code or explicitly requested tests added or edited by this skill must follow comprehensive comments: file-level explanations must state file purpose and main classes, functions, or test targets; classes/types need responsibility explanations; functions and test methods must explain parameter meanings and return values or explicitly say there is no return value; every line of business code and test business logic needs an adjacent intent comment.
- Generic capabilities, reusable classes, reusable components, and common modules must be minimal, stable, and low-coupling. Do not abstract for its own sake, and do not copy repeated logic into multiple similar implementations.
- Python reusable capabilities should express default behavior with type annotations and default parameters. Configuration defaults should be written directly as default parameters, for example `path=Config.default_config_file()` or `batch_size=config.train.batch_size`; the function body stores the parameter on a same-named field, for example `self.batch_size = batch_size`. Do not stack long `None` or parameter-case branches inside `__init__`.
- Public APIs must use explicit object-oriented design or static interfaces. Do not use `getattr`, `setattr`, `delattr`, monkey-patching, dynamic injection, or stringly typed dispatch by default.

## Registry Fields

```text
Capability | Purpose | Public API | Owners/Callers | Tests | Migration notes
```

## Initial module priorities

1. `indexed_series` or `indexed_tensor_series`: long-series wrappers indexed by category, entity, or time window.
2. `lightning_test_harness`.
3. Project-specific component libraries that already have a README and tests.
