from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.validate_cx_pack import validate_agents, validate_manifest


class TestValidateCxPack(unittest.TestCase):
    def test_validate_agent_requires_cx_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            agent_dir = root / ".codex" / "agents"
            agent_dir.mkdir(parents=True)
            (agent_dir / "reviewer.toml").write_text(
                'name = "reviewer"\n'
                'description = "A reviewer description that is long enough."\n'
                'developer_instructions = """Review the work carefully and report concrete evidence, missing tests, documentation drift, and actionable issues without editing code."""\n',
                encoding="utf-8",
            )

            errors = validate_agents(root)

        self.assertTrue(any("cx-" in error for error in errors))

    def test_manifest_requires_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "manifest.json").write_text(
                '{"package":"cx","version":"1.0.0","skills":[{"name":"cx-missing","path":"missing/SKILL.md"}],"agents":[]}',
                encoding="utf-8",
            )

            errors = validate_manifest(root)

        self.assertTrue(any("does not exist" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
