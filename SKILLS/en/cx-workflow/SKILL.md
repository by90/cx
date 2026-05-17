---
name: cx-workflow
description: Use for workflow handling, task routing, end-to-end development orchestration, selecting the right cx skills, and deciding whether BDD/TDD, changelog, evidence review, specialist skills, or clarification is needed.
version: 1.0.0
---

# cx Workflow Handling

## Purpose

Use this skill as the cx workflow entry point. It classifies the user's request, selects the cx skills that need to be combined, orders the work, and asks for clarification when missing requirements would make implementation unsafe.

## Entry Flow

1. Classify the task: requirements discussion, feature implementation, bug fix, refactor, specialist technical work, documentation update, evidence review, or installation/use question.
2. Check whether the project already has `docs/INDEX.md` or `docs/README.md`, one or more documentation sets, and `AGENTS.md`.
3. Decide whether the request changes behavior, public APIs, data structures, user workflows, or release mechanics.
4. Select the smallest necessary set of cx skills. Do not apply every skill by default.
5. Select the target documentation set. Multi-feature work uses `docs/<feature-group>/`; single-feature work may keep using the root `docs/` documentation set.
6. State the current step or execute directly. Ask first only when a missing requirement would likely cause the wrong implementation.

## Skill Selection

- Behavior changes, bug fixes, architecture changes, or implementation planning: use `$cx-bdd-tdd`.
- Changelog-only updates or change ID checks: use `$cx-changelog`.
- Python, PyTorch, Lightning, tensor, or ML tests: add `$cx-pytorch-tdd`.
- Variable-length tensors, masks, padding, or collation: add `$cx-ragged-tensor`.
- Rust, GPUI, or gpui-component desktop UI: add `$cx-rust-ui`.
- Multi-task progress, ETA, cancellation, or background task adapters: add `$cx-progress-ui`.
- Shared module extraction, stable APIs, reusable components, or duplicated logic migration: add `$cx-common-module`.
- Final delivery checks, test evidence, or documentation consistency: use `$cx-evidence`.

## Execution Order

1. For normal development tasks, start with `$cx-bdd-tdd`, choose or create the target documentation set, then add specialist skills.
2. For finishing work around an existing implementation, check docs and test evidence before using `$cx-evidence`.
3. For installation, update, language switching, or shskills usage questions, answer with commands directly and do not start BDD/TDD.
4. For read-only analysis or code review, read the relevant files and list risks before making changes, unless the user asks for fixes.
5. For broad changes across multiple feature groups, split the work into feature-group documentation sets and record order, dependencies, and status in `docs/INDEX.md`.
6. For potentially reusable components, data structures, test harnesses, or UI state models, use `$cx-common-module` first to search existing implementations and registries before adding a new abstraction.

## Stop Conditions

- Critical business rules, target environment, or acceptance criteria are missing and continuing would create likely rework.
- The requested implementation conflicts with the current `AGENTS.md`, technical constraints, or public API.
- High-risk or fast-changing information must be verified online, but the environment cannot verify it.

When a stop condition applies, state the blocker and ask the smallest set of questions needed to continue.
