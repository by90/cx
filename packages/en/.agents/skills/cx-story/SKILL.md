---
name: cx-story
description: Use for use-case-driven story discovery, main success scenario folders, task folders, change folders, single-current-document discipline, unfinished-change-first execution, and limiting each task to one task document, one code file, and one unit-test file when needed.
version: 0.1.0
---

# cx Use Cases, Tasks, and Changes

## Purpose

Use this skill before implementation and testing. cx uses use-case-driven story documents instead of the old scenario-expression workflow. Reusable-code scenarios and business scenarios use the same structure: a main success scenario plus conditional substeps attached to concrete main-success steps.

## docs/cx Layout

All cx project descriptions, scenarios, tasks, process documents, and change documents live under `docs/cx`. Documents outside `docs/cx` are not part of cx.

```text
docs/cx/
docs/cx/00.project.md
docs/cx/01.create_user/
docs/cx/01.create_user/00.use_case.md
docs/cx/01.create_user/00.design.md
docs/cx/01.create_user/tasks/
docs/cx/01.create_user/tasks/01.write_user_entity/00.task.md
docs/cx/01.create_user/changes/
docs/cx/01.create_user/changes/20260629T120000-task01-write_user_entity.md
```

Chinese projects may use Chinese file names such as `00.项目说明.md`, `00.用例.md`, and `00. 设计.md`. English projects use the same folder responsibilities with English names.

## Workflow Rules

1. Read project-level `docs/cx` documents first.
2. Read the target main success scenario's use-case document, design document, tasks, and changes.
3. Unless the work is adding a new task, conditional substep, or use case, inspect unfinished changes first and decide the current work from those changes.
4. A use case contains one main success scenario and conditional, alternate, or exception substeps attached to concrete main-success steps.
5. A task is a folder under `tasks/` and starts at `01.`.
6. A task document's basic measure is a class or type group. It may cover one class or a tightly collaborating set of classes or types.
7. A single task touches one task document, one code file, and one matching unit-test file when a test file is required.
8. If one change affects several tasks or also changes the use-case document, split the work into an ordered task list and execute it one task at a time.
9. Before starting work, ask whether to finish documentation, tests, implementation, and validation directly, or ask after each task.
10. If the user does not explicitly choose per-task confirmation, default to direct completion; direct mode continues after document updates into tests, implementation, and validation.
11. Only per-task confirmation mode stops after one task and waits for user review before starting the next task.

## Use-Case Granularity And Main Success Scenario Discipline

1. One `docs/cx/NN.name/` folder represents one user-goal use case; it does not represent a whole app, a menu, a page set, or several independent operations.
2. Name each use case as the actor's goal, such as "view exposed location", "save current location", or "manage favorite locations"; do not use a vague "use the app" use case to hold every behavior.
3. The main success scenario describes the most common direct path from trigger to completed user goal; keep it to about 3 to 9 steps.
4. Each main-success step is one observable actor-system interaction. Do not put a menu, several mutually exclusive choices, several complete tasks, or several user goals into one step.
5. If a main-success step needs its own actors, preconditions, main success scenario, and conditional steps, it is a sub-use case or a separate use case. Split it into a new `docs/cx/NN.name/` folder; the original use case should say "enter use case: X" under the relevant step, not turn that independent use case into a pile of exception branches.
6. Conditional, alternate, and exception behavior must attach to a concrete main-success step with substep numbering such as `1.1` or `2.1`, for example: "2.1 If the user denies permission, end this use case and show that permission is required" or "3.1 If the user needs to manage favorites, enter use case: manage favorite locations."
7. Keep short conditions under the relevant step in the current `00.use_case.md`. Split complex flows into separate use cases when they exceed about 3 to 5 steps, introduce a new actor, have independent completion criteria, or need independent tasks and tests; the original substep should name the entered use case.
8. Do not put every button on a home screen into one main success scenario. Showing the home screen, selecting a favorite, saving the current location, and managing favorites are different user goals and should be separate use cases.
9. A top-level requirement may keep a use-case index and navigation relationships in `docs/cx/00.project.md`, but each use case owns its actors, preconditions, main success scenario, conditional substeps, and completion conditions in its own use-case file.
10. A separate use case must read like a clear scenario: it has a trigger, continuous successful steps, and an observable completion result. It must not be only a collection of errors, exceptions, button branches, or state notes.

## Use-Case Document

The use-case document owns behavior expression:

- Main success scenario.
- Conditional, alternate, and exception substeps attached to concrete main-success steps.
- Observable result.
- Completion conditions.

It should not contain implementation detail that belongs in a task document.

The use-case document should describe one user goal only. If a condition or step becomes another user goal, create a separate use case and link it from the project index or the current use case's sub-use-case list.

## Design Document

The design document explains:

- Existing common code that can simplify work.
- New common code that should be written for reuse.
- Design decisions.
- Task boundaries.

## Change Documents

Each change document must explain:

- Timestamp.
- Task number.
- Task name.
- What was done before.
- What should be done now.
- Status.

The agent uses unfinished changes to decide what to do next.

## Output

When this skill is used, return:

- Target `docs/cx` scenario folder.
- Conditional substep or task being changed.
- Ordered task list when the request spans multiple tasks.
- Current task document.
- Current change document.
- The execution mode and whether per-task review is required.
