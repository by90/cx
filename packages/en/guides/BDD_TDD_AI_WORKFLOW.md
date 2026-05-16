# BDD/TDD AI-Assisted Development Workflow

## Core idea

BDD defines the behavior and shared language. TDD proves the behavior with executable tests. AI coding agents are useful only when their work is constrained by durable documents and verification evidence.

The cx workflow uses this order:

1. Intake the user request.
2. Update `docs/CHANGELOG.md` with a `CHANGE-*` entry.
3. Update `docs/ENGINEERING_SPEC.md` with behavior, BDD scenarios, architecture notes, task queue, and test matrix.
4. Write the expected failing test.
5. Run the narrow test and record the red failure.
6. Implement the smallest change.
7. Run tests until green.
8. Refactor only while keeping tests green.
9. Record verification evidence.
10. Consider whether duplicated logic should become a common module.

## Why one engineering document

Many AI workflows generate a new spec, plan, or task file for every request. That looks organized for one task but becomes unsearchable across a long-lived project. cx keeps a single engineering spec with stable sections so new work strengthens the existing document instead of creating document trash.

## Recommended prompt

```text
Use $cx-bdd-tdd. First update docs/ENGINEERING_SPEC.md and docs/CHANGELOG.md. Derive BDD scenarios and failing tests. Show the expected red failure, implement the smallest change, run validation, and record evidence. Do not create separate planning docs.
```

## Specialized prompts

For Python ML work, combine `$cx-bdd-tdd`, `$cx-pytorch-tdd`, and `$cx-ragged-tensor` when variable-length tensors are involved.

For desktop Rust UI work, combine `$cx-bdd-tdd`, `$cx-rust-ui`, and `$cx-progress-ui` when progress state or task monitoring is involved.

For final review, use `$cx-evidence` or explicitly spawn `cx-review` as a read-only subagent.
