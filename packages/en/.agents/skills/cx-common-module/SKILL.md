---
name: cx-common-module
description: Use to discover and design registered common packages, shared utilities, reusable features, reusable classes, stable interfaces, and common data structures. Before implementation, read docs/cx/docs topic documents, then search source and real callers so existing common capabilities are not ignored and duplicated.
version: 0.1.0
---

# cx Common-Capability Reuse

## Purpose

Find project capabilities before adding implementation. Every stable common capability stays small and has an independent topic document under `docs/cx/docs/`.

## Required discovery order

1. Read `docs/cx/docs/00.index.md` and relevant topic documents.
2. Obtain the common package, public interface, source location, usage, and scope from the topic document.
3. Search source, the current use case, design, original task, and real callers to confirm that documentation and implementation agree.
4. Search adjacent domains for an existing equivalent structure or directly reusable entry.
5. Record candidates, adoption or rejection reasons, and caller impact.
6. Design a new entry only when no existing capability satisfies the current goal.

Missing documentation does not prove that a capability is absent. Search source anyway. When a stable capability lacks a topic document, use `$cx-doc` to document its current entry first.

## Calling model

Before adding or changing a common capability, state:

```text
Problem solved:
Topic document:
Public entry:
Normal usage:
Special-case entry:
Instance or state lifecycle:
State source:
Real callers:
Error behavior:
Verification:
Non-goals:
```

Reject an abstraction unless it hides real complexity, reduces caller knowledge, has multiple real callers or isolates stable error-prone behavior, and cannot be expressed directly through the underlying structure or library.

## Current documentation

- Every common package and stable public interface has one numbered topic document under `docs/cx/docs/`.
- The topic document states the current problem, entry, inputs, outputs, constraints, shortest usage, and verification.
- Rewrite the same topic document when direction changes. Never preserve migration history.
- A package-local note, when unavoidable, only links to the topic document and shows the shortest entry. It does not duplicate details.

## Implementation discipline

- Use the least code that satisfies the current goal. Do not pre-build frameworks or compatibility layers.
- Keep only the latest public entry and callers. Delete old interfaces, aliases, adapters, bridges, compatibility parameters, compatibility configuration, compatibility paths, old behavior, and related documentation.
- Unless the user explicitly requests a specific validation or error behavior in the current request, do not add validation that raises an error and do not catch, translate, wrap, swallow, skip, or fall back from errors. Let the original error stop execution.
- Use explicit objects or equivalent types for state, lifecycle, and invariants.
- Put defaults in function signatures or configuration objects.
- Remove entries with no real caller, no complexity reduction, or test-only purpose.

## Required output

- Topic documents read.
- Search evidence and candidate comparison.
- Decision to reuse or add an entry, with reasons.
- Current topic document and source entry.
- Verification.
- Unified `$cx-review` decision.
