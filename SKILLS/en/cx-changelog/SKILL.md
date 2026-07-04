---
name: cx-changelog
description: Use for docs/cx change documents, release notes, audit trails, status changes, and keeping each change mapped to one scenario task instead of a duplicated requirement document.
version: 0.1.0
---

# cx Change Documents

## Language Rules

- Use the package language for conversations, explanations, plans, summaries, review decisions, verification evidence, and cx documents. Do not mix languages inside prose fragments or term lists.
- In Chinese-package work, if an English identifier, command, path, API name, library, protocol, standard, proper name, or ambiguity-sensitive term must remain in English, explain its meaning, role, and local context in Chinese in the same sentence or an adjacent sentence. In English-package work, explain unavoidable non-English terms in English.

## Purpose

Maintain `changes/` under each `docs/cx` scenario. A change document records later changes after implementation. It must not duplicate the whole use case or replace initial planning.

## Required Location

```text
docs/cx/01.create_user/changes/adjust_user_entity_constraints.md
```

Chinese projects may use:

```text
docs/cx/01.创建用户/changes/调整用户实体约束.md
```

## Required Content

Each change must include:

- Implementation time.
- Status.
- Related task or document.
- What was done before.
- What should be done now.

## Rules

1. Inspect unfinished changes before choosing new work.
2. Do not create duplicate planning files outside `docs/cx`.
3. Do not create change documents for unimplemented planning.
4. Change filenames do not include timestamps.
5. If a change spans multiple tasks, list those tasks in order and execute one at a time.
6. If a change also modifies the use-case document, make that part of the ordered task list.
7. Mark a change complete only after task verification, `$cx-review` PASS for each produced artifact type, and `$cx-evidence` handoff evidence review are recorded.
8. Default execution stops at the current task and current production code-file boundary; continue through additional tasks only when the user explicitly requests multi-task continuation.

## Output

Return:

- Change file path.
- Current status.
- Task mapping.
- Next required action.
- Verification evidence, review decision, or missing evidence.
