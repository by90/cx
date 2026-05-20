#!/usr/bin/env python3
"""Append one release version entry to docs/VERSIONS.md."""

from __future__ import annotations

import argparse  # argparse turns command-line arguments into Python values.
import datetime as dt  # datetime provides the default date.
import re  # re validates the version string.
from pathlib import Path  # Path joins filesystem paths safely.


VERSION_RE = re.compile(r"v\d+\.\d+\.\d+\Z")  # Match semantic versions like v0.0.1.
FEATURE_FOLDER_RE = re.compile(r"\d{3}_[a-z0-9]+(?:_[a-z0-9]+)*\Z")  # Match feature groups such as 001_project_template.
DEFAULT_VERSIONS = "# VERSIONS.md\n\n## Versions\n"  # Minimum text for a new version index.


def join_values(values: tuple[str, ...], fallback: str = "TODO") -> str:
    """Join multiple values into one Markdown-friendly line."""

    cleaned = [value.strip() for value in values if value.strip()]  # Drop empty values.
    if cleaned:  # Use caller-provided values when at least one remains.
        return ", ".join(cleaned)  # Join with commas for readability.
    return fallback  # Use the fallback when the caller has no values yet.


def validate_feature_groups(groups: tuple[str, ...]) -> None:
    """Ensure release entries only reference valid numbered feature groups."""

    for group in groups:  # Check every feature group supplied by the caller.
        if not FEATURE_FOLDER_RE.fullmatch(group):  # The group value must match the docs folder name.
            raise ValueError("feature group must look like 001_project_template")  # Tell callers how to fix the value.


def build_entry(
    version: str,
    title: str,
    today: str,
    groups: tuple[str, ...],
    changes: tuple[str, ...],
    release_branch: str,
) -> str:
    """Render version metadata as Markdown."""

    group_text = join_values(groups)  # Convert feature groups to one line.
    change_text = join_values(changes)  # Convert change IDs to one line.
    return f"""
## {version} - {title}

- Date: {today}
- Feature groups: {group_text}
- Changes: {change_text}
- Release branch: {release_branch}
- Summary: TODO
- Verification evidence: TODO
""".strip()  # Trim template edges so append logic controls blank lines.


def append_version(
    root: Path,
    version: str,
    title: str,
    today: str | None = None,
    groups: tuple[str, ...] = (),
    changes: tuple[str, ...] = (),
    release_branch: str = "dev",
) -> str:
    """Validate the version and write it to docs/VERSIONS.md."""

    if not VERSION_RE.fullmatch(version):  # Require explicit vX.Y.Z versions.
        raise ValueError("version must look like v0.0.1")  # Raise a clear correction message.
    validate_feature_groups(groups)  # The version index must only record numbered feature groups.
    versions_path = root / "docs" / "VERSIONS.md"  # Keep the version index at the docs root.
    versions_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure docs/ exists.
    text = versions_path.read_text(encoding="utf-8") if versions_path.exists() else DEFAULT_VERSIONS  # Read or create text.
    actual_today = today or dt.date.today().isoformat()  # Use today's date when none is provided.
    entry = build_entry(version, title, actual_today, groups, changes, release_branch)  # Build Markdown entry.
    updated_text = text.rstrip() + f"\n\n{entry}\n"  # Append versions in creation order.
    versions_path.write_text(updated_text, encoding="utf-8")  # Save the file as UTF-8.
    return version  # Return the version for tests and scripts.


def main() -> int:
    """Append a version entry from the command line."""

    parser = argparse.ArgumentParser(description="Append a version entry to docs/VERSIONS.md.")  # Create parser.
    parser.add_argument("version")  # Read version, such as v0.0.1.
    parser.add_argument("title")  # Read release title.
    parser.add_argument("--root", default=".")  # Read repository root.
    parser.add_argument("--date", default=None)  # Let automation pass a fixed date.
    parser.add_argument("--group", action="append", default=[])  # Accept repeated feature groups.
    parser.add_argument("--change", action="append", default=[])  # Accept repeated change IDs.
    parser.add_argument("--release-branch", default="dev")  # Read release source branch.
    args = parser.parse_args()  # Parse every argument.

    append_version(  # Call the reusable helper.
        Path(args.root).resolve(),  # Resolve the repository root.
        args.version,  # Pass the version.
        args.title,  # Pass the title.
        today=args.date,  # Pass the optional date.
        groups=tuple(args.group),  # Convert groups to an immutable tuple.
        changes=tuple(args.change),  # Convert changes to an immutable tuple.
        release_branch=args.release_branch,  # Pass the release source branch.
    )
    print(args.version)  # Print the version for scripts.
    return 0  # Return success.


if __name__ == "__main__":
    raise SystemExit(main())  # Use main's return value as the process exit code.
