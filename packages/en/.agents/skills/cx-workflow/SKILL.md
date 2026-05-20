---
name: cx-workflow
description: Use for workflow handling, task routing, end-to-end development orchestration, selecting the right cx skills, and deciding whether BDD, TDD, changelog, release versioning, research, evidence review, or clarification is needed.
version: 0.1.0
---

# cx Workflow Handling

## Purpose

Use this skill as the cx workflow entry point. It classifies the user's request, selects the cx skills that need to be combined, orders the work, and asks for clarification when missing requirements would make implementation unsafe.

## Entry Flow

1. Classify the task: requirements discussion, feature implementation, bug fix, refactor, specialist technical work, documentation update, evidence review, or installation/use question.
2. For any feature-group work, require a dedicated feature branch before changing files. Feature branches merge to `dev`, not directly to `main`.
3. Check whether the project already has `docs/INDEX.md` or `docs/README.md`, one or more documentation sets, and `AGENTS.md`.
4. Decide whether the request changes behavior, public APIs, data structures, user workflows, release mechanics, or research conclusions.
5. Select the smallest necessary set of cx skills. Do not apply every skill by default.
6. Select the target documentation set. Multi-feature work uses `docs/<feature-group>/`; single-feature work may keep using the root `docs/` documentation set.
7. State the current step or execute directly. Ask first only when a missing requirement would likely cause the wrong implementation.

## Hard Constraints

1. For development work that needs BDD, an engineering spec, an implementation plan, or a changelog entry, stop after updating the documents, report the document result to the user, and wait for explicit user confirmation. Do not write tests, edit implementation, or enter TDD before that confirmation.
2. When the target project has the Chinese cx package installed, every cx-generated or cx-maintained document must be Simplified Chinese, including `BDD.md`, `ENGINEERING_SPEC.md`, `CHANGELOG.md`, `docs/INDEX.md`, plans, test matrices, and verification evidence. Code identifiers, commands, API names, and quoted external names may remain in their source language.
3. When the user asks to commit, deliver, open a PR, or release, treat the working tree as one change set: stage tracked and untracked files and make one commit. Do not analyze which files were changed by the assistant versus the user, and do not split commits by ownership; stop first only for obvious secrets, build artifacts, or unrelated large files.
4. After work is complete, merge the related feature branch into `dev` and delete the local feature branch. Push the feature branch to the remote only when the user explicitly asks; by default, push only `dev`, and push `main` only when the user explicitly asks for a release handoff.
5. Use "verified basis" or "verification evidence" for information backed by documents, tests, command output, or cited sources. Do not use the unclear phrase "engineering facts."

## Prompt Intake Contract

When the user request is vague, normalize it into this contract before planning:

```text
Goal:
Context:
Branch:
Constraints:
Required workflow:
Verification:
Deliverables:
```

- Goal must describe observable behavior or a concrete research/release outcome.
- Context should identify target docs, files, branch, environment, and relevant prior decisions.
- Branch should name the feature-group branch, confirm the integration target is `dev`, and say whether a release handoff to `main` is requested.
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

1. For normal development tasks, start or switch to a dedicated feature-group branch before editing project files.
2. Then use `$cx-bdd`, choose or create the target ordered feature folder, and update `BDD.md`, `ENGINEERING_SPEC.md`, and `CHANGELOG.md`.
3. After the document update is complete, stop, report the document changes and next implementation plan to the user, and wait for explicit user confirmation.
4. After user confirmation, use `$cx-tdd` and any specialist skill to write the failing test, record the red failure, implement the smallest change, and validate it.
5. When a feature group is complete, merge its branch into `dev`; never merge a feature branch directly into `main`.
6. For finishing work around an existing implementation, check docs and test evidence before using `$cx-evidence`.
7. For installation, update, language switching, or shskills usage questions, answer with commands directly and do not start BDD/TDD.
8. For read-only analysis or code review, read the relevant files and list risks before making changes, unless the user asks for fixes.
9. For broad changes across multiple feature groups, split the work into feature-group documentation sets and record order, dependencies, and status in `docs/INDEX.md`.
10. For potentially reusable components, data structures, test harnesses, or UI state models, use `$cx-common-module` first to search existing implementations and registries before adding a new abstraction.
11. For component domains such as progress UI or ragged tensor utilities, do not invent a new cx skill. Treat them as project components with their own README and tests.
12. For release work, use `$cx-version`: after the user confirms the version is complete, merge `dev` into `main`; only `main` may be used for the version commit, annotated release tag, and release-tag push. Feature branches and `dev` may still be pushed for collaboration, backup, or CI.

## Stop Conditions

- Critical business rules, target environment, or acceptance criteria are missing and continuing would create likely rework.
- The requested implementation conflicts with the current `AGENTS.md`, technical constraints, or public API.
- High-risk or fast-changing information must be verified online, but the environment cannot verify it.

When a stop condition applies, state the blocker and ask the smallest set of questions needed to continue.
