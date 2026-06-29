# Use-Case-Driven TDD AI-Assisted Development Workflow

## Core Principle

The use-case document defines the main success scenario and branch scenarios. The task document defines one class or type-group boundary. The change document defines how AI should continue current work. TDD proves task behavior with executable tests.

## Standard Order

1. Use `$cx-workflow` to classify the task and create a visible todo list.
2. Ask the execution-mode question: finish documentation, tests, implementation, and validation directly, or ask after each task.
3. If the user does not explicitly choose per-task confirmation, default to direct completion.
4. Use `$cx-story` to read `docs/cx` project documents and the target scenario.
5. If unfinished changes exist, read `changes/` first and let them decide current work.
6. If adding a use case, branch, or task, update the use-case document, design document, or `tasks/`.
7. If adjusting an existing task, write a `changes/` document with timestamp, task id, task name, previous state, and next action.
8. Document completion is not a default stop point; continue with `$cx-tdd` and write the narrow failing test.
9. Implement one task's code file and one matching unit-test file when needed.
10. Run the narrowest validation and record command plus result.
11. Only per-task confirmation mode waits for user review after the task.

## Document Location

```text
docs/cx/00.project.md
docs/cx/01.create_user/00.use_case.md
docs/cx/01.create_user/00.design.md
docs/cx/01.create_user/tasks/01.write_user_entity/00.task.md
docs/cx/01.create_user/changes/20260629T120000-task01-write_user_entity.md
```

## Recommended Prompt

```text
Use $cx-workflow and $cx-story. Ask the execution-mode question before starting; if I do not choose per-task confirmation, default to completing documentation, tests, implementation, and validation directly. First check whether the target docs/cx scenario has unfinished changes. Then read 00.use_case.md, 00.design.md, and the current task document, use $cx-tdd to write the failing test, and implement the current task.
```

For Python ML work, combine `$cx-story`, `$cx-tdd`, and `$cx-pytorch-tdd`.

For Rust work, combine `$cx-story`, `$cx-tdd`, and `$cx-rust-tdd`.
