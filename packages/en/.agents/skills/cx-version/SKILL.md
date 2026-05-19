---
name: cx-version
description: Use for cx package release version management, SemVer bump decisions, Keep a Changelog release notes, annotated Git tags, GitHub Releases, and release validation evidence.
version: 1.0.0
---

# cx Release Version Management

## Purpose

Use this skill when preparing, reviewing, or explaining a cx package release. The release mechanism is intentionally standard: one SemVer version value, one human-readable changelog, one annotated Git tag, and optional GitHub Release notes generated from the changelog.

## Standard Mechanism

1. `VERSION` at the repository root is the single source of truth. It stores the SemVer value only, such as `2.0.0`, without a leading `v`.
2. `packages/en/manifest.json` and `packages/zh/manifest.json` must copy the exact same version from `VERSION`.
3. The root `CHANGELOG.md` follows Keep a Changelog. Keep `## [Unreleased]` at the top, then add `## [X.Y.Z] - YYYY-MM-DD` for each release.
4. Git release tags use the common `vX.Y.Z` tag name. The tag name has the `v` prefix; the SemVer value does not.
5. Use annotated Git tags for releases, for example `git tag -a v2.0.0 -m "Release 2.0.0"`.
6. GitHub Releases, when used, should point at the matching tag and use the changelog section as the release notes.
7. Run `python tools/cx_version.py check .` and `python tools/validate_release.py .` before tagging.

## Version Bump Rules

- `1.0.0`: first stable public workflow/API contract.
- Major: incompatible public contract changes, such as removing or renaming a public skill, agent, install path, CLI command, document-set rule, prompt contract, or workflow API.
- Minor: backward-compatible public interface or workflow capability changes, such as adding a skill, agent, template, optional field, validation command, or compatible workflow path.
- Patch: wording fixes, validation bug fixes, examples, translations, or implementation fixes that do not change the public workflow/API contract.
- Prerelease: use SemVer prerelease identifiers such as `2.1.0-rc.1` only when the release is intentionally not final.

If an interface changes, classify compatibility first: compatible additions use minor versions such as `1.1.0`; breaking changes use major versions such as `2.0.0`.

## Release Checklist

1. Decide the next version from the public workflow impact.
2. Update `VERSION` and both package manifests.
3. Move user-visible changes from `CHANGELOG.md` `Unreleased` into the new release section.
4. Run version and release validation.
5. Commit the release files.
6. Create an annotated tag named `vX.Y.Z`.
7. Publish a GitHub Release when a public release page or downloadable archive is needed.
