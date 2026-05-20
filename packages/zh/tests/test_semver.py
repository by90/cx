import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class SemverToolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]
        self.tool = self.repo_root / "tools" / "semver.py"

    def make_project(
        self,
        version: str = "0.1.0",
        pyproject_version: str | None = None,
        with_pyproject: bool = True,
    ) -> Path:
        folder = Path(tempfile.mkdtemp())
        docs = folder / "docs"
        docs.mkdir()
        (folder / "VERSION").write_text(f"{version}\n", encoding="utf-8")
        if with_pyproject:
            (folder / "pyproject.toml").write_text(
                "\n".join(
                    [
                        "[project]",
                        'name = "sample"',
                        f'version = "{pyproject_version or version}"',
                        "",
                    ]
                ),
                encoding="utf-8",
            )
        (docs / "VERSIONS.md").write_text(
            "\n".join(
                [
                    "# 版本记录",
                    "",
                    "本文件记录发布版本。",
                    "",
                    "## v0.0.1 - 初始版本",
                    "",
                    "- Date: 2026-05-20",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return folder

    def run_tool(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.tool), *args, "--root", str(root)],
            capture_output=True,
            text=True,
        )

    def test_check_reports_synced_version_as_json(self) -> None:
        project = self.make_project()
        try:
            result = self.run_tool(project, "check", "--json")
            data = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(data["version"], "0.1.0")
            self.assertEqual(data["pyproject_version"], "0.1.0")
            self.assertEqual(data["documented_versions"], ["0.0.1"])
        finally:
            shutil.rmtree(project)

    def test_check_rejects_pyproject_version_mismatch(self) -> None:
        project = self.make_project(version="0.1.0", pyproject_version="0.2.0")
        try:
            result = self.run_tool(project, "check")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("pyproject", result.stderr)
        finally:
            shutil.rmtree(project)

    def test_check_allows_project_without_pyproject(self) -> None:
        project = self.make_project(with_pyproject=False)
        try:
            result = self.run_tool(project, "check", "--json")
            data = json.loads(result.stdout)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(data["version"], "0.1.0")
            self.assertIsNone(data["pyproject_version"])
        finally:
            shutil.rmtree(project)

    def test_next_reports_cx_pre_one_bump_rule(self) -> None:
        project = self.make_project(version="0.1.0")
        try:
            feature_result = self.run_tool(project, "next", "feature-group", "--json")
            patch_result = self.run_tool(project, "next", "patch", "--json")
            feature_data = json.loads(feature_result.stdout)
            patch_data = json.loads(patch_result.stdout)

            self.assertEqual(feature_result.returncode, 0, feature_result.stderr)
            self.assertEqual(patch_result.returncode, 0, patch_result.stderr)
            self.assertEqual(feature_data["next_version"], "0.2.0")
            self.assertEqual(patch_data["next_version"], "0.1.1")
        finally:
            shutil.rmtree(project)

    def test_prepare_updates_version_sources_and_versions_doc(self) -> None:
        project = self.make_project()
        try:
            result = self.run_tool(
                project,
                "prepare",
                "0.2.0",
                "新增版本工具",
                "--feature-group",
                "001_project_template",
                "--summary",
                "新增 SemVer 工具",
                "--evidence",
                "python tools/semver.py check --root .",
                "--json",
            )
            data = json.loads(result.stdout)
            versions_text = (project / "docs" / "VERSIONS.md").read_text(
                encoding="utf-8"
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(data["version"], "0.2.0")
            self.assertEqual(
                (project / "VERSION").read_text(encoding="utf-8"), "0.2.0\n"
            )
            self.assertIn(
                'version = "0.2.0"',
                (project / "pyproject.toml").read_text(encoding="utf-8"),
            )
            self.assertIn("## v0.2.0 - 新增版本工具", versions_text)
            self.assertLess(
                versions_text.index("## v0.2.0"),
                versions_text.index("## v0.0.1"),
            )
        finally:
            shutil.rmtree(project)

    def test_prepare_rejects_invalid_semver(self) -> None:
        project = self.make_project()
        try:
            result = self.run_tool(project, "prepare", "1", "坏版本")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("SemVer", result.stderr)
        finally:
            shutil.rmtree(project)


if __name__ == "__main__":
    unittest.main()
