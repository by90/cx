# docs/INDEX.md

This file is the index and instruction page for the `docs/` root. In multi-feature projects, the `docs/` root keeps only indexes, instructions, and the version index long term; concrete engineering documents live in feature-group directories.

## Documentation Layout

```text
docs/INDEX.md
docs/VERSIONS.md
docs/<feature-group>/ENGINEERING_SPEC.md
docs/<feature-group>/CHANGELOG.md
docs/<feature-group>/GUIDE.md
```

Single-feature projects may temporarily use:

```text
docs/ENGINEERING_SPEC.md
docs/CHANGELOG.md
docs/GUIDE.md
```

## Feature Group Index

| Group ID | Folder | Goal | Changelog | BDD IDs | Reusable components | Status | Dependencies |
| --- | --- | --- | --- | --- | --- | --- | --- |
| core | `docs/core/` | TODO | `docs/core/CHANGELOG.md` | TODO | TODO | planned | TODO |

## Version Index

After a feature group is complete and merged into `dev`, use the version tool to append a release entry to `docs/VERSIONS.md`, for example `v0.0.1 "Create project template"`.

## Notes

- Each feature-group directory maintains its own `ENGINEERING_SPEC.md`, `CHANGELOG.md`, and optional `GUIDE.md`.
- Concrete change IDs belong only in the same feature group's `CHANGELOG.md`; do not copy them into the BDD spec.
- In principle, each feature group or change uses its own work branch, then merges into `dev` and deletes the work branch after completion.
- Register reusable components first in the owning feature group's Reusable Component Registry; also mark cross-feature reuse in this index.
