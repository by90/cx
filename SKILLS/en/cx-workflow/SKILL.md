---
name: cx-workflow
description: Use for workflow handling, task routing, end-to-end development orchestration, selecting the right cx skills, and deciding whether BDD, TDD, changelog, release versioning, research, evidence review, or clarification is needed.
version: 1.0.0
---

# cx Workflow Handling

## Purpose

Use this skill as the cx workflow entry point. It classifies the user's request, selects the cx skills that need to be combined, orders the work, and asks for clarification when missing requirements would make implementation unsafe.

## Entry Flow

1. Classify the task: requirements discussion, feature implementation, bug fix, refactor, specialist technical work, documentation update, evidence review, or installation/use question.
2. Check whether the project already has `docs/INDEX.md` or `docs/README.md`, one or more documentation sets, and `AGENTS.md`.
3. Decide whether the request changes behavior, public APIs, data structures, user workflows, release mechanics, or research conclusions.
4. Select the smallest necessary set of cx skills. Do not apply every skill by default.
5. Select the target documentation set. Multi-feature work uses `docs/<feature-group>/`; single-feature work may keep using the root `docs/` documentation set.
6. State the current step or execute directly. Ask first only when a missing requirement would likely cause the wrong implementation.

## Prompt Intake Contract

When the user request is vague, normalize it into this contract before planning:

```text
Goal:
Context:
Constraints:
Required workflow:
Verification:
Deliverables:
```

- Goal must describe observable behavior or a concrete research/release outcome.
- Context should identify target docs, files, branch, environment, and relevant prior decisions.
- Constraints should include public APIs, language rules, compatibility, performance, security, or style limits.
- Required workflow names the smallest necessary cx skills.
- Verification lists the commands, checks, screenshots, or evidence expected.
- Deliverables state what will be changed and what summary/evidence is required.

Ask a clarifying question only when a missing field would likely cause wrong behavior, unsafe changes, or unverifiable work. Otherwise proceed and state assumptions briefly.

## Skill Selection

- Behavior discovery, requirements, acceptance criteria, business rules, or scenario writing: use `$cx-bdd`.
- Test-first implementation after BDD is clear: use `$cx-tdd`.
- Behavior changes, bug fixes, architecture changes, or implementation planning: use `$cx-bdd`, then `$cx-tdd`.
- Changelog-only updates or change ID checks: use `$cx-changelog`.
- Release version decisions, SemVer bumps, tags, or release notes: use `$cx-version`.
- Model selection, model mechanism research, recent AI papers, academic/blog synthesis, or research reports: use `$cx-research`.
- Python, PyTorch, Lightning, tensor, or ML tests: add `$cx-pytorch-tdd`.
- Rust implementation or Rust tests: add `$cx-rust-tdd`.
- Shared module extraction, stable APIs, reusable components, or duplicated logic migration: add `$cx-common-module`.
- Final delivery checks, test evidence, or documentation consistency: use `$cx-evidence`.

## Execution Order

1. For normal development tasks, start with `$cx-bdd`, choose or create the target ordered feature folder, then use `$cx-tdd` and any specialist skill.
2. For finishing work around an existing implementation, check docs and test evidence before using `$cx-evidence`.
3. For installation, update, language switching, or shskills usage questions, answer with commands directly and do not start BDD/TDD.
4. For read-only analysis or code review, read the relevant files and list risks before making changes, unless the user asks for fixes.
5. For broad changes across multiple feature groups, split the work into feature-group documentation sets and record order, dependencies, and status in `docs/INDEX.md`.
6. For potentially reusable components, data structures, test harnesses, or UI state models, use `$cx-common-module` first to search existing implementations and registries before adding a new abstraction.
7. For component domains such as progress UI or ragged tensor utilities, do not invent a new cx skill. Treat them as project components with their own README and tests.

## Stop Conditions

- Critical business rules, target environment, or acceptance criteria are missing and continuing would create likely rework.
- The requested implementation conflicts with the current `AGENTS.md`, technical constraints, or public API.
- High-risk or fast-changing information must be verified online, but the environment cannot verify it.

When a stop condition applies, state the blocker and ask the smallest set of questions needed to continue.
