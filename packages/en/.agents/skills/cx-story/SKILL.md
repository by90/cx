---
name: cx-story
description: Use for use-case-driven story discovery and current-state maintenance. Manage docs/cx project context, main-success scenarios, the single current use case and design, fixed task sets, and temporary changes, while preventing task-count churn when an existing story changes, code fails, or implementation direction shifts.
version: 0.1.0
---

# cx Current-State Story Workflow

## Purpose

Express user goals through main-success scenarios while keeping project, use-case, design, and task documents at the current valid state. Establish the task set once when the story is created. Later changes update the original tasks through a temporary change file, with history retained only by Git.

## Current-state principles

1. `docs/cx/` is the sole root for project context, use cases, designs, tasks, topic documents, research notes, and temporary changes.
2. Durable documents describe only current facts, goals, design, tasks, interfaces, and conclusions.
3. Durable documents never preserve old solutions, comparisons, migrations, attempts, completed changes, or historical summaries.
4. Keep one current document per object. Never create drafts, backups, old versions, or parallel plans.
5. Old/new differences appear only in an unfinished change file.
6. Delete completed change files. Git commits, tags, and releases preserve history.

## Layout

```text
AGENTS.md
docs/cx/
docs/cx/00.project.md
docs/cx/docs/
docs/cx/docs/00.index.md
docs/cx/notes/
docs/cx/01.create_user/
docs/cx/01.create_user/00.use_case.md
docs/cx/01.create_user/00.design.md
docs/cx/01.create_user/tasks/
docs/cx/01.create_user/tasks/01.validate_request.md
docs/cx/01.create_user/changes/
```

- The project-root `AGENTS.md` supplements global rules and navigates current-project common-package tutorials.
- `docs/cx/docs/` stores caller tutorials for common packages and topic documents for stable technical processes.
- `docs/cx/notes/` stores current conclusions for explicit research questions.
- Each numbered top-level story folder represents one user goal.
- Each story has one current use case, one current design, a fixed `tasks/` set, and a `changes/` directory containing unfinished work only.

## Use-case discipline

1. Name the participant goal, such as “create user,” rather than a generic system activity.
2. Keep the most common direct success path to roughly three through nine observable interactions.
3. Attach conditions, alternatives, and errors to a main step with `1.1`, `2.1`, and state whether the flow returns, ends, or enters another use case.
4. Split a flow into another use case when it needs its own participant, preconditions, sequence, or completion result.
5. Keep implementation tasks, test plans, and change history out of the use case.

## Fixed task set

1. When a new story is created, create all necessary task files from the current design.
2. Name tasks `tasks/NN.concise_name.md`. Each task owns one stable responsibility and one production file, plus one matching test file only when unit tests are explicitly declared.
3. After story creation, task count, numbers, filenames, and identities remain fixed.
4. When requirements, design, or implementation change, create a temporary change file and rewrite the original task body.
5. Map code errors to the original task. Never create fix, remove, modify, or reimplementation tasks.
6. Add a story and its own fixed tasks only for a genuinely independent user goal.
7. Task title, goal, scope, current requirements, verification, and status describe only current work.

## Work priority

1. Read the project-root `AGENTS.md`. When initializing a project, create it from `$cx-doc`'s `assets/AGENTS.md` and tailor it to project goals, languages, toolchain, and common packages.
2. Read every common-package tutorial linked for the current domain and `docs/cx/docs/00.index.md`.
3. Search registered common packages, public interfaces, and real callers.
4. Read the project context, target use case, design, and original task.
5. Check `changes/`; use the earliest still-relevant unfinished change as the current instruction.
6. Without an active change, follow the current original task.
7. For a change or code error in an existing story, use `$cx-changelog` and commit the change file before implementation.
8. Update tutorials, the topic index, and project `AGENTS.md` navigation when a common package is added or changed.
9. Rewrite durable documents and implementation to current state, then use `$cx-review` for quality and completion evidence.
10. Delete the change file and commit the deletion only after review passes.

## Durable document sections

Use case: goal, participants, preconditions, trigger, main-success scenario, child-use-case index, task index, completion criteria.

Design: file scope, public entry, topic documents and common capabilities, object responsibilities and collaboration, decisions, non-goals, verification.

Task: source, goal, file scope, task measure, current implementation requirements, verification, status.

## Completion criteria

- Use case, design, tasks, topic documents, and implementation state only current facts.
- The project-root `AGENTS.md` matches project goals, languages, toolchain, and common packages and navigates every common-package tutorial.
- Task files in an existing story did not change because of a change or error.
- All declared verification succeeded.
- Both `$cx-review` stages passed.
- `changes/` contains no completed change file.
