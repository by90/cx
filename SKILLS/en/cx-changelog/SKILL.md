---
name: cx-changelog
description: Use when updating changelogs, release notes, change IDs, audit trails, ordered change-task records, or ensuring CHANGE entries stay only in the target documentation set's CHANGELOG.
version: 1.0.0
---

# cx Changelog Curator

## Purpose

Maintain the target documentation set's `CHANGELOG.md` as the only ordered record of changes and change tasks. It must not become a second requirements document and must not duplicate long behavior descriptions. In multi-feature projects, each `docs/<feature-group>/CHANGELOG.md` records that feature group's history, while `docs/INDEX.md` handles cross-feature indexing.

## Rules

1. Every entry must have a stable `CHANGE-YYYY-NNN` ID.
2. Every entry must include date, type, status, work branch, base branch, feature group, summary, related scenarios, tests, and evidence.
3. Concrete change IDs belong only in `CHANGELOG.md` or the version index; do not copy them into the same documentation set's `ENGINEERING_SPEC.md`.
4. Do not copy long requirements into the changelog.
5. One feature group or one change normally uses a separate work branch, then merges into `dev` and deletes the work branch after completion.
6. When a feature group is complete and ready to release, use the version tool to append `docs/VERSIONS.md`, for example `v0.0.1 "Create project template"`.
7. Do not create separate release-note documents unless the user explicitly asks.
8. Keep entries short enough to scan and concrete enough to audit and order tasks.

## Entry template

```markdown
### CHANGE-YYYY-NNN - Title

- Date:
- Type: feature | bugfix | refactor | test | docs | research
- Status: planned | in_progress | done | blocked
- Branch:
- Base branch: dev
- Feature group:
- Task order:
- Summary:
- Related scenarios:
- Related tests:
- Verification evidence:
```
