---
name: cx-review
description: Use for the unified review of any completed code, document, tutorial, research, design, process, or release artifact. First review artifact quality by type, then verify review coverage, validation evidence, current-state documents, temporary-change deletion conditions, and residual risk. A failure in either stage blocks completion and deletion of the active change file.
version: 0.1.0
---

# cx Unified Delivery Review

## Purpose

Run two consecutive stages in one skill: determine whether artifacts are correct, then determine whether the evidence permits completion. A task completes and its active change file can be deleted only after both stages pass.

## General rules

1. List every artifact type and file in scope.
2. Review each artifact type independently.
3. Run the completion-evidence gate after artifact-quality review.
4. Any priority-one, priority-two, or priority-three finding fails review. Fix it and repeat both stages.
5. Durable documents describe only the current valid state. Old solutions, comparisons, and process narratives belong only in an unfinished change file.
6. A failed review keeps the task unfinished and the active change file present.
7. Delete the change file only after both stages pass, then commit the deletion.

## Stage one: artifact quality

### Code

- Implementation exactly matches the current use case, design, original task, and unfinished change.
- Explicit objects or equivalent types represent state, lifecycle, invariants, and domain collaboration.
- The agent read relevant `docs/cx/docs/` topics and searched registered common packages, public entries, and real callers.
- Unless the user explicitly requests a specific validation or error behavior in the current request, code does not add validation that raises an error and does not catch, translate, wrap, swallow, skip, or fall back from errors. The original type, message, and stack stop execution.
- Code, interfaces, parameters, configuration, paths, callers, documentation, examples, and declared tests express only the latest intent. No old entry, alias, adapter, bridge, compatibility branch, compatibility behavior, or old trace remains.
- No duplicated logic, bloated code, needless parameters, needless variables, convenience wrapper, debug entry, or speculative extension remains.

### Current-state documents

- Project, use-case, design, task, topic, and research documents each have a distinct responsibility.
- Every durable document states only the current goal, design, task, interface, or conclusion.
- No durable document contains an old solution, comparison, migration narrative, completed change, draft, backup, or parallel version.
- An existing story did not change task count or task identity because of a requirement change, implementation change, or code error.
- Every topic has one current document and every link or source entry is valid.

### Design

- Design starts from target behavior, constraints, data boundaries, lifecycle, and invariants.
- Entries, object responsibilities, collaboration, state sources, reuse boundaries, non-goals, and verification are explicit.
- Common packages and stable technical processes have independent topic documents under `docs/cx/docs/`.
- The design maps to the original task set without creating tasks for implementation changes.

### Tutorial

- Preconditions, steps, commands, inputs, expected results, and failure handling are executable in order.
- Commands, paths, labels, and interfaces match current project state.
- No outdated step, historical alternative, or hidden prerequisite remains.

### Research

- The question, date window, inclusion criteria, exclusion criteria, and audience are explicit.
- Reliable sources support non-obvious claims, with source types distinguished.
- The note under `docs/cx/notes/` answers the question, explains it plainly, and states applicability, limits, and work impact.
- No search scratchpad, material pile, candidate history, or replaced conclusion remains.

### Temporary change and process

- Changes, implementation direction shifts, and code errors in an existing story entered `changes/` and were committed before work.
- The change file fully states current facts, target state, and major differences.
- Durable documents were rewritten directly to current state without copying the change history.
- The original task was updated while task count and identity remained stable.

## Stage two: completion-evidence gate

Verify:

1. Every artifact type received its corresponding quality review.
2. The request, current use case, design, original task, code, and topic documents express the same behavior.
3. Commands, checks, screenshots, sources, or observation actually cover the artifacts.
4. Unit tests are evidence only when explicitly declared by the user, current task, or active change.
5. No unrun, failed, or missing verification is reported as successful.
6. Durable documents contain only current state and no old/new difference outside unfinished changes.
7. No required topic document or registered common capability was ignored.
8. All callers use the current entry without compatibility code.
9. No failed review, unresolved finding, or blocker is marked complete.
10. The active change file can be deleted without losing current knowledge because durable documents are updated.
11. Residual risks are explicit and do not block the current goal.

## Output

```text
Findings:
1. [severity] file:line - issue
   Evidence:
   Fix:

Review scope:
- Artifact types:
- Current documents checked:
- Commands or sources checked:

Verified:
- command or evidence -> result

Missing evidence:
- None, or list the gap

Review decision:
- PASS or FAIL
- FAIL keeps the task unfinished and the active change file present

Residual risk:
- None, or list non-blocking risks
```
