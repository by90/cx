#!/usr/bin/env python3
"""Validate cx documentation-set layout for a target repository."""

from __future__ import annotations

import argparse  # argparse turns command-line arguments into Python objects.
import re  # re finds CHANGE IDs and BDD IDs with regular expressions.
from dataclasses import dataclass  # dataclass declares small result objects.
from pathlib import Path  # Path handles filesystem paths in an object-oriented way.


CHANGE_ID_RE = re.compile(r"CHANGE-\d{4}-\d{3}")  # Match stable change IDs.
BDD_ID_RE = re.compile(r"BDD-[A-Z0-9]+-\d{3}")  # Match stable behavior scenario IDs.
ROOT_INDEX_DOCS = {"INDEX.md", "README.md"}  # Root docs may keep index/instruction files.
DOC_SET_FILES = {"BDD.md", "ENGINEERING_SPEC.md", "CHANGELOG.md"}  # Each documentation set needs these files.
OPTIONAL_DOC_SET_FILES = {"INDEX.md", "README.md"}  # A doc-set folder may also include local notes.


@dataclass(frozen=True)
class DocSet:
    """Describe one folder that owns an engineering spec and changelog."""

    root_relative: str  # User-facing relative path for error messages.
    directory: Path  # Actual directory path for file checks.
    spec_path: Path  # Full path to ENGINEERING_SPEC.md.
    changelog_path: Path  # Full path to CHANGELOG.md.


@dataclass(frozen=True)
class ValidationReport:
    """Return validation success, errors, and warnings as one object."""

    ok: bool  # True means there are no errors.
    errors: tuple[str, ...]  # Errors are issues that must be fixed.
    warnings: tuple[str, ...]  # Warnings are issues worth attention.


def read_text(path: Path) -> str:
    """Read UTF-8 text, returning an empty string when the file is absent."""

    if path.exists():  # Read only when the file exists.
        return path.read_text(encoding="utf-8")  # cx documents are UTF-8 text.
    return ""  # Missing files return empty text so validation can continue.


def markdown_files(directory: Path) -> set[str]:
    """Return Markdown file names directly inside one directory."""

    if not directory.exists():  # A missing directory has no Markdown files.
        return set()  # Return an empty set for easy set operations.
    return {path.name for path in directory.glob("*.md") if path.is_file()}  # Collect only direct file names.


def discover_doc_sets(root: Path) -> list[DocSet]:
    """Find root or feature-folder documentation sets under docs/."""

    docs_dir = root / "docs"  # All long-lived docs live under docs/.
    doc_sets: list[DocSet] = []  # Store every discovered documentation set.
    root_spec = docs_dir / "ENGINEERING_SPEC.md"  # Root-set engineering spec path.
    root_changelog = docs_dir / "CHANGELOG.md"  # Root-set changelog path.
    if root_spec.exists() or root_changelog.exists():  # Either core file makes the root a candidate set.
        doc_sets.append(  # Save the root documentation set for later validation.
            DocSet(
                root_relative="docs",  # User-facing root docs path.
                directory=docs_dir,  # Root documentation set directory.
                spec_path=root_spec,  # Root engineering spec file.
                changelog_path=root_changelog,  # Root changelog file.
            )
        )
    if docs_dir.exists():  # Scan children only when docs/ exists.
        for child in sorted(path for path in docs_dir.iterdir() if path.is_dir()):  # Inspect first-level feature folders.
            child_spec = child / "ENGINEERING_SPEC.md"  # Feature-set engineering spec path.
            child_changelog = child / "CHANGELOG.md"  # Feature-set changelog path.
            if child_spec.exists() or child_changelog.exists():  # Either core file makes the child a candidate set.
                doc_sets.append(  # Save this feature-group documentation set.
                    DocSet(
                        root_relative=f"docs/{child.name}",  # User-facing feature docs path.
                        directory=child,  # Feature documentation set directory.
                        spec_path=child_spec,  # Feature engineering spec file.
                        changelog_path=child_changelog,  # Feature changelog file.
                    )
                )
    return doc_sets  # Return every candidate documentation set.


