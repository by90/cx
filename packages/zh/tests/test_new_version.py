from __future__ import annotations

import tempfile  # tempfile 创建自动清理的临时目录。
import unittest  # unittest 是项目规定的 Python 单元测试框架。
from pathlib import Path  # Path 用于构造文件路径。

from tools.new_version import append_version  # 引入待测试的版本记录工具函数。


class TestNewVersion(unittest.TestCase):
    """验证版本工具能生成版本索引。"""

    def test_appends_version_entry(self) -> None:
        """完成一组功能后，版本工具应写入 docs/VERSIONS.md。"""

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 把临时目录转成 Path。
            append_version(  # 写入一个版本条目。
                root,
                "v0.0.1",
                "创建项目模板",
                today="2026-05-18",
                groups=("template",),
                changes=("CHANGE-2026-001",),
            )
            text = (root / "docs" / "VERSIONS.md").read_text(encoding="utf-8")  # 读取版本索引。

        self.assertIn("## v0.0.1 - 创建项目模板", text)  # 标题应包含版本号和标题。
        self.assertIn("- Feature groups: template", text)  # 版本应记录完成功能组。
        self.assertIn("- Changes: CHANGE-2026-001", text)  # 版本应记录关联变更。


if __name__ == "__main__":
    unittest.main()
