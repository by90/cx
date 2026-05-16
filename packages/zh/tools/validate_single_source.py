#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


CHANGE_ID_RE = re.compile(r"CHANGE-\d{4}-\d{3}")
BDD_ID_RE = re.compile(r"BDD-[A-Z0-9]+-\d{3}")
DEFAULT_ALLOWED_DOCS = {"ENGINEERING_SPEC.md", "CHANGELOG.md"}


@dataclass(frozen=True)
class ValidationReport:
    ok: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def find_markdown_docs(docs_dir: Path) -> set[str]:
    if not docs_dir.exists():
        return set()
    return {path.name for path in docs_dir.glob("*.md") if path.is_file()}


def validate_single_source(root: Path, allowed_docs: set[str] | None = None) -> ValidationReport:
    allowed = allowed_docs or DEFAULT_ALLOWED_DOCS
    docs_dir = root / "docs"
    spec_path = docs_dir / "ENGINEERING_SPEC.md"
    changelog_path = docs_dir / "CHANGELOG.md"

    errors: list[str] = []
    warnings: list[str] = []

    if not spec_path.exists():
        errors.append("missing docs/ENGINEERING_SPEC.md")
    if not changelog_path.exists():
        errors.append("missing docs/CHANGELOG.md")

    extra_docs = sorted(find_markdown_docs(docs_dir) - allowed)
    for doc_name in extra_docs:
        errors.append(f"unexpected long-lived docs file: docs/{doc_name}")

    spec_text = read_text(spec_path)
    changelog_text = read_text(changelog_path)

    change_ids_in_changelog = set(CHANGE_ID_RE.findall(changelog_text))
    change_ids_in_spec = set(CHANGE_ID_RE.findall(spec_text))
    missing_in_spec = sorted(change_ids_in_changelog - change_ids_in_spec)
    for change_id in missing_in_spec:
        errors.append(f"{change_id} appears in CHANGELOG.md but not ENGINEERING_SPEC.md")

    bdd_ids = sorted(set(BDD_ID_RE.findall(spec_text)))
    if spec_path.exists() and not bdd_ids:
        warnings.append("no BDD-* scenario IDs found in ENGINEERING_SPEC.md")

    test_matrix_section = "## 6. Test Matrix"
    if bdd_ids and test_matrix_section not in spec_text:
        errors.append("BDD IDs exist but Test Matrix section is missing")

    return ValidationReport(ok=not errors, errors=tuple(errors), warnings=tuple(warnings))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate single-source engineering documentation policy.")
    parser.add_argument("root", nargs="?", default=".", help="Target repository root")
    parser.add_argument(
        "--allow-doc",
        action="append",
        default=[],
        help="Additional allowed Markdown file name in docs/",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    allowed_docs = DEFAULT_ALLOWED_DOCS | set(args.allow_doc)
    report = validate_single_source(root, allowed_docs=allowed_docs)

    for warning in report.warnings:
        print(f"WARN  {warning}")
    for error in report.errors:
        print(f"ERROR {error}")

    if report.ok:
        print("OK single-source documentation policy passed")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
