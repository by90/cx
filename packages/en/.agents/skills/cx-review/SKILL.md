---
name: cx-review
description: Use for the unified review of any completed code, document, tutorial, research, design, process, or release artifact. First review artifact quality by type, then verify review coverage, validation evidence, current-state documents, temporary-change deletion conditions, and residual risk. A failure in either stage blocks completion and deletion of the active change file.
metadata:
  version: 0.1.1
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

- The modified scope contains only the current task jointly defined by the user's current request, current use-case path, original task document, and active unfinished change. Any out-of-scope modification without the user's explicit authorization for that specific list item is a scope violation and fails review, regardless of motive or outcome.
- Out-of-scope issues were not opportunistically modified, deleted, formatted, refactored, tested, documented, or configured. They appear only on an authorization-needed list containing file, location, symptom, risk, and recommendation; agent inference, preference, review opinion, and best-practice judgment were not treated as authorization.
- Implementation exactly matches the current use case, design, original task, and unfinished change.
- Explicit objects or equivalent types represent state, lifecycle, invariants, and domain collaboration.
- The agent read current-domain common-package tutorials from project `AGENTS.md` and searched registered public entries and real callers.
- Unless the user explicitly requests a specific validation or error behavior in the current request, code does not add validation that raises an error and does not catch, translate, wrap, swallow, skip, or fall back from errors. The original type, message, and stack stop execution.
- Code, interfaces, parameters, configuration, paths, callers, documentation, examples, and declared tests express only the latest intent. No old entry, alias, adapter, bridge, compatibility branch, compatibility behavior, or old trace remains.
- No duplicated logic, bloated code, needless parameters, needless variables, convenience wrapper, debug entry, or speculative extension remains.
- UI deliverables used `$cx-ui`: every page, reusable component, and ViewModel lives in a separate file; dependencies flow only through View, ViewModel, Service, Data; module entrypoints contain no page, component, business, or data implementation.
- Explicit Rust tests all live under repository-root `tests/`, mirror `src/` as closely as possible, and map each tested source file to at most one matching `_test.rs`; production source contains no `#[cfg(test)]`, inline tests, or fixtures.

### Current-state documents

- The project-root `AGENTS.md`, project, use-case, design, task, topic, and research documents each have a distinct responsibility.
- Project `AGENTS.md` is tailored to project goals, languages, toolchain, and common packages and supplements rather than copies global rules.
- Project `AGENTS.md` lists every common package's domain, tutorial link, public entry, and read-first condition, and every link is valid.
- Every durable document states only the current goal, design, task, interface, or conclusion.
- No durable document contains an old solution, comparison, migration narrative, completed change, draft, backup, or parallel version.
- An existing story did not change task count or task identity because of a requirement change, implementation change, or code error.
- Every topic has one current document and every link or source entry is valid.

### Design

- Design starts from target behavior, constraints, data boundaries, lifecycle, and invariants.
- Entries, object responsibilities, collaboration, state sources, reuse boundaries, non-goals, and verification are explicit.
- Common packages have independent caller tutorials under `docs/cx/docs/`, and stable technical processes have independent topic documents.
- The design maps to the original task set without creating tasks for implementation changes.

### Tutorial

- The tutorial explains real work from the caller's perspective rather than cataloging internal classes, fields, or implementation steps.
- Goal, scenarios, prerequisites, public entry, inputs, outputs, minimal runnable example, steps, expected results, failure handling, constraints, and verification are complete.
- Preconditions, steps, commands, inputs, expected results, and failure handling are executable in order.
- Commands, paths, labels, and interfaces match current project state.
- No outdated step, historical alternative, or hidden prerequisite remains.
- Every common package has exactly one current tutorial and project `AGENTS.md` links it correctly.

### Research

- The question, date window, inclusion criteria, exclusion criteria, and audience are explicit.
- Reliable sources support non-obvious claims, with source types distinguished.
- The note under `docs/cx/notes/` answers the question, explains it plainly, and states applicability, limits, and work impact.
- No search scratchpad, material pile, candidate history, or replaced conclusion remains.

### Machine-learning experiments

- When the project has formal models, the experiment read project-authorized Git tags and frozen artifacts directly and froze the strongest formal-model baseline with the same data scope, label, split, and aggregation contract. It did not check out a tag, restore the working tree, create a worktree, or retrain a historical release merely to compare baselines.
- Before training a new model, loss, feature, capacity, optimization, or scheduling direction, the work used `$cx-research` for online research. The research note synthesizes formal-release facts with reliable sources and states a falsifiable hypothesis, one changed variable, and contract-comparable acceptance criteria.
- Every run used to accept or reject a direction, compare candidates, promote, scale, calculate parameter importance, or select the next configuration has at least twenty-one cumulative strict validation-loss improvements. A run below twenty-one is only invalid evidence, and no local business-metric peak entered a conclusion.
- HPO samplers, pruners, parameter importance, and incumbents use only trials with at least twenty-one strict validation-loss improvements. Resource failures and invalid evidence retain only their original state and reason.
- Business comparisons between formal baselines and candidates use the same population, target dates, labels, daily-N source, and cross-day aggregation. Stock ranking checks dynamic TopN, fixed TopK, highest target levels, and lowest target-level contamination together rather than substituting one aggregate metric.

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
7. No tutorial required by project `AGENTS.md`, topic document, or registered common capability was ignored.
8. All callers use the current entry without compatibility code.
9. No failed review, unresolved finding, or blocker is marked complete.
10. The active change file can be deleted without losing current knowledge because durable documents are updated.
11. Residual risks are explicit and do not block the current goal.
12. Machine-learning experiment deliverables prove the formal baseline, pre-training research, and twenty-one-improvement eligibility of every run supporting a conclusion; invalid evidence did not affect direction selection.

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
