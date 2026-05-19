# BDD/TDD AI-Assisted Development Workflow

## Core idea

BDD defines the behavior and shared language. TDD proves the behavior with executable tests. AI coding agents are useful only when their work is constrained by durable documents and verification evidence.

The cx workflow uses this order:

1. Intake the user request.
2. Create or switch to a dedicated branch for this feature group before changing project files.
3. Choose or create the target ordered feature folder, such as `docs/1.Configuration System/`.
4. Update the target `BDD.md` with business rules, main success scenarios, alternate scenarios, and exception scenarios.
5. Update the target `CHANGELOG.md` with a `CHANGE-*` entry.
6. Update the target `ENGINEERING_SPEC.md` with architecture notes, task queue, and test matrix links back to BDD IDs.
7. Write the expected failing test.
8. Run the narrow test and record the red failure.
9. Implement the smallest change.
10. Run tests until green.
11. Refactor only while keeping tests green.
12. Record verification evidence.
13. Search existing implementation, related skills, and registries to decide whether duplicated logic should become a reusable component.
14. Merge the completed feature-group branch into `dev`; release handoff from `dev` to `main` happens only after user version confirmation.

## Why docs documentation sets

Many AI workflows generate a new spec, plan, or task file for every request. That looks organized for one task but becomes unsearchable across a long-lived project. cx makes every new piece of work enter an explicit `docs/` documentation set: small projects can keep one set, while larger projects split by feature group and use `docs/INDEX.md` as the index.

## Recommended prompt

```text
Use $cx-bdd and $cx-tdd. First create or switch to the feature-group branch, then choose or create the ordered feature folder and update its BDD.md, ENGINEERING_SPEC.md, and CHANGELOG.md. Derive main success scenarios, alternate scenarios, exception scenarios, and failing tests. Show the expected red failure, implement the smallest change, run validation, record evidence, and merge the completed feature branch to dev. Do not create separate planning docs.
```

## Specialized prompts

For Python ML work, combine `$cx-bdd`, `$cx-tdd`, and `$cx-pytorch-tdd`.

For Rust work, combine `$cx-bdd`, `$cx-tdd`, and `$cx-rust-tdd`.

For final review, use `$cx-evidence` or explicitly spawn `cx-review` as a read-only subagent.
