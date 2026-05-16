from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.validate_skill_pack import parse_frontmatter, validate_skill_file


class TestValidateSkillPack(unittest.TestCase):
    def test_parse_frontmatter_extracts_name_and_description(self) -> None:
        text = """---
name: cx-example
description: Use this skill for a sufficiently clear and repeatable task.
version: 1.0.0
---

Body text.
"""
        self.assertEqual(
            parse_frontmatter(text),
            {
                "name": "cx-example",
                "description": "Use this skill for a sufficiently clear and repeatable task.",
                "version": "1.0.0",
            },
        )

    def test_validate_skill_file_rejects_non_cx_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "example"
            skill_dir.mkdir()
            path = skill_dir / "SKILL.md"
            path.write_text(
                "---\nname: example\ndescription: This description is long enough but lacks the required prefix.\nversion: 1.0.0\n---\n\n"
                + "Word " * 100,
                encoding="utf-8",
            )

            result = validate_skill_file(path)

        self.assertFalse(result.ok)
        self.assertTrue(any("cx-" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
