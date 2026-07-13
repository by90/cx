---
name: cx-changelog
description: Use for temporary change files under a docs/cx story changes directory. Trigger when an existing story, task, design, or implementation must change, when code is wrong, or when implementation direction changes. Record the major old/new differences, commit the current work instruction, and delete it after review so Git remains the only history source.
version: 0.1.0
---

# cx Temporary Change Workflow

## Purpose

`changes/` shows only unfinished work. A change file guides updates to an existing story, design, original task, and implementation. It is not a permanent audit log. Commit it before implementation, delete it after completion, and commit the deletion so history exists only in Git.

## When to create one

For an existing story, create or update a temporary change file before:

1. Changing the user goal, conditional steps, design, or interface.
2. Replacing the implementation approach of an original task.
3. Fixing incorrect code, a regression, or behavior that disagrees with current documents.
4. Changing common capabilities, dependencies, data structures, or technical direction.

An entirely new story creates its fixed task set directly because no earlier state exists. Once registered, every later change follows `changes/`.

## Core rules

1. Every story keeps a `changes/` directory, but it contains only unfinished change files.
2. Prefer one active change file for one continuous objective. Do not split one concern into add/remove/modify/fix change chains.
3. The change file is the only project document allowed to describe the previous state, target state, and major differences.
4. Use cases, designs, tasks, topic documents, research notes, and interface docs describe only the latest state.
5. Commit a created or updated change file before editing durable documents or implementation.
6. Map code errors back to the original story and task. Never create a fix task.
7. When implementation changes, rewrite the original task without creating, deleting, or renaming task files.
8. Delete the change file only after both `$cx-review` stages pass.
9. Commit the deletion. Never move completed change content into another document.
10. An empty `changes/` directory means there is no unfinished change.

## File format

```markdown
# Change: adjust request validation

## Status

In progress

## Related objects

- Use case: `00.use_case.md`
- Design: `00.design.md`
- Original task: `tasks/01.validate_request.md`

## Current facts

Describe behavior, documents, and implementation that exist before work starts.

## Target state

Describe the latest behavior, documents, and implementation that must exist after completion.

## Major changes

1. List every material difference between current facts and target state.

## Ordered work list

| Order | Original task or document | Current action | Status |
| --- | --- | --- | --- |
| 01 | `tasks/01.validate_request.md` | Rewrite for the current approach | In progress |

## File scope

- Durable documents: TODO
- Production file: TODO
- Unit-test file: Not declared

## Verification

TODO

## Completion action

- Delete this file after review passes.
- Commit the deletion and create no completed-change archive.
```

## Execution order

1. Read topic documents, the current use case, design, task, and unfinished changes.
2. Write current facts, target state, and major differences into one temporary change file.
3. Commit the file so the work instruction enters Git.
4. Rewrite durable documents and implementation to the latest state.
5. Update only the active work list as work progresses.
6. Use `$cx-review` for artifact quality and the completion-evidence gate.
7. Keep the change file when review fails.
8. Delete the change file and commit the deletion when review passes.

## Prohibited

- Keeping a completed change file.
- Creating change archives, historical summaries, migration histories, or durable comparison documents.
- Creating new tasks to represent a change, removal, fix, or second implementation of an original task.
- Copying change history into a task, design, topic document, or research note.
