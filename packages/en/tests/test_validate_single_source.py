from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.validate_single_source import validate_single_source


class TestValidateSingleSource(unittest.TestCase):
    def test_valid_docs_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "ENGINEERING_SPEC.md").write_text(
                """# ENGINEERING_SPEC.md

## 4. BDD Scenarios

BDD-TRAIN-001
CHANGE-2026-001

## 6. Test Matrix
""",
                encoding="utf-8",
            )
            (docs / "CHANGELOG.md").write_text("CHANGE-2026-001\n", encoding="utf-8")

            report = validate_single_source(root)

        self.assertTrue(report.ok, report.errors)

    def test_change_in_changelog_must_appear_in_spec(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "ENGINEERING_SPEC.md").write_text("# spec\n", encoding="utf-8")
            (docs / "CHANGELOG.md").write_text("CHANGE-2026-001\n", encoding="utf-8")

            report = validate_single_source(root)

        self.assertFalse(report.ok)
        self.assertIn(
            "CHANGE-2026-001 appears in CHANGELOG.md but not ENGINEERING_SPEC.md",
            report.errors,
        )

    def test_extra_markdown_doc_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "ENGINEERING_SPEC.md").write_text("# spec\n", encoding="utf-8")
            (docs / "CHANGELOG.md").write_text("# changelog\n", encoding="utf-8")
            (docs / "random_plan.md").write_text("# random\n", encoding="utf-8")

            report = validate_single_source(root)

        self.assertFalse(report.ok)
        self.assertIn("unexpected long-lived docs file: docs/random_plan.md", report.errors)


if __name__ == "__main__":
    unittest.main()
