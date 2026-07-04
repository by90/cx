---
name: cx-review
description: Use for mandatory local review after code, documentation, tutorials, research, design, process changes, or any other deliverable is produced. Reviews by artifact type for document agreement, business semantics, duplication smells, full OOP, minimal implementation, source quality, tutorial executability, design feasibility, and completion status. If review fails, the task, change, or deliverable is not complete.
version: 0.1.0
---

# cx Deliverable Review

## Purpose

Run local review after any deliverable is produced and before marking a task or change complete. Deliverables include code, use-case documents, task documents, change documents, design documents, tutorials, research reports, release notes, and workflow rules. Any P0/P1/P2 finding means review fails; the task, change, or deliverable must remain incomplete until fixed and reviewed again.

## General Rules

1. Identify the artifact types produced in this turn; when several types changed, review each type.
2. Review against the user request, `docs/cx` project notes, use case, design, task, change, and relevant sources; do not only inspect surface formatting.
3. If review fails, return concrete findings, evidence, and fixes. Do not mark the task, change, or deliverable complete.
4. After review passes, record the PASS decision, review scope, verification evidence, and residual risk in the current task or change document. If no target cx document exists, state it in the final summary.

## Review Types

### Code

- Implementation matches the use case, design, task, and change documents exactly, with no missing behavior, scope creep, or changed business meaning.
- No repeated checks, transformations, config reads, field passing, similar helpers, or several locals naming the same concept.
- Full OOP is used when state, lifecycle, invariants, or domain collaboration are present.
- Implementation is minimal: no extra validation, fallbacks, exception wrapping, variable passing, parameters, redundant names, bloated files, or abstractions without real reuse.
- Constructors and functions use default parameters for configuration defaults, for example `path=Config.default_config_file()` or `batch_size=config.train.batch_size`; function bodies store parameters on same-named fields, such as `self.batch_size = batch_size`.

### Documentation

- The document has a clear audience, goal, scope, status, and single home.
- Content matches project notes, use cases, design, tasks, changes, code behavior, and verification evidence.
- No scattered documents, duplicate explanations, stale claims, conflicting rules, vague TODOs, or unsupported conclusions.
- Structure is short and actionable instead of repeating background or narrative filler.
- Documents state concrete facts, concrete actions, and concrete decisions, with no filler, repeated goals, missing "what to do", or undefined invented terms.
- Project documents, use cases, designs, and tasks each own their own content; the same goals are not repeated across all of them.
- Use cases express business scenarios, main success scenarios, conditional substeps, and sub-use cases, not test plans or implementation tasks.
- Task files use `tasks/NN.task_name.md`, change files use `changes/change_name.md` without timestamps, and change documents record only later changes after implementation.
- Common packages under `src/<subsystem>/` have package-local `readme.md` files that list public APIs and usage, not instance config sections, internal fields, or implementation steps as public-interface documentation.

### Tutorial

- The tutorial can be followed in order; prerequisites, commands, inputs, expected outputs, and failure handling are explicit.
- Commands, paths, UI text, and APIs match the current project state.
- No hidden steps, skipped steps, stale commands, marketing-style introductions, or one-off experience presented as stable process.
- Examples are minimal and runnable, and do not lead users to damage the worktree, expose credentials, or bypass project rules.

### Research

- The research question, date window, inclusion criteria, exclusion criteria, and target reader are defined first.
- Every non-obvious claim has a reliable source; volatile facts such as latest status, recommendations, prices, rules, model capabilities, or paper status are checked online.
- Primary sources, papers, blog interpretations, vendor claims, and weak community signals are separated.
- The output provides synthesis, limits, unknowns, and actionable recommendations instead of only listing sources.

### Design

- The design starts from target behavior, business constraints, data boundaries, lifecycle, and invariants.
- Public entrypoints, common call paths, special-case entrypoints, state sources, reuse boundaries, non-goals, and verification are explicit.
- Necessary tradeoffs are compared, including why more complex, dynamic, or legacy-compatible paths are not chosen.
- The design can be implemented by the next one-task/one-code-file step or by an explicit ordered task sequence.

### Process And Change

- The change document accurately records previous state, current requirement, ordered task list, affected files, verification evidence, and completion status.
- A task or change is marked complete only after the corresponding artifact review passes.
- Failed, missing-evidence, unverified, unreviewed, or user-unconfirmed work is not written as complete.

## Output Format

```text
Findings:
1. [severity] file:line - issue
   Evidence:
   Fix:

Review scope:
- Artifact type:
- Documents checked:
- Commands or sources checked:

Review decision:
- PASS or FAIL
- FAIL means the task, change, or deliverable remains incomplete

Residual risk:
- ...
```
