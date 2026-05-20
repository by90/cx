# docs/INDEX.md

This file is the index and instruction page for the `docs/` root. Every project is organized as multiple feature groups, so the `docs/` root keeps only indexes, instructions, and the version index long term; concrete engineering documents live in feature-group directories.

## Documentation Layout

```text
docs/INDEX.md
docs/VERSIONS.md
docs/001_project_template/ENGINEERING_SPEC.md
docs/001_project_template/CHANGELOG.md
docs/001_project_template/GUIDE.md
docs/002_next_feature/ENGINEERING_SPEC.md
docs/002_next_feature/CHANGELOG.md
docs/002_next_feature/GUIDE.md
```

## Feature Group Index

| Group ID | Folder | Goal | Changelog | BDD IDs | Reusable components | Status | Dependencies |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 001 | `docs/001_project_template/` | TODO | `docs/001_project_template/CHANGELOG.md` | TODO | TODO | planned | TODO |

## Version Index

After a feature group is complete and merged into `dev`, use the project-local `tools/semver.py` to append a release entry to `docs/VERSIONS.md`, for example `v0.0.1 "Create project template"`.

During `0.x.x`, new feature groups bump minor only: `python tools/semver.py next feature-group --root .`. Changes, bug fixes, or adjustments inside an existing feature group bump patch only: `python tools/semver.py next patch --root .`.

## Notes

- Each feature-group directory must use a three-digit order prefix, lowercase words, and underscores, and maintain its own `ENGINEERING_SPEC.md`, `CHANGELOG.md`, and `GUIDE.md`.
- Concrete change IDs belong only in the same feature group's `CHANGELOG.md`; do not copy them into BDD or the engineering spec.
- Do not create BDD automatically for ordinary non-programming tasks; ask the user first when behavior discovery is unclear.
- In principle, each feature group or change uses its own work branch, then merges into `dev` and deletes the work branch after completion.
- Register reusable features, classes, or components first in the owning feature group's Reusable Capability Registry; also mark cross-feature reuse in this index.
