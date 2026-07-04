---
name: cx-version
description: Use for project release version management, project-local SemVer tool calls, bump decisions, docs/VERSIONS.md, annotated Git tags, GitHub Releases, and release validation evidence.
version: 0.1.0
---

# cx Release Version Management

## Language Rules

- Use the package language for conversations, explanations, plans, summaries, review decisions, verification evidence, and cx documents. Do not mix languages inside prose fragments or term lists.
- In Chinese-package work, if an English identifier, command, path, API name, library, protocol, standard, proper name, or ambiguity-sensitive term must remain in English, explain its meaning, role, and local context in Chinese in the same sentence or an adjacent sentence. In English-package work, explain unavoidable non-English terms in English.

## Purpose

Use this skill when preparing, reviewing, or explaining a project release. The release mechanism must be standardized and should use the target project's non-interactive version tool first:

```bash
python tools/semver.py check --root .
python tools/semver.py next feature-group --root .
python tools/semver.py next patch --root .
python tools/semver.py prepare <version> "<title>" --root .
python tools/semver.py tag --root .
```

When Codex App needs structured output, append `--json` to `check`, `next`, or `prepare`.

If the target project does not have the tool yet, copy this skill directory's `scripts/semver.py` to the target project's `tools/semver.py`, and make sure the target project has `VERSION` and `docs/VERSIONS.md`.

## Standard Mechanism

1. The target project must provide `tools/semver.py`, or copy an equivalent implementation from this skill's `scripts/semver.py` before release. Do not hand-write `docs/VERSIONS.md` entries instead of using the tool.
2. `VERSION` at the repository root is the single source of truth. It stores the SemVer value only, such as `0.1.0`, without a leading `v`.
3. If the project has `pyproject.toml`, `[project].version` must match `VERSION` exactly and be synchronized by `tools/semver.py prepare`.
4. `docs/VERSIONS.md` is the human-facing version record. Headings use `## vX.Y.Z - Title`.
5. Git release tags use `vX.Y.Z`. The tag has the `v` prefix; the `VERSION` value does not.
6. Use annotated Git tags for releases, for example `git tag -a v0.1.0 -m "Release 0.1.0"`; normally create them with `python tools/semver.py tag --root .`.
7. Release commits and release tags are allowed only on `main`. Work branches stay local by default and must not be pushed unless the user explicitly overrides the main-only remote policy; the remote should keep only `main` and version tags.
8. The cx package itself may still use the repository-root `tools/cx_version.py` and `tools/validate_release.py`; target project releases must prefer the target project's `tools/semver.py`.

## Version Bump Rules

- Default start: new or unproven projects start at `0.0.1` unless the user explicitly says the project has reached `1.0.0`.
- Default bump: when the user only asks to update, bump, or prepare the version without explicitly saying minor, major, new feature group, stable release, or incompatible release, bump only the final patch segment.
- Major `0`: the project is not formally stable; public interface and workflow-contract changes are normal.
- Adding a feature group during `0.x.x`: bump only the minor version. For example, adding a real feature group at `0.1.3` should produce `0.2.0`. Verify with `python tools/semver.py next feature-group --root .`.
- Changes, bug fixes, documentation adjustments, implementation fixes, or small refactors inside an existing feature group during `0.x.x`: bump only the patch version. For example, fixing `002_config` at `0.1.3` should produce `0.1.4`. Verify with `python tools/semver.py next patch --root .`.
- A pre-1.0 public-contract change that does not add a feature group defaults to patch unless the user explicitly treats it as a new feature group or release milestone.
- `1.0.0`: first stable public workflow/API contract, only after the user explicitly declares the project stable.
- Post-1.0 minor: after `1.0.0`, minor bumps such as `1.1.0` mean backward-compatible public additions.
- Post-1.0 major: after `1.0.0`, major bumps such as `2.0.0` mean incompatible public-contract changes.
- Prerelease: use SemVer prerelease identifiers such as `0.2.0-rc.1` only when the release is intentionally not final.

## Release Checklist

1. Confirm the feature group or change work happened on its own local branch.
2. Decide the release type: default to `next patch` unless an earlier version segment was explicitly requested; use `next feature-group` only for a new feature group or explicit minor request; use `next patch` for existing feature-group changes, bug fixes, or adjustments.
3. Ask the user to confirm that this version is complete and ready for release.
4. After confirmation, merge the completed local work branch into `main` and delete the local branch.
5. On `main`, run `python tools/semver.py check --root .`.
6. On `main`, run `python tools/semver.py prepare <version> "<title>" --root . --feature-group <group> --summary "<summary>" --evidence "<evidence>"`.
7. On `main`, rerun project tests and `python tools/semver.py check --root .`.
8. On `main`, commit release files such as `VERSION`, `pyproject.toml`, and `docs/VERSIONS.md`.
9. On `main`, run `python tools/semver.py tag --root .` to create the annotated tag.
10. Push `main` and the release tag.
11. Create a GitHub Release when a public release page or downloadable archive is needed.

Never create release commits or release tags on work branches. Do not push work branches unless the user explicitly overrides the main-only remote policy in the current conversation.
