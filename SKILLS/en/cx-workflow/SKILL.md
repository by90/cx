---
name: cx-workflow
description: Use as the cx workflow router and end-to-end orchestrator. Start by reading the project AGENTS.md, current-domain common-package tutorials, and registered public entries, then locate the current story, fixed tasks, and temporary changes and choose the smallest skill set. Durable documents keep only current state, and cx-review handles both quality and completion evidence.
version: 0.1.0
---

# cx Workflow Orchestration

## Purpose

Understand established project knowledge and reusable capabilities before deciding the current work. The workflow keeps no development-process documents: durable documents show only the latest state and Git stores history.

## Overriding principles

1. Keep no intermediate artifact, completed-change archive, old solution, draft, backup, or parallel plan.
2. Project, use-case, design, task, topic, and research documents describe only current valid state.
3. Old/new differences belong only in the active unfinished file under `changes/`.
4. Commit a change file before work. Delete it after review passes and commit the deletion.
5. Task count, numbers, filenames, and identities remain fixed after story creation. Implementation changes and code errors update the original task.
6. Git commits, tags, and releases preserve history. cx documents do not.

## Startup order

1. Create a visible conversation checklist for multi-step work.
2. Read the project-root `AGENTS.md`. If it is missing or does not reflect project goals, languages, and common packages, first create or fix it from `$cx-doc`'s `assets/AGENTS.md`.
3. Read every tutorial registered for the current domain, then check `docs/cx/docs/00.index.md`.
4. Search documented common packages, public entries, source locations, and real callers.
5. Read project context, the current use case, design, and original task.
6. Check the story `changes/` directory.
7. Follow an unfinished change when present; otherwise follow the current original task.
8. For a requirement change, design change, implementation change, or code error in an existing story, create or update the change file and commit it before implementation.
9. Choose the smallest necessary skill set and proceed.

## Common-capability gate

Before adding a class, function, component, data structure, protocol implementation, or tool:

1. Identify the current domain from project `AGENTS.md` and read all registered common-package tutorials.
2. Search registered common packages and stable interfaces.
3. Search source and real callers to confirm documentation is current.
4. Record the reason to adopt or reject each relevant candidate.
5. Design a new entry only when no existing capability satisfies the goal.
6. Add a caller tutorial and update the index and project `AGENTS.md` navigation with any new common capability.

Ignoring a registered common package and adding similar implementation is duplication and must fail `$cx-review`.

## Current state and changes

- A new story may establish a new fixed task set.
- An existing story never adds, deletes, or renames task files.
- A changed approach first enters `$cx-changelog`, then rewrites the original task.
- Code errors use the same flow and never create fix tasks or error-history documents.
- Durable documents cannot narrate prior/current alternatives or migrations. That material belongs only in the active change file.
- Keep the change file until `$cx-review` passes, then delete and commit it.

## Topic documents and research

- Use `$cx-doc` for caller tutorials and register each common package's domain, tutorial link, public entry, and read-first condition in project `AGENTS.md`.
- Use `$cx-doc` for protocols, data processes, feature systems, metric definitions, and technical direction.
- Use `$cx-research` for research and save its question-specific synthesized conclusion under `docs/cx/notes/`.
- Answer the research question first, then explain evidence, limits, and work impact plainly.
- Do not commit search scratchpads, excerpt piles, or candidate-process notes.

## Skill routing

- Use cases, fixed task sets, and current story state: `$cx-story`.
- Changes or code errors in an existing story: `$cx-changelog`, then return to the original `$cx-story` task.
- Topic documents, common-package docs, protocols, data processes, feature systems, or technical direction: `$cx-doc`.
- Reusable functions, classes, and stable interfaces: `$cx-doc`, then `$cx-common-module`.
- Architecture, responsibilities, domain objects, and data-access boundaries: `$cx-design`.
- Research, model selection, and paper synthesis: `$cx-research`, with `$cx-doc` for the note.
- Explicitly requested unit tests or test-driven development: use `$cx-tdd` as the single main workflow; add `$cx-pytorch-tdd` for Python, PyTorch, or Lightning tests, and add `$cx-rust-tdd` for Rust tests.
- Ordinary Rust implementation follows the current task's default implementation flow. Do not use `$cx-rust-tdd` without an explicit test requirement.
- Version release: `$cx-version`.
- Artifact quality and completion evidence: `$cx-review`.

## Implementation discipline

1. By default, complete the current task document and edit its one production file.
2. Continue through multiple original tasks only when the user explicitly requests it.
3. Do not create, modify, or run unit tests unless the user, current task, or active change explicitly declares them.
4. Use complete object modeling for state, lifecycle, invariants, and domain collaboration.
5. Keep implementation minimal and remove redundant checks, fallbacks, variables, unused entries, and speculative extensions.
6. Unless the user explicitly requests a specific validation or error behavior in the current request, do not add validation that raises an error and do not catch, translate, wrap, swallow, or fall back from errors. Preserve the original type, message, and stack and stop execution.
7. Implement only the latest intent. Delete old interfaces, aliases, adapters, bridges, compatibility branches, old parameters, old configuration, old paths, old behavior, and all traces; migrate every caller to the current entry.
8. For cx source changes, finish Chinese source and package first, then synchronize English source and package.
9. Commit and push `main`, then run the remote installer to update global skills and `AGENTS.md`.

## Completion order

1. Rewrite durable documents and implementation to current state.
2. Run the narrowest effective verification, then necessary package-level checks.
3. Use `$cx-review` for artifact-quality review.
4. Use the same `$cx-review` for the completion-evidence gate.
5. Keep the change file and fix findings when review fails.
6. Delete the change file and commit the deletion when review passes.
7. Finish, cancel, or explicitly block every checklist item and report verification and residual risk.
