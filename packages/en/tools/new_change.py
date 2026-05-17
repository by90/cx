#!/usr/bin/env python3
"""Append one CHANGE entry to the target documentation set changelog."""

from __future__ import annotations

import argparse  # argparse turns command-line arguments into Python values.
import datetime as dt  # datetime provides the default date.
import re  # re finds existing CHANGE IDs with a regular expression.
from pathlib import Path  # Path joins filesystem paths safely across platforms.


CHANGE_ID_RE = re.compile(r"CHANGE-(\d{4})-(\d{3})")  # Match CHANGE-year-number IDs.
ROOT_DOC_SET_NAMES = {"", ".", "docs", "root"}  # These names mean the root docs set.
DEFAULT_CHANGELOG = "# CHANGELOG.md\n\n## Unreleased\n"  # Minimum text for a new changelog.


def next_change_id(changelog_text: str, year: int) -> str:
    """Generate the next CHANGE ID for the given year and changelog text."""

    numbers = [  # Collect numbers that already exist for this year.
        int(match.group(2))  # The second group is the three-digit sequence number.
        for match in CHANGE_ID_RE.finditer(changelog_text)  # Visit every CHANGE ID in the changelog.
        if int(match.group(1)) == year  # Count only IDs from the target year.
    ]
    next_number = max(numbers, default=0) + 1  # Start at 1 or advance past the largest number.
    return f"CHANGE-{year}-{next_number:03d}"  # Format the sequence as three digits.


def changelog_path_for(root: Path, doc_set: str | None) -> Path:
    """Return the changelog path for a root or feature documentation set."""

    normalized = (doc_set or "").strip().strip("/\\")  # Remove whitespace and edge separators.
    if normalized in ROOT_DOC_SET_NAMES:  # Root-style names use docs/CHANGELOG.md.
        return root / "docs" / "CHANGELOG.md"  # Return the root changelog path.
    if normalized.startswith("docs/") or normalized.startswith("docs\\"):  # Accept docs/<group> input.
        normalized = normalized[5:]  # Strip docs/ so the path is not duplicated.
    return root / "docs" / normalized / "CHANGELOG.md"  # Return the feature-group changelog path.


def build_entry(
    change_id: str,
    title: str,
    change_type: str,
    today: str,
    branch: str,
    base_branch: str,
    feature_group: str,
) -> str:
    """Render one CHANGE entry as Markdown."""

    return f"""
### {change_id} - {title}

- Date: {today}
- Type: {change_type}
- Status: planned
- Branch: {branch}
- Base branch: {base_branch}
- Feature group: {feature_group}
- Summary: TODO
- Related scenarios: TODO
- Related tests: TODO
- Verification evidence: TODO
""".strip()  # Trim template edges so insertion controls blank lines.


def append_under_unreleased(text: str, entry: str) -> str:
    """Append a new entry to the end of the Unreleased section."""

    if "## Unreleased" not in text:  # Add the section when an older file lacks it.
        return text.rstrip() + f"\n\n## Unreleased\n\n{entry}\n"  # Place the entry in the new section.
    header_index = text.index("## Unreleased")  # Find the Unreleased heading.
    search_start = header_index + len("## Unreleased")  # Start searching after the heading text.
    next_header_index = text.find("\n## ", search_start)  # The next level-two heading ends the section.
    if next_header_index == -1:  # No later release section means append to the file end.
        return text.rstrip() + f"\n\n{entry}\n"  # Preserve existing order, then append the new entry.
    before = text[:next_header_index].rstrip()  # Keep existing Unreleased content.
    after = text[next_header_index:]  # Keep later release sections unchanged.
    return before + f"\n\n{entry}\n" + after  # Insert at the end of Unreleased.


def append_change(
    root: Path,
    title: str,
    change_type: str,
    doc_set: str | None = None,
    today: str | None = None,
    branch: str = "TODO",
    base_branch: str = "dev",
) -> str:
    """Create a CHANGE ID and write it to the target changelog."""

    changelog_path = changelog_path_for(root, doc_set)  # Choose the target changelog.
    changelog_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the docs directory exists.
    text = changelog_path.read_text(encoding="utf-8") if changelog_path.exists() else DEFAULT_CHANGELOG  # Read or create text.
    actual_today = today or dt.date.today().isoformat()  # Use today's date when none is provided.
    year = int(actual_today[:4])  # The year segment controls the CHANGE ID group.
    change_id = next_change_id(text, year)  # Generate the next stable ID.
    feature_group = doc_set or "root"  # Record which feature group owns this change.
    entry = build_entry(change_id, title, change_type, actual_today, branch, base_branch, feature_group)  # Build Markdown.
    updated_text = append_under_unreleased(text, entry)  # Append to the Unreleased section.
    changelog_path.write_text(updated_text, encoding="utf-8")  # Save the updated changelog as UTF-8.
    return change_id  # Return the ID for scripts and tests.


def main() -> int:
    """Append a CHANGE entry from the command line."""

    parser = argparse.ArgumentParser(description="Append a CHANGE-* entry to a target docs changelog.")  # Create parser.
    parser.add_argument("title")  # Read the change title.
    parser.add_argument("--type", default="feature", choices=["feature", "bugfix", "refactor", "test", "docs", "research"])  # Read type.
    parser.add_argument("--root", default=".")  # Read repository root.
    parser.add_argument("--doc-set", default=None)  # Read target documentation set.
    parser.add_argument("--branch", default="TODO")  # Read work branch.
    parser.add_argument("--base-branch", default="dev")  # Read merge target branch.
    parser.add_argument("--date", default=None)  # Let automation pass a fixed date.
    args = parser.parse_args()  # Parse every argument.

    change_id = append_change(  # Call the reusable helper.
        Path(args.root).resolve(),  # Resolve the root path.
        args.title,  # Pass the title.
        args.type,  # Pass the change type.
        doc_set=args.doc_set,  # Pass the target docs set.
        today=args.date,  # Pass the optional date.
        branch=args.branch,  # Pass the work branch.
        base_branch=args.base_branch,  # Pass the merge target branch.
    )
    print(change_id)  # Print the new ID for the user or calling script.
    return 0  # Return success.


if __name__ == "__main__":
    raise SystemExit(main())  # Use main's return value as the process exit code.
