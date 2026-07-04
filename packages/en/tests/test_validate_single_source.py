from __future__ import annotations

import tempfile  # tempfile creates automatically cleaned temporary repositories.
import unittest  # unittest is the package's standard test framework.
from pathlib import Path  # Path builds cross-platform filesystem paths.

from tools.validate_single_source import validate_single_source  # Import the docs/cx validator under test.


class TestValidateSingleSource(unittest.TestCase):
    """Cover docs/cx use-case, task, and change single-source validation."""

    def test_valid_docs_cx_story_layout_passes(self) -> None:
        """A valid scenario, task, and change layout should pass."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Wrap the temporary path as a Path object.
            scenario = root / "docs" / "cx" / "01.create_user"  # Build the main success scenario path.
            tasks = scenario / "tasks"  # Build the tasks directory path.
            changes = scenario / "changes"  # Build the changes folder path.
            tasks.mkdir(parents=True)  # Create the tasks directory and parents.
            changes.mkdir()  # Create the changes folder.
            (root / "docs" / "cx" / "00.project.md").write_text("# Project\n", encoding="utf-8")  # Write a project document.
            (scenario / "00.use_case.md").write_text("# Use Case\n\n## Main Success Scenario\n", encoding="utf-8")  # Write a use-case document.
            (scenario / "00.design.md").write_text("# Design\n\n## Common Code\n", encoding="utf-8")  # Write a design document.
            (tasks / "01.write_user_entity.md").write_text("# Task\n\n## Class\nUser\n", encoding="utf-8")  # Write a task document.
            (changes / "write_user_entity.md").write_text(  # Write a change document.
                "# Change\n\n"
                "## Status\nopen\n\n"
                "## Task\n01\n\n"
                "## Task Name\nwrite_user_entity\n\n"
                "## What Was Done Before\nNothing has been implemented.\n\n"
                "## What Should Happen Now\nWrite the test first, then implement the class.\n",
                encoding="utf-8",
            )

            report = validate_single_source(root)  # Run validation.

        self.assertTrue(report.ok, report.errors)  # The valid layout must pass.

    def test_missing_docs_cx_is_error(self) -> None:
        """Missing docs/cx should fail."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Wrap the temporary path as a Path object.

            report = validate_single_source(root)  # Validate the empty repository.

        self.assertFalse(report.ok)  # Missing docs/cx must fail.
        self.assertIn("missing docs/cx directory", report.errors)  # The error must point to the new root.

    def test_legacy_cx_documents_are_error(self) -> None:
        """Old fixed-name cx documents should be rejected."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Wrap the temporary path as a Path object.
            legacy = root / "docs" / "001_user"  # Build an old-style folder path.
            legacy.mkdir(parents=True)  # Create the old-style folder.
            old_name = "B" + "DD.md"  # Build the old fixed file name without exposing it as a workflow entry.
            (legacy / old_name).write_text("# old\n", encoding="utf-8")  # Write an old cx file.
            (root / "docs" / "cx").mkdir()  # Create docs/cx so this test focuses on the old file.

            report = validate_single_source(root)  # Run validation.

        expected_path = "docs/" + "001_user/" + "B" + "DD.md"  # Build the expected error path.
        self.assertFalse(report.ok)  # Old files must fail.
        self.assertIn(f"legacy cx document is not allowed: {expected_path}", report.errors)  # The error must identify the file.

    def test_bad_scenario_folder_name_is_error(self) -> None:
        """Scenario folders must use two digits and a dot."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Wrap the temporary path as a Path object.
            scenario = root / "docs" / "cx" / "1_create_user"  # Build a badly named scenario folder.
            tasks = scenario / "tasks"  # Build the tasks directory under it.
            tasks.mkdir(parents=True)  # Create the tasks directory.
            (scenario / "changes").mkdir()  # Create the changes folder.
            (scenario / "00.use_case.md").write_text("# Use Case\n", encoding="utf-8")  # Write a use-case document.
            (scenario / "00.design.md").write_text("# Design\n", encoding="utf-8")  # Write a design document.
            (tasks / "01.write_user_entity.md").write_text("# Task\n", encoding="utf-8")  # Write a task document.

            report = validate_single_source(root)  # Run validation.

        self.assertFalse(report.ok)  # Bad scenario naming must fail.
        self.assertIn("scenario folder must be named like docs/cx/01.create_user: docs/cx/1_create_user", report.errors)  # The error must show the target format.

    def test_generic_task_document_name_is_error(self) -> None:
        """Task documents must not use the generic 00.task.md filename."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Wrap the temporary path as a Path object.
            scenario = root / "docs" / "cx" / "01.create_user"  # Build the scenario folder.
            tasks = scenario / "tasks"  # Build the tasks root.
            tasks.mkdir(parents=True)  # Create the tasks root.
            (scenario / "changes").mkdir()  # Create the changes folder.
            (scenario / "00.use_case.md").write_text("# Use Case\n", encoding="utf-8")  # Write a use-case document.
            (scenario / "00.design.md").write_text("# Design\n", encoding="utf-8")  # Write a design document.
            (tasks / "00.task.md").write_text("# Task\n", encoding="utf-8")  # Intentionally write a generic task document.

            report = validate_single_source(root)  # Run validation.

        self.assertFalse(report.ok)  # Generic task documents must fail.
        self.assertIn("task document must be named like tasks/01.write_user_entity.md, not tasks/00.task.md", report.errors)  # The error must identify the generic file.

    def test_task_folder_is_error(self) -> None:
        """Old task folders should be rejected."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Wrap the temporary path as a Path object.
            scenario = root / "docs" / "cx" / "01.create_user"  # Build the scenario folder.
            task = scenario / "tasks" / "01.write_user_entity"  # Build an old task folder.
            task.mkdir(parents=True)  # Create the old task folder.
            (scenario / "changes").mkdir()  # Create the changes folder.
            (scenario / "00.use_case.md").write_text("# Use Case\n", encoding="utf-8")  # Write a use-case document.
            (scenario / "00.design.md").write_text("# Design\n", encoding="utf-8")  # Write a design document.

            report = validate_single_source(root)  # Run validation.

        self.assertFalse(report.ok)  # Old task folders must fail.
        self.assertIn("task documents must be files under tasks/, not directory: docs/cx/01.create_user/tasks/01.write_user_entity", report.errors)  # The error must identify the old folder.

    def test_change_document_requires_working_headings(self) -> None:
        """Change documents must contain the headings AI needs to resume work."""

        with tempfile.TemporaryDirectory() as tmpdir:  # Create a temporary repository root.
            root = Path(tmpdir)  # Wrap the temporary path as a Path object.
            scenario = root / "docs" / "cx" / "01.create_user"  # Build the scenario folder.
            tasks = scenario / "tasks"  # Build the tasks directory.
            changes = scenario / "changes"  # Build the changes folder.
            tasks.mkdir(parents=True)  # Create the tasks directory.
            changes.mkdir()  # Create the changes folder.
            (scenario / "00.use_case.md").write_text("# Use Case\n", encoding="utf-8")  # Write a use-case document.
            (scenario / "00.design.md").write_text("# Design\n", encoding="utf-8")  # Write a design document.
            (tasks / "01.write_user_entity.md").write_text("# Task\n", encoding="utf-8")  # Write a task document.
            (changes / "write_user_entity.md").write_text("# Change\n", encoding="utf-8")  # Intentionally omit required headings.

            report = validate_single_source(root)  # Run validation.

        self.assertFalse(report.ok)  # Missing headings must fail.
        self.assertIn("missing heading ## What Should Happen Now in docs/cx/01.create_user/changes/write_user_entity.md", report.errors)  # The error must identify the missing heading.


if __name__ == "__main__":
    unittest.main()  # Allow direct unittest execution.
