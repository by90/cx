# Use-Case-Driven AI-Assisted Development Workflow

## Core Principle

The use-case document defines the main success scenario plus conditional, alternate, and exception substeps attached to concrete main steps. The task document defines one class or type-group boundary. The change document defines how AI should continue current work. Default execution edits one production code file after the task document is complete; unit tests and TDD enter scope only when explicitly requested.

## Standard Order

1. Use `$cx-workflow` to classify the task and create a visible todo list.
2. Use one-task/one-code-file execution by default: after the current task document is complete, edit only that task's bound production code file.
3. Continue into another code file only when the user explicitly asks for multi-task continuation; wait after each task only when explicitly requested.
4. Use `$cx-story` to read `docs/cx` project documents and the target scenario.
5. If unfinished changes exist, read `changes/` first and let them decide current work.
6. If adding a use case, conditional substep, or task, update the use-case document, design document, or `tasks/`.
7. If adjusting an existing task, write a `changes/` document with timestamp, task id, task name, previous state, and next action.
8. After the task document is complete, implement that task's one production code file.
9. Do not create or edit unit tests by default; use `$cx-tdd` and one matching unit-test file only when TDD, unit tests, or failing tests are explicitly requested.
10. Run the narrowest validation and record command plus result.
11. Run `$cx-evidence` mandatory review after code completion; if review fails, keep the task incomplete and return to fixing.
12. After review passes, report and stop at the current code-file boundary by default.

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
Use $cx-workflow and $cx-story. First check whether the target docs/cx scenario has unfinished changes. Then read 00.use_case.md, 00.design.md, and the current task document. By default, complete the current task document and implement only the one production code file bound to that task. Do not create or edit unit tests by default. Use $cx-tdd only when I explicitly ask for TDD, unit tests, or failing tests. After code is written, run $cx-evidence review; if review fails, do not mark the task complete.
```

For Python ML work, use `$cx-story` by default; add `$cx-tdd` and `$cx-pytorch-tdd` only when tests are explicitly requested.

For Rust work, use `$cx-story` and `$cx-rust-tdd` by default; add `$cx-tdd` only when tests are explicitly requested.
