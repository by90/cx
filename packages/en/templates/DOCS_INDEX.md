# docs/INDEX.md

This file is the index and instruction page for the `docs/` root. In multi-feature projects, the `docs/` root keeps only indexes and instructions long term; concrete engineering documents live in feature-group directories.

## Documentation Layout

```text
docs/INDEX.md
docs/<feature-group>/ENGINEERING_SPEC.md
docs/<feature-group>/CHANGELOG.md
```

Single-feature projects may temporarily use:

```text
docs/ENGINEERING_SPEC.md
docs/CHANGELOG.md
```

## Feature Group Index

| Group ID | Folder | Goal | Changes | BDD IDs | Reusable components | Status | Dependencies |
| --- | --- | --- | --- | --- | --- | --- | --- |
| core | `docs/core/` | TODO | TODO | TODO | TODO | planned | TODO |

## Notes

- Each feature-group directory maintains its own `ENGINEERING_SPEC.md` and `CHANGELOG.md`.
- Every `CHANGE-*` entry must map back to the same feature group's engineering spec.
- Register reusable components first in the owning feature group's Reusable Component Registry; also mark cross-feature reuse in this index.