def validate_doc_set(doc_set: DocSet) -> tuple[list[str], list[str]]:
    """Validate one documentation set and return errors plus warnings."""

    errors: list[str] = []  # Collect this set's errors.
    warnings: list[str] = []  # Collect this set's warnings.
    if doc_set.root_relative != "docs" and not re.fullmatch(r"\d+\..+", doc_set.directory.name):  # Feature folders are ordered.
        errors.append(f"feature documentation folder must be named like docs/1.Configuration System: {doc_set.root_relative}")  # Report bad naming.
    bdd_path = doc_set.directory / "BDD.md"  # BDD lives beside the engineering spec.
    if doc_set.root_relative != "docs" and not bdd_path.exists():  # Multi-feature sets must carry their BDD document.
        errors.append(f"missing {doc_set.root_relative}/BDD.md")  # Report missing BDD doc.
    if not doc_set.spec_path.exists():  # Every set needs an engineering spec.
        errors.append(f"missing {doc_set.root_relative}/ENGINEERING_SPEC.md")  # Report the missing spec.
    if not doc_set.changelog_path.exists():  # Every set needs a changelog.
        errors.append(f"missing {doc_set.root_relative}/CHANGELOG.md")  # Report the missing changelog.

    allowed = DOC_SET_FILES | OPTIONAL_DOC_SET_FILES  # Core files and local notes are allowed.
    for doc_name in sorted(markdown_files(doc_set.directory) - allowed):  # Find extra Markdown files.
        errors.append(f"unexpected long-lived docs file: {doc_set.root_relative}/{doc_name}")  # Block orphan docs.

    spec_text = read_text(doc_set.spec_path)  # Read the engineering spec text.
    bdd_text = read_text(bdd_path)  # Read the BDD document text.
    changelog_text = read_text(doc_set.changelog_path)  # Read the changelog text.
    change_ids_in_changelog = set(CHANGE_ID_RE.findall(changelog_text))  # Extract change IDs from changelog.
    change_ids_in_spec = set(CHANGE_ID_RE.findall(spec_text))  # Extract change IDs from spec.
    for change_id in sorted(change_ids_in_changelog - change_ids_in_spec):  # Every changelog change must map to spec.
        errors.append(  # Build a clear mapping error.
            f"{change_id} appears in {doc_set.root_relative}/CHANGELOG.md but not "
            f"{doc_set.root_relative}/ENGINEERING_SPEC.md"
        )

    if bdd_text and doc_set.root_relative != "docs":  # Check feature-name alignment when BDD exists.
        expected = doc_set.directory.name  # BDD title and Feature name should match this folder.
        if f"# BDD: {expected}" not in bdd_text and f"Feature: {expected}" not in bdd_text:  # Require at least one exact marker.
            errors.append(f"{doc_set.root_relative}/BDD.md must use the same BDD or Feature name as its folder")  # Report drift.

    bdd_ids = sorted(set(BDD_ID_RE.findall(spec_text + "\n" + bdd_text)))  # Extract BDD scenario IDs from docs.
    if doc_set.spec_path.exists() and not bdd_ids:  # A spec without BDD IDs is suspicious but not fatal.
        warnings.append(f"no BDD-* scenario IDs found in {doc_set.root_relative}/ENGINEERING_SPEC.md")  # Ask for behavior IDs.
    if bdd_ids and "## 6. Test Matrix" not in spec_text:  # BDD scenarios need test mappings.
        errors.append(f"BDD IDs exist but Test Matrix section is missing in {doc_set.root_relative}/ENGINEERING_SPEC.md")  # Report missing matrix.
    return errors, warnings  # Return this set's validation results.


def validate_single_source(root: Path, allowed_docs: set[str] | None = None) -> ValidationReport:
    """Validate either one root docs set or many feature-folder docs sets."""

    extra_allowed_docs = allowed_docs or set()  # Allow callers to whitelist extra root Markdown files.
    docs_dir = root / "docs"  # The docs directory is the long-lived documentation root.
    errors: list[str] = []  # Collect global errors.
    warnings: list[str] = []  # Collect global warnings.

    if not docs_dir.exists():  # A repository without docs/ cannot satisfy the policy.
        errors.append("missing docs directory")  # Report missing docs/.
        return ValidationReport(ok=False, errors=tuple(errors), warnings=tuple(warnings))  # Stop early.

    doc_sets = discover_doc_sets(root)  # Discover root and feature documentation sets.
    if not doc_sets:  # At least one documentation set is required.
        errors.append("missing docs/ENGINEERING_SPEC.md or docs/<feature-group>/ENGINEERING_SPEC.md")  # Report missing spec.

    has_root_set = any(doc_set.root_relative == "docs" for doc_set in doc_sets)  # Detect root-set mode.
    has_child_sets = any(doc_set.root_relative != "docs" for doc_set in doc_sets)  # Detect feature-set mode.
    if has_root_set and has_child_sets:  # Multi-feature mode should not keep concrete specs in the root.
        errors.append("multi-doc-set mode must keep docs/ root to INDEX.md or README.md; move root spec/changelog into a feature folder")  # Report conflict.
    if has_child_sets and not any((docs_dir / name).exists() for name in ROOT_INDEX_DOCS):  # Feature sets need an index.
        errors.append("multi-doc-set mode requires docs/INDEX.md or docs/README.md")  # Report missing root index.

    root_allowed = ROOT_INDEX_DOCS | extra_allowed_docs  # Root docs are index-only by default.
    if has_root_set and not has_child_sets:  # Single-set mode allows root spec/changelog.
        root_allowed = root_allowed | DOC_SET_FILES  # Allow root ENGINEERING_SPEC.md and CHANGELOG.md.
    for doc_name in sorted(markdown_files(docs_dir) - root_allowed):  # Reject extra root Markdown files.
        errors.append(f"unexpected long-lived docs file: docs/{doc_name}")  # Report the orphan root file.

    for doc_set in doc_sets:  # Validate each documentation set.
        doc_errors, doc_warnings = validate_doc_set(doc_set)  # Validate one set.
        errors.extend(doc_errors)  # Merge set errors.
        warnings.extend(doc_warnings)  # Merge set warnings.

    return ValidationReport(ok=not errors, errors=tuple(errors), warnings=tuple(warnings))  # Return the final report.


def main() -> int:
    """Run the validator from the command line."""

    parser = argparse.ArgumentParser(description="Validate cx documentation-set policy.")  # Create CLI parser.
    parser.add_argument("root", nargs="?", default=".", help="Target repository root")  # Optional target path.
    parser.add_argument(  # Allow extra root Markdown documents when explicitly requested.
        "--allow-doc",
        action="append",
        default=[],
        help="Additional allowed Markdown file name in docs/",
    )
    args = parser.parse_args()  # Parse command-line arguments.

    root = Path(args.root).resolve()  # Resolve the target path to an absolute path.
    report = validate_single_source(root, allowed_docs=set(args.allow_doc))  # Run validation.

    for warning in report.warnings:  # Print every warning.
        print(f"WARN  {warning}")  # Warnings do not fail validation.
    for error in report.errors:  # Print every error.
        print(f"ERROR {error}")  # Errors fail validation.

    if report.ok:  # Success means no errors were collected.
        print("OK documentation-set policy passed")  # Print success message.
        return 0  # Return success status.
    return 1  # Return failure status.


if __name__ == "__main__":
    raise SystemExit(main())  # Use main's return value as the process exit code.
