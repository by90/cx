# BDD/TDD AI-Assisted Development Workflow

## Core idea

BDD defines the behavior and shared language. TDD proves the behavior with executable tests. AI coding agents are useful only when their work is constrained by durable documents and verification evidence.

The cx workflow uses this order:

1. Intake the user request.
2. Choose or create the target documentation set. Multi-feature projects use `docs/<feature-group>/ENGINEERING_SPEC.md` and the sibling `CHANGELOG.md`.
3. Update the target `CHANGELOG.md` with a `CHANGE-*` entry.
4. Update the target `ENGINEERING_SPEC.md` with behavior, main success scenarios, alternate scenarios, exception scenarios, architecture notes, task queue, and test matrix.
5. Write the expected failing test.
6. Run the narrow test and record the red failure.
7. Implement the smallest change.
8. Run tests until green.
9. Refactor only while keeping tests green.
10. Record verification evidence.
11. Search existing implementation, related skills, and registries to decide whether duplicated logic should become a reusable component.

## Why docs documentation sets

Many AI workflows generate a new spec, plan, or task file for every request. That looks organized for one task but becomes unsearchable across a long-lived project. cx makes every new piece of work enter an explicit `docs/` documentation set: small projects can keep one set, while larger projects split by feature group and use `docs/INDEX.md` as the index.

## Recommended prompt

```text
Use $cx-bdd-tdd. First choose or create the target docs documentation set, then update its ENGINEERING_SPEC.md and CHANGELOG.md. Derive main success scenarios, alternate scenarios, exception scenarios, and failing tests. Show the expected red failure, implement the smallest change, run validation, and record evidence. Do not create separate planning docs.
```

## Specialized prompts

For Python ML work, combine `$cx-bdd-tdd`, `$cx-pytorch-tdd`, and `$cx-ragged-tensor` when variable-length tensors are involved.

For desktop Rust UI work, combine `$cx-bdd-tdd`, `$cx-rust-ui`, and `$cx-progress-ui` when progress state or task monitoring is involved.

For final review, use `$cx-evidence` or explicitly spawn `cx-review` as a read-only subagent.
