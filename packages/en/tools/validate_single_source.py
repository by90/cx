#!/usr/bin/env python3
"""Validate the docs/cx use-case, task, and change single-source policy.

This file exposes `validate_single_source` for checking project-level docs, scenario folders,
task documents, and change documents under `docs/cx`. Main classes are `ScenarioFolder` and
`ValidationReport`.
"""

from __future__ import annotations

import re  # Use regular expressions for stable folder and file naming checks.
from dataclasses import dataclass  # Use dataclasses for immutable validation data objects.
from pathlib import Path  # Use Path for object-oriented cross-platform filesystem paths.


SCENARIO_FOLDER_RE = re.compile(r"\d{2}\..+\Z")  # A main success scenario folder looks like 01.create_user.
TASK_DOCUMENT_RE = re.compile(r"\d{2}\..+\.md\Z")  # A task document looks like 01.write_user_entity.md.
TIMESTAMPED_CHANGE_FILE_RE = re.compile(r"\d{8}T\d{6}")  # Change filenames must not carry timestamps.
LEGACY_CX_FILE_NAMES = {"B" + "DD.md", "ENGINEERING" + "_SPEC.md", "CHANGE" + "LOG.md", "GUIDE.md"}  # Old cx files are not allowed.
LEGACY_CX_TEXT_RE = re.compile(r"\bB" + r"DD\b|\bGher" + r"kin\b|ENGINEERING" + r"_SPEC|CHANGE" + r"LOG")  # Old workflow words are not allowed in cx docs.
RESERVED_CX_DIRECTORIES = {"docs", "notes"}  # Topic documents and research notes are not scenario folders.
CHANGE_REQUIRED_HEADINGS = (
    "## Status",
    "## Related objects",
    "## Current facts",
    "## Target state",
    "## Major changes",
    "## Ordered work list",
    "## File scope",
    "## Verification",
    "## Completion action",
)  # Every temporary change must fully describe the current instruction and deletion condition.


@dataclass(frozen=True)
class ScenarioFolder:
    """Represent one main success scenario folder under docs/cx."""

    root_relative: str  # Store a user-facing relative path like docs/cx/01.create_user.
    directory: Path  # Store the real scenario directory path.
    usecase_path: Path  # Store the use-case document path.
    design_path: Path  # Store the design document path.
    tasks_path: Path  # Store the tasks directory path.
    changes_path: Path  # Store the changes directory path.


@dataclass(frozen=True)
class ValidationReport:
    """Return validation success, errors, and warnings as one object."""

    ok: bool  # True means no blocking errors were found.
    errors: tuple[str, ...]  # Store blocking validation errors.
    warnings: tuple[str, ...]  # Store non-blocking validation warnings.


class ScenarioScanner:
    """Scan docs/cx without spreading filesystem traversal across validators."""

    def __init__(self, root: Path = Path(".")) -> None:
        """Create a scanner.

        `root` is the target repository root; this method stores paths and returns no value.
        """

        self.root = root  # Store the repository root for later scans.
        self.docs_dir = root / "docs"  # Store the docs root for legacy-file checks.
        self.cx_dir = self.docs_dir / "cx"  # Store the new cx single-source root.

    def scenario_folders(self) -> list[ScenarioFolder]:
        """Return all direct main success scenario folders under docs/cx."""

        if not self.cx_dir.exists():  # Missing docs/cx means there are no scenarios to scan.
            return []  # Return an empty list and let the caller report the missing root.
        folders: list[ScenarioFolder] = []  # Collect scenario folders in a stable list.
        for child in sorted(self.cx_dir.iterdir()):  # Iterate direct docs/cx children by name.
            if child.is_dir() and child.name not in RESERVED_CX_DIRECTORIES:  # Exclude topic and research-note directories.
                folders.append(self._build_scenario(child))  # Convert the directory to a structured object.
        return folders  # Return all discovered scenario folders.

    def legacy_cx_files(self) -> list[Path]:
        """Return old fixed-name cx files still present under docs."""

        if not self.docs_dir.exists():  # Without docs there are no old files to scan.
            return []  # Return an empty list and let docs/cx validation handle the root error.
        return sorted(  # Sort results so error output is stable.
            path  # Return each matching path.
            for path in self.docs_dir.rglob("*")  # Recursively scan docs.
            if path.is_file() and path.name in LEGACY_CX_FILE_NAMES  # Match only old fixed cx names.
        )

    def _build_scenario(self, directory: Path) -> ScenarioFolder:
        """Convert a directory into a `ScenarioFolder`.

        `directory` is the scenario candidate; the return value contains all convention paths.
        """

        return ScenarioFolder(  # Build an immutable scenario path object.
            root_relative=f"docs/cx/{directory.name}",  # Store the user-facing path.
            directory=directory,  # Store the real directory path.
            usecase_path=directory / "00.use_case.md",  # Store the English use-case path.
            design_path=directory / "00.design.md",  # Store the English design path.
            tasks_path=directory / "tasks",  # Store the tasks directory path.
            changes_path=directory / "changes",  # Store the changes directory path.
        )


