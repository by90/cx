from __future__ import annotations

import tempfile  # tempfile 用于创建自动清理的临时仓库目录。
import unittest  # unittest 是本项目规定的 Python 单元测试框架。
from pathlib import Path  # Path 用于构造跨平台文件路径。

from tools.new_change import create_change_document  # 引入待测试的变更文档创建函数。


class TestNewChange(unittest.TestCase):
    """验证变更文档只写入 docs/cx 场景 changes 目录。"""

    def test_creates_change_document_under_scenario_changes(self) -> None:
        """创建变更时应写入指定主成功场景的 changes 目录。

        本测试没有参数，也没有返回值；它验证文件路径和关键章节内容。
        """

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 将临时目录包装为 Path。
            path = create_change_document(  # 创建一份变更文档。
                root,
                "01.创建用户",
                1,
                "编写用户实体",
                "尚未实现用户实体。",
                "先写用户实体测试，再实现实体类。",
            )
            text = path.read_text(encoding="utf-8")  # 读取生成的变更文档。

        self.assertEqual(path.name, "编写用户实体.md")  # 文件名必须只使用变更名，不带时间戳。
        self.assertIn("docs\\cx\\01.创建用户\\changes", str(path))  # 路径必须位于指定场景 changes 目录。
        self.assertNotIn("时间戳", text)  # 变更正文不能继续保留旧式时间戳章节。
        self.assertIn("## 之前做了什么\n尚未实现用户实体。", text)  # 文档必须记录之前状态。
        self.assertIn("## 现在应该如何\n先写用户实体测试，再实现实体类。", text)  # 文档必须记录下一步动作。

    def test_accepts_docs_cx_prefixed_scenario(self) -> None:
        """调用方可以传入 docs/cx 前缀形式的场景路径。

        本测试没有参数，也没有返回值；它验证路径规范化不会重复拼接 docs/cx。
        """

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 将临时目录包装为 Path。
            path = create_change_document(  # 使用带 docs/cx 前缀的场景创建变更。
                root,
                "docs/cx/01.创建用户",
                "02",
                "补充条件子步骤",
                "已有主成功场景。",
                "补充条件子步骤并更新任务。",
            )

        self.assertEqual(path.parent, root / "docs" / "cx" / "01.创建用户" / "changes")  # 父目录必须只包含一层 docs/cx。
        self.assertEqual(path.name, "补充条件子步骤.md")  # 文件名必须只使用变更名。

    def test_rejects_bad_scenario_name(self) -> None:
        """场景名不符合 01.创建用户 格式时应拒绝。

        本测试没有参数，也没有返回值；它验证变更不会写入旧式目录。
        """

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 将临时目录包装为 Path。
            with self.assertRaisesRegex(ValueError, "01.创建用户"):  # 断言错误说明包含正确格式。
                create_change_document(  # 传入旧式场景名。
                    root,
                    "001_user",
                    1,
                    "编写用户实体",
                    "无。",
                    "实现。",
                )

    def test_rejects_bad_task_number(self) -> None:
        """任务号必须是两位数字。

        本测试没有参数，也没有返回值；它验证任务编号不会漂移成任意文本。
        """

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 将临时目录包装为 Path。
            with self.assertRaisesRegex(ValueError, "task_number"):  # 断言错误说明指向任务编号。
                create_change_document(  # 传入非法任务号。
                    root,
                    "01.创建用户",
                    "1A",
                    "编写用户实体",
                    "无。",
                    "实现。",
                )


if __name__ == "__main__":
    unittest.main()  # 允许直接用 unittest 运行本文件。
