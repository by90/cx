from __future__ import annotations

import tempfile  # tempfile 创建自动清理的临时目录。
import unittest  # unittest 是项目规定的 Python 单元测试框架。
from pathlib import Path  # Path 用于构造跨平台文件路径。

from tools.new_change import append_change  # 引入待测试的变更记录工具函数。


class TestNewChange(unittest.TestCase):
    """验证变更只追加到目标文档集 changelog。"""

    def test_appends_changes_in_order_to_feature_changelog(self) -> None:
        """同一功能组的多个变更应该按创建顺序写入 changelog。"""

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 把临时目录转成 Path。
            first_id = append_change(  # 追加第一条变更。
                root,
                "创建项目模板",
                "feature",
                doc_set="template",
                today="2026-05-18",
                branch="codex/create-template",
            )
            second_id = append_change(  # 追加第二条变更。
                root,
                "补充使用指南",
                "docs",
                doc_set="template",
                today="2026-05-18",
                branch="codex/create-template",
            )
            changelog = (root / "docs" / "template" / "CHANGELOG.md").read_text(encoding="utf-8")  # 读取目标 changelog。

        self.assertEqual(first_id, "CHANGE-2026-001")  # 第一条变更编号应从 001 开始。
        self.assertEqual(second_id, "CHANGE-2026-002")  # 第二条变更编号应递增。
        self.assertLess(  # 第一条应该排在第二条前面，保留任务顺序。
            changelog.index("CHANGE-2026-001"),
            changelog.index("CHANGE-2026-002"),
        )
        self.assertIn("- Branch: codex/create-template", changelog)  # 变更记录应保存工作分支。


if __name__ == "__main__":
    unittest.main()
