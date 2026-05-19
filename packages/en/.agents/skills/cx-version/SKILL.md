---
name: cx-version
description: Use for cx package release version management, SemVer bump decisions, Keep a Changelog release notes, annotated Git tags, GitHub Releases, and release validation evidence.
version: 0.0.1
---

# cx Release Version Management

## Purpose

Use this skill when preparing, reviewing, or explaining a cx package release. The release mechanism is intentionally standard: one SemVer version value, one human-readable changelog, one annotated Git tag, and optional GitHub Release notes generated from the changelog.

## Standard Mechanism

1. `VERSION` at the repository root is the single source of truth. It stores the SemVer value only, such as `0.0.1`, without a leading `v`.
2. `packages/en/manifest.json` and `packages/zh/manifest.json` must copy the exact same version from `VERSION`.
3. The root `CHANGELOG.md` follows Keep a Changelog. Keep `## [Unreleased]` at the top, then add `## [X.Y.Z] - YYYY-MM-DD` for each release.
4. Git release tags use the common `vX.Y.Z` tag name. The tag name has the `v` prefix; the SemVer value does not.
5. Use annotated Git tags for releases, for example `git tag -a v0.0.1 -m "Release 0.0.1"`.
6. GitHub Releases, when used, should point at the matching tag and use the changelog section as the release notes.
7. Release commits and release tags are allowed only on `main`. Run `python tools/cx_version.py check .` and `python tools/validate_release.py .` on `main` before tagging.

## Version Bump Rules

- Default start: new or unproven projects start at `0.0.1` unless the user explicitly says the project has reached `1.0.0`.
- Major `0`: the project is not formally released. Public interface and workflow contract changes are normal during this phase.
- Pre-1.0 minor: while major is `0`, use minor bumps such as `0.1.0` for interface changes, workflow contract changes, skill/agent additions, renamed workflows, or document-set rule changes.
- Pre-1.0 feature-group completion: when a feature group is completed and accepted, move from the `0.0.x` line to the next minor line, for example `0.1.0`. Keep major version `0` until the user explicitly confirms the project is stable.
- Pre-1.0 patch: while major is `0`, use patch bumps such as `0.0.2` for wording fixes, validation bug fixes, examples, translations, or implementation fixes that do not change the public contract.
- `1.0.0`: first stable public workflow/API contract, only after the project is complete and explicitly declared stable.
- Post-1.0 minor: after `1.0.0`, use minor bumps such as `1.1.0` for backward-compatible public additions.
- Post-1.0 major: after `1.0.0`, use major bumps such as `2.0.0` for incompatible public contract changes.
- Prerelease: use SemVer prerelease identifiers such as `0.2.0-rc.1` only when the release is intentionally not final.

If an interface changes before `1.0.0`, keep the major version at `0` and bump minor. Do not jump to `1.0.0` unless the user explicitly declares the project stable.

## Release Checklist

1. Confirm all work for the feature group happened on its own branch.
2. Merge the completed feature-group branch into `dev`; do not merge it directly into `main`.
3. Decide whether the project is still pre-1.0. If not explicitly stable, keep major version `0`.
4. Decide the next version from the public workflow impact. During pre-1.0 work, a completed feature group normally moves `0.0.x` to the next minor line such as `0.1.0`.
5. Ask the user to confirm that this version is complete and ready for release.
6. After confirmation, merge `dev` into `main`.
7. On `main` only, update `VERSION` and both package manifests.
8. On `main` only, move user-visible changes from `CHANGELOG.md` `Unreleased` into the new release section.
9. Run version and release validation on `main`.
10. Commit the release files on `main`.
11. Create an annotated tag named `vX.Y.Z` on `main`.
12. Push `main` and the release tag.
13. Publish a GitHub Release when a public release page or downloadable archive is needed.

Never create release commits or release tags on feature branches or on `dev`. This restriction does not forbid pushing feature branches or `dev`; it only restricts release-version actions to `main`.
