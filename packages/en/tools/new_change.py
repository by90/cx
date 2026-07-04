#!/usr/bin/env python3
"""Create one change document under a docs/cx scenario changes directory."""

from __future__ import annotations

import re  # re validates scenario names, task numbers, and filename fragments.
from pathlib import Path  # Path builds cross-platform filesystem paths.


SCENARIO_FOLDER_RE = re.compile(r"\d{2}\..+\Z")  # Scenario folders look like 01.create_user.
TASK_NUMBER_RE = re.compile(r"\d{2}\Z")  # Task numbers are exactly two digits.
SAFE_NAME_RE = re.compile(r'[\\/:*?"<>|\r\n\t]+')  # These characters are unsafe in Windows filenames.


def normalize_scenario_name(scenario: str) -> str:
    """Normalize a scenario path to a scenario folder name."""

    normalized = scenario.strip().strip("/\\")  # Remove surrounding whitespace and separators.
    normalized = normalized.replace("\\", "/")  # Normalize Windows separators.
    if normalized.startswith("docs/cx/"):  # Accept a docs/cx-prefixed scenario path.
        normalized = normalized[len("docs/cx/") :]  # Strip the fixed prefix.
    if "/" in normalized:  # A scenario name cannot include nested paths.
        raise ValueError("scenario must look like 01.create_user")  # Report the required format.
    if not SCENARIO_FOLDER_RE.fullmatch(normalized):  # The name must be two digits plus a dot.
        raise ValueError("scenario must look like 01.create_user")  # Report the required format.
    return normalized  # Return the normalized scenario folder name.


def normalize_task_number(task_number: int | str) -> str:
    """Normalize a task number to two digits."""

    if isinstance(task_number, int):  # Integer task numbers need padding.
        normalized = f"{task_number:02d}"  # Convert to two digits.
    else:  # String task numbers are caller-provided identifiers.
        normalized = task_number.strip()  # Remove surrounding whitespace.
    if not TASK_NUMBER_RE.fullmatch(normalized):  # Task numbers must be exactly two digits.
        raise ValueError("task_number must look like 01")  # Report the required format.
    return normalized  # Return the normalized task number.


def safe_filename_part(value: str) -> str:
    """Convert a task name into a safe filename part."""

    cleaned = SAFE_NAME_RE.sub("", value.strip())  # Remove unsafe path characters.
    cleaned = re.sub(r"\s+", "_", cleaned)  # Convert whitespace to underscores.
    if not cleaned:  # Empty names cannot create readable files.
        raise ValueError("task_name must not be empty")  # Report the task-name requirement.
    return cleaned  # Return the safe filename part.


def change_path_for(
    root: Path,
    scenario: str,
    task_number: int | str,
    task_name: str,
) -> Path:
    """Compute the change document path."""

    scenario_name = normalize_scenario_name(scenario)  # Normalize the scenario folder name.
    normalize_task_number(task_number)  # Validate the task number before writing a change under it.
    safe_task_name = safe_filename_part(task_name)  # Normalize the task name for filenames.
    filename = f"{safe_task_name}.md"  # Build the timestamp-free change filename.
    return root / "docs" / "cx" / scenario_name / "changes" / filename  # Return the full change path.


def build_change_text(
    task_number: str,
    task_name: str,
    previous: str,
    current: str,
    status: str = "open",
) -> str:
    """Render a change document as Markdown."""

    return (  # Use fixed headings so AI can parse the handoff.
        "# Change\n\n"
        f"## Status\n{status}\n\n"
        f"## Task\n{task_number}\n\n"
        f"## Task Name\n{task_name}\n\n"
        f"## What Was Done Before\n{previous}\n\n"
        f"## What Should Happen Now\n{current}\n"
    )  # Return the complete Markdown text.


def create_change_document(
    root: Path,
    scenario: str,
    task_number: int | str,
    task_name: str,
    previous: str,
    current: str,
    status: str = "open",
) -> Path:
    """Create one change document and return its path."""

    task_id = normalize_task_number(task_number)  # Normalize the task number.
    path = change_path_for(root, scenario, task_id, task_name)  # Compute the target path.
    path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the changes directory exists.
    text = build_change_text(task_id, task_name, previous, current, status)  # Render the change document.
    path.write_text(text, encoding="utf-8")  # Write UTF-8 Markdown.
    return path  # Return the generated path.


def main() -> int:
    """Reject command-line-parameter use for change creation."""

    print("Call create_change_document(...) from controlled automation; this script accepts no command-line parameters.")  # Explain the intended use.
    return 1  # Return failure to avoid pretending a change was created.


if __name__ == "__main__":
    raise SystemExit(main())  # Use main's return value as the process exit code.