def read_text(path: Path) -> str:
    """Read UTF-8 text, returning an empty string for missing files."""

    if path.exists():  # Read only existing files to avoid masking other validation errors.
        return path.read_text(encoding="utf-8")  # cx text files use UTF-8 without BOM.
    return ""  # Missing files produce empty text for downstream checks.


def markdown_files(directory: Path) -> list[Path]:
    """Return direct Markdown files under one directory."""

    if not directory.exists():  # Missing directories contain no Markdown files.
        return []  # Return an empty list to keep callers simple.
    return sorted(path for path in directory.glob("*.md") if path.is_file())  # Collect only direct Markdown files.


def validate_scenario_folder(scenario: ScenarioFolder) -> tuple[list[str], list[str]]:
    """Validate one main success scenario folder."""

    errors: list[str] = []  # Collect blocking errors for this scenario.
    warnings: list[str] = []  # Collect non-blocking warnings for this scenario.
    if not SCENARIO_FOLDER_RE.fullmatch(scenario.directory.name):  # The scenario folder must use two digits and a dot.
        errors.append(f"scenario folder must be named like docs/cx/01.create_user: {scenario.root_relative}")  # Report bad naming.
    if not scenario.usecase_path.exists():  # Every scenario needs a use-case document.
        errors.append(f"missing {scenario.root_relative}/00.use_case.md")  # Report a missing use-case document.
    if not scenario.design_path.exists():  # Every scenario needs a design document.
        errors.append(f"missing {scenario.root_relative}/00.design.md")  # Report a missing design document.
    if not scenario.tasks_path.is_dir():  # Every scenario needs tasks.
        errors.append(f"missing {scenario.root_relative}/tasks/")  # Report a missing tasks directory.
    if not scenario.changes_path.is_dir():  # Every scenario needs changes.
        errors.append(f"missing {scenario.root_relative}/changes/")  # Report a missing changes directory.
    errors.extend(validate_task_root(scenario))  # Merge task-root errors.
    errors.extend(validate_change_root(scenario))  # Merge change-root errors.
    errors.extend(validate_legacy_text(scenario))  # Merge old-wording errors.
    if not markdown_files(scenario.changes_path):  # No changes means AI has no change-first work source.
        warnings.append(f"no change documents found in {scenario.root_relative}/changes/")  # Warn without blocking.
    return errors, warnings  # Return scenario validation results.


def validate_task_root(scenario: ScenarioFolder) -> list[str]:
    """Validate the tasks directory for one scenario."""

    errors: list[str] = []  # Collect task errors.
    if not scenario.tasks_path.exists():  # The caller already reports a missing tasks directory.
        return errors  # Stop scanning this missing directory.
    task_files = markdown_files(scenario.tasks_path)  # Collect task Markdown files directly under tasks/.
    task_dirs = sorted(path for path in scenario.tasks_path.iterdir() if path.is_dir())  # Collect old-style task directories.
    for task_dir in task_dirs:  # Reject old-style task directories.
        errors.append(f"task documents must be files under tasks/, not directory: {scenario.root_relative}/tasks/{task_dir.name}")  # Report the old task folder.
    if not task_files:  # A scenario needs at least one task document.
        errors.append(f"missing task documents under {scenario.root_relative}/tasks/")  # Report an empty task list.
    for task_file in task_files:  # Validate each task document.
        task_path = task_file.relative_to(scenario.directory).as_posix()  # Build the scenario-relative task path.
        if task_file.name == "00.task.md":  # Generic task filenames hide the task concern.
            errors.append(f"task document must be named like tasks/01.write_user_entity.md, not {task_path}")  # Report the generic task file.
        elif not TASK_DOCUMENT_RE.fullmatch(task_file.name):  # Task files must use a numbered name.
            errors.append(f"task document must be named like tasks/01.write_user_entity.md: {scenario.root_relative}/{task_path}")  # Report bad task naming.
    return errors  # Return task errors.


