---
name: cx-changelog
description: Use for docs/cx change documents, release notes, audit trails, status changes, and keeping each change mapped to one scenario task instead of a duplicated requirement document.
version: 0.1.0
---

# cx Change Documents

## Purpose

Maintain `changes/` under each `docs/cx` scenario. A change document is the current audit and handoff unit for AI work. It must not duplicate the whole use case.

## Required Location

```text
docs/cx/01.create_user/changes/20260629T120000-task01-write_user_entity.md
```

Chinese projects may use:

```text
docs/cx/01.创建用户/changes/20260629T120000-任务01-编写用户实体.md
```

## Required Content

Each change must include:

- Timestamp.
- Status.
- Task number.
- Task name.
- What was done before.
- What should be done now.

## Rules

1. Inspect unfinished changes before choosing new work.
2. Do not create duplicate planning files outside `docs/cx`.
3. If a change spans multiple tasks, list those tasks in order and execute one at a time.
4. If a change also modifies the use-case document, make that part of the ordered task list.
5. Mark a change complete only after task verification and `$cx-evidence` review PASS are recorded.
6. Default execution stops at the current task and current production code-file boundary; continue through additional tasks only when the user explicitly requests multi-task continuation.

## Output

Return:

- Change file path.
- Current status.
- Task mapping.
- Next required action.
- Verification evidence, review decision, or missing evidence.
