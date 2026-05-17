from __future__ import annotations

import tempfile  # tempfile creates temporary directories that clean themselves up.
import unittest  # unittest is the required Python unit test framework for this project.
from pathlib import Path  # Path creates and joins filesystem paths.

from tools.validate_single_source import validate_single_source  # Import the function under test.


class TestValidateSingleSource(unittest.TestCase):
    """Cover single-set, multi-set, and invalid documentation layouts."""

    def test_valid_docs_pass(self) -> None:
        """A single-feature project may keep one documentation set in docs/."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Convert the temporary path string into Path.
            docs = root / "docs"  # Point to the docs directory.
            docs.mkdir()  # Create the docs directory.
            (docs / "ENGINEERING_SPEC.md").write_text(  # Write the root engineering spec.
                """# ENGINEERING_SPEC.md

## 4. BDD Scenarios

BDD-TRAIN-001
## 6. Test Matrix
""",
                encoding="utf-8",
            )
            (docs / "CHANGELOG.md").write_text("CHANGE-2026-001\n", encoding="utf-8")  # Write the root changelog.

            report = validate_single_source(root)  # Run validation.

        self.assertTrue(report.ok, report.errors)  # The single-set layout should pass.

    def test_valid_feature_folder_docs_pass(self) -> None:
        """A multi-feature project may keep documentation sets in docs subfolders."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Convert the temporary path string into Path.
            docs = root / "docs"  # Point to the docs root.
            feature = docs / "training"  # Point to one feature-group docs folder.
            feature.mkdir(parents=True)  # Create docs and the feature folder.
            (docs / "INDEX.md").write_text("# docs index\n", encoding="utf-8")  # Write the root index.
            (feature / "ENGINEERING_SPEC.md").write_text(  # Write the feature engineering spec.
                "BDD-TRAIN-001\n\n## 6. Test Matrix\n",
                encoding="utf-8",
            )
            (feature / "CHANGELOG.md").write_text("CHANGE-2026-001\n", encoding="utf-8")  # Write the feature changelog.

            report = validate_single_source(root)  # Run validation.

        self.assertTrue(report.ok, report.errors)  # The multi-set layout should pass.

    def test_change_id_in_spec_is_error(self) -> None:
        """A CHANGE belongs only in changelog, not in the BDD spec."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Convert the temporary path string into Path.
            docs = root / "docs"  # Point to the docs directory.
            docs.mkdir()  # Create docs.
            (docs / "ENGINEERING_SPEC.md").write_text(  # Spec intentionally includes an invalid CHANGE.
                "CHANGE-2026-001\nBDD-TRAIN-001\n\n## 6. Test Matrix\n",
                encoding="utf-8",
            )
            (docs / "CHANGELOG.md").write_text("CHANGE-2026-001\n", encoding="utf-8")  # Changelog includes CHANGE.

            report = validate_single_source(root)  # Run validation.

        self.assertFalse(report.ok)  # CHANGE in spec should fail.
        self.assertIn(  # Error should point to the same documentation set.
            "CHANGE-2026-001 must be recorded in docs/CHANGELOG.md, not docs/ENGINEERING_SPEC.md",
            report.errors,
        )

    def test_extra_markdown_doc_is_error(self) -> None:
        """The docs root must not keep random long-lived planning files."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Convert the temporary path string into Path.
            docs = root / "docs"  # Point to the docs directory.
            docs.mkdir()  # Create docs.
            (docs / "ENGINEERING_SPEC.md").write_text("# spec\n", encoding="utf-8")  # Write a spec.
            (docs / "CHANGELOG.md").write_text("# changelog\n", encoding="utf-8")  # Write a changelog.
            (docs / "random_plan.md").write_text("# random\n", encoding="utf-8")  # Write a forbidden orphan document.

            report = validate_single_source(root)  # Run validation.

        self.assertFalse(report.ok)  # Orphan document should fail.
        self.assertIn("unexpected long-lived docs file: docs/random_plan.md", report.errors)  # Confirm clear error.

    def test_multi_doc_mode_requires_root_index(self) -> None:
        """Multi-feature mode requires a docs root index."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Convert the temporary path string into Path.
            feature = root / "docs" / "training"  # Point to one feature docs folder.
            feature.mkdir(parents=True)  # Create the feature folder.
            (feature / "ENGINEERING_SPEC.md").write_text(  # Write the feature engineering spec.
                "BDD-TRAIN-001\n\n## 6. Test Matrix\n",
                encoding="utf-8",
            )
            (feature / "CHANGELOG.md").write_text("CHANGE-2026-001\n", encoding="utf-8")  # Write the feature changelog.

            report = validate_single_source(root)  # Run validation.

        self.assertFalse(report.ok)  # Missing root index should fail.
        self.assertIn("multi-doc-set mode requires docs/INDEX.md or docs/README.md", report.errors)  # Confirm index error.


if __name__ == "__main__":
    unittest.main()
