from __future__ import annotations

import tempfile  # tempfile creates temporary directories that clean themselves up.
import unittest  # unittest is the required Python test framework.
from pathlib import Path  # Path builds filesystem paths safely.

from tools.new_change import append_change  # Import the change-log helper under test.


class TestNewChange(unittest.TestCase):
    """Verify that changes are appended only to the target changelog."""

    def test_appends_changes_in_order_to_feature_changelog(self) -> None:
        """Multiple changes in one feature group should keep creation order."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Convert the temporary path string into Path.
            first_id = append_change(  # Append the first change.
                root,
                "Create project template",
                "feature",
                doc_set="001_project_template",
                today="2026-05-18",
                branch="codex/create-template",
            )
            second_id = append_change(  # Append the second change.
                root,
                "Add usage guide",
                "docs",
                doc_set="001_project_template",
                today="2026-05-18",
                branch="codex/create-template",
            )
            changelog = (root / "docs" / "001_project_template" / "CHANGELOG.md").read_text(encoding="utf-8")  # Read target changelog.

        self.assertEqual(first_id, "CHANGE-2026-001")  # First change ID should start at 001.
        self.assertEqual(second_id, "CHANGE-2026-002")  # Second change ID should increment.
        self.assertLess(  # First change should appear before the second to preserve task order.
            changelog.index("CHANGE-2026-001"),
            changelog.index("CHANGE-2026-002"),
        )
        self.assertIn("- Branch: codex/create-template", changelog)  # Changelog should keep the work branch.

    def test_rejects_unnumbered_doc_set(self) -> None:
        """The change helper should reject unnumbered feature folders."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Convert the temporary path string into Path.
            with self.assertRaisesRegex(ValueError, "001_project_template"):  # Assert that the hint shows the new format.
                append_change(root, "Create project template", "feature", doc_set="template")  # Pass the old feature-group name.


if __name__ == "__main__":
    unittest.main()
