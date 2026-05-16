---
name: cx-changelog
description: Use when updating changelogs, release notes, change IDs, audit trails, or ensuring CHANGE entries map back to the single engineering specification.
version: 1.0.0
---

# cx Changelog Curator

## Purpose

Maintain `docs/CHANGELOG.md` as a compact historical index. It must not become a second requirements document and must not duplicate long behavior descriptions.

## Rules

1. Every entry must have a stable `CHANGE-YYYY-NNN` ID.
2. Every entry must include date, type, summary, related engineering spec sections, BDD scenarios, tests, and evidence.
3. If the changelog entry has no matching engineering spec content, update the engineering spec first.
4. Do not copy long requirements into the changelog.
5. Do not create separate release-note documents unless the user explicitly asks.
6. Keep entries short enough to scan and concrete enough to audit.

## Entry template

```markdown
### CHANGE-YYYY-NNN - Title

- Date:
- Type: feature | bugfix | refactor | test | docs | research
- Summary:
- Engineering spec sections:
- Related BDD scenarios:
- Related tests:
- Verification evidence:
```
