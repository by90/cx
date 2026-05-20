from __future__ import annotations

import tempfile  # tempfile creates temporary directories that clean themselves up.
import unittest  # unittest is the required Python test framework.
from pathlib import Path  # Path builds filesystem paths safely.

from tools.new_version import append_version  # Import the version helper under test.


class TestNewVersion(unittest.TestCase):
    """Verify that the version tool writes a version index."""

    def test_appends_version_entry(self) -> None:
        """After completing a feature group, the version tool should update docs/VERSIONS.md."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Convert the temporary path string into Path.
            append_version(  # Write one version entry.
                root,
                "v0.0.1",
                "Create project template",
                today="2026-05-18",
                groups=("001_project_template",),
                changes=("CHANGE-2026-001",),
            )
            text = (root / "docs" / "VERSIONS.md").read_text(encoding="utf-8")  # Read the version index.

        self.assertIn("## v0.0.1 - Create project template", text)  # Heading should include version and title.
        self.assertIn("- Feature groups: 001_project_template", text)  # Version should record completed feature groups.
        self.assertIn("- Changes: CHANGE-2026-001", text)  # Version should record related changes.

    def test_rejects_unnumbered_feature_group(self) -> None:
        """The version helper should reject unnumbered feature-group names."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Convert the temporary path string into Path.
            with self.assertRaisesRegex(ValueError, "001_project_template"):  # Assert that the hint shows the required format.
                append_version(root, "v0.0.1", "Create project template", groups=("template",))  # Pass the old unnumbered group value.


if __name__ == "__main__":
    unittest.main()