def validate_change_root(scenario: ScenarioFolder) -> list[str]:
    """Validate the changes directory for one scenario."""

    errors: list[str] = []  # Collect change errors.
    if not scenario.changes_path.exists():  # The caller already reports a missing changes directory.
        return errors  # Stop scanning this missing directory.
    for child in sorted(scenario.changes_path.iterdir()):  # Iterate change children stably.
        if child.is_dir():  # Changes should be files, not nested directories.
            errors.append(f"change documents must be files, not directory: {scenario.root_relative}/changes/{child.name}")  # Report nested change dirs.
    for change_file in markdown_files(scenario.changes_path):  # Validate each change document.
        if TIMESTAMPED_CHANGE_FILE_RE.search(change_file.name):  # Change filenames must stay timestamp-free.
            errors.append(f"change file must not contain timestamp: {scenario.root_relative}/changes/{change_file.name}")  # Report bad change naming.
        change_text = read_text(change_file)  # Read the change document.
        for heading in CHANGE_REQUIRED_HEADINGS:  # Check every required heading.
            if heading not in change_text:  # Missing headings prevent AI from resuming work safely.
                errors.append(f"missing heading {heading} in {scenario.root_relative}/changes/{change_file.name}")  # Report the missing heading.
    return errors  # Return change errors.


def validate_legacy_text(scenario: ScenarioFolder) -> list[str]:
    """Validate that scenario documents do not carry old workflow wording."""

    errors: list[str] = []  # Collect old-wording errors.
    for doc_path in sorted(scenario.directory.rglob("*.md")):  # Scan every Markdown file in this scenario.
        text = read_text(doc_path)  # Read the document text.
        if LEGACY_CX_TEXT_RE.search(text):  # New cx documents should not contain old workflow terms.
            relative_path = doc_path.relative_to(scenario.directory).as_posix()  # Build a scenario-relative path.
            errors.append(f"legacy cx wording is not allowed in {scenario.root_relative}/{relative_path}")  # Report old wording.
    return errors  # Return old-wording errors.


def validate_single_source(root: Path = Path(".")) -> ValidationReport:
    """Validate the target repository's docs/cx single-source rules."""

    scanner = ScenarioScanner(root)  # Create a scanner for the target repository.
    errors: list[str] = []  # Collect all blocking errors.
    warnings: list[str] = []  # Collect all non-blocking warnings.
    if not scanner.cx_dir.is_dir():  # docs/cx must exist.
        errors.append("missing docs/cx directory")  # Report the missing root.
        return ValidationReport(ok=False, errors=tuple(errors), warnings=tuple(warnings))  # Return early without docs/cx.
    for legacy_path in scanner.legacy_cx_files():  # Look for old fixed files under docs.
        errors.append(f"legacy cx document is not allowed: {legacy_path.relative_to(root).as_posix()}")  # Report old files.
    scenarios = scanner.scenario_folders()  # Discover scenario folders.
    if not scenarios:  # At least one scenario is needed.
        errors.append("missing docs/cx/01.main_success_scenario folder")  # Report missing scenarios.
    for scenario in scenarios:  # Validate every scenario.
        scenario_errors, scenario_warnings = validate_scenario_folder(scenario)  # Validate one scenario.
        errors.extend(scenario_errors)  # Merge scenario errors.
        warnings.extend(scenario_warnings)  # Merge scenario warnings.
    return ValidationReport(ok=not errors, errors=tuple(errors), warnings=tuple(warnings))  # Return the full report.


def main() -> int:
    """Run docs/cx validation from the current working directory."""

    report = validate_single_source(Path(".").resolve())  # Validate the current repository without command-line parameters.
    for warning in report.warnings:  # Print every warning.
        print(f"WARN  {warning}")  # Prefix warnings for readability.
    for error in report.errors:  # Print every error.
        print(f"ERROR {error}")  # Prefix errors for readability.
    if report.ok:  # No errors means success.
        print("OK docs/cx single-source policy passed")  # Print success output.
        return 0  # Return success.
    return 1  # Return failure when any error exists.


if __name__ == "__main__":
    raise SystemExit(main())  # Use main's return value as the process exit code.
