from __future__ import annotations

import tempfile  # tempfile creates automatically cleaned temporary repositories.
import unittest  # unittest is the package's standard test framework.
from pathlib import Path  # Path builds cross-platform filesystem paths.

from tools.new_change import create_change_document  # Import the change-document creator under test.


class TestNewChange(unittest.TestCase):
    """Verify change documents are written only under docs/cx scenario changes."""

    def test_creates_change_document_under_scenario_changes(self) -> None:
        """Creating a change should write into the selected scenario changes directory."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Wrap the temporary path as a Path object.
            path = create_change_document(  # Create one change document.
                root,
                "01.create_user",
                1,
                "write_user_entity",
                "No user entity exists yet.",
                "Write the user entity test first, then implement the entity class.",
            )
            text = path.read_text(encoding="utf-8")  # Read the generated document.

        self.assertEqual(path.name, "write_user_entity.md")  # The filename must use the change name without a timestamp.
        self.assertIn("docs\\cx\\01.create_user\\changes", str(path))  # The path must target the scenario changes directory.
        self.assertNotIn("Timestamp", text)  # The generated document must not keep the old timestamp heading.
        self.assertIn("## What Was Done Before\nNo user entity exists yet.", text)  # The document must preserve previous state.
        self.assertIn("## What Should Happen Now\nWrite the user entity test first, then implement the entity class.", text)  # The document must preserve next action.

    def test_accepts_docs_cx_prefixed_scenario(self) -> None:
        """The scenario argument may include a docs/cx prefix."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Wrap the temporary path as a Path object.
            path = create_change_document(  # Create a change with a prefixed scenario path.
                root,
                "docs/cx/01.create_user",
                "02",
                "add_conditional_substep",
                "The main success scenario exists.",
                "Add the conditional substep and update tasks.",
            )

        self.assertEqual(path.parent, root / "docs" / "cx" / "01.create_user" / "changes")  # The prefix must not be duplicated.
        self.assertEqual(path.name, "add_conditional_substep.md")  # The filename must use the change name only.

    def test_rejects_bad_scenario_name(self) -> None:
        """Bad scenario names should be rejected."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Wrap the temporary path as a Path object.
            with self.assertRaisesRegex(ValueError, "01.create_user"):  # Assert the error explains the format.
                create_change_document(  # Pass an old-style scenario name.
                    root,
                    "001_user",
                    1,
                    "write_user_entity",
                    "None.",
                    "Implement.",
                )

    def test_rejects_bad_task_number(self) -> None:
        """Task numbers must be two digits."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Wrap the temporary path as a Path object.
            with self.assertRaisesRegex(ValueError, "task_number"):  # Assert the error points to the task number.
                create_change_document(  # Pass an invalid task number.
                    root,
                    "01.create_user",
                    "1A",
                    "write_user_entity",
                    "None.",
                    "Implement.",
                )


if __name__ == "__main__":
    unittest.main()  # Allow direct unittest execution.
