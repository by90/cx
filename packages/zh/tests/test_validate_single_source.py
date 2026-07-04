from __future__ import annotations

import tempfile  # tempfile 用于创建自动清理的临时仓库目录。
import unittest  # unittest 是本项目规定的 Python 单元测试框架。
from pathlib import Path  # Path 用于以面向对象方式构造测试文件路径。

from tools.validate_single_source import validate_single_source  # 引入待测试的 docs/cx 校验入口。


class TestValidateSingleSource(unittest.TestCase):
    """覆盖 docs/cx 用例、任务和变更单一来源校验。"""

    def test_valid_docs_cx_story_layout_passes(self) -> None:
        """有效的主成功场景、任务和变更目录应通过校验。

        本测试没有参数，也没有返回值；它验证最小合格 docs/cx 结构。
        """

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 将临时目录包装为 Path。
            scenario = root / "docs" / "cx" / "01.创建用户"  # 构造主成功场景目录。
            tasks = scenario / "tasks"  # 构造任务目录。
            changes = scenario / "changes"  # 构造变更目录。
            tasks.mkdir(parents=True)  # 创建任务目录及父目录。
            changes.mkdir()  # 创建变更目录。
            (root / "docs" / "cx" / "00.项目说明.md").write_text("# 项目说明\n", encoding="utf-8")  # 写入项目说明。
            (scenario / "00.用例.md").write_text("# 用例\n\n## 主成功场景\n", encoding="utf-8")  # 写入用例文档。
            (scenario / "00.设计.md").write_text("# 设计\n\n## 公用代码\n", encoding="utf-8")  # 写入设计文档。
            (tasks / "01.编写用户实体.md").write_text("# 任务\n\n## 类\nUser\n", encoding="utf-8")  # 写入任务文档。
            (changes / "编写用户实体.md").write_text(  # 写入变更文档。
                "# 变更\n\n"
                "## 状态\n未完成\n\n"
                "## 任务\n01\n\n"
                "## 任务名称\n编写用户实体\n\n"
                "## 之前做了什么\n尚未实现。\n\n"
                "## 现在应该如何\n先写测试，再实现类。\n",
                encoding="utf-8",
            )

            report = validate_single_source(root)  # 执行 docs/cx 校验。

        self.assertTrue(report.ok, report.errors)  # 合格结构必须通过。

    def test_missing_docs_cx_is_error(self) -> None:
        """缺少 docs/cx 时应失败。

        本测试没有参数，也没有返回值；它验证新 cx 根目录是强制入口。
        """

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 将临时目录包装为 Path。

            report = validate_single_source(root)  # 对空仓库执行校验。

        self.assertFalse(report.ok)  # 缺少 docs/cx 必须失败。
        self.assertIn("missing docs/cx directory", report.errors)  # 错误信息必须指向新根目录。

    def test_legacy_cx_documents_are_error(self) -> None:
        """旧 cx 文档文件名应被拒绝。

        本测试没有参数，也没有返回值；它验证旧文件不会继续作为单一来源。
        """

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 将临时目录包装为 Path。
            legacy = root / "docs" / "001_user"  # 构造旧功能组目录。
            legacy.mkdir(parents=True)  # 创建旧功能组目录。
            old_name = "B" + "DD.md"  # 构造旧 cx 文件名，避免测试说明继续暴露旧流程入口。
            (legacy / old_name).write_text("# old\n", encoding="utf-8")  # 写入旧 cx 文件。
            (root / "docs" / "cx").mkdir()  # 创建新 cx 根目录，确保错误聚焦旧文件。

            report = validate_single_source(root)  # 执行 docs/cx 校验。

        self.assertFalse(report.ok)  # 旧文件残留必须失败。
        expected_path = "docs/" + "001_user/" + "B" + "DD.md"  # 构造期望路径。
        self.assertIn(f"legacy cx document is not allowed: {expected_path}", report.errors)  # 错误必须指出旧文件路径。

    def test_bad_scenario_folder_name_is_error(self) -> None:
        """主成功场景目录必须使用两位数字加点号命名。

        本测试没有参数，也没有返回值；它验证 `01.创建用户` 这类命名是强制规则。
        """

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 将临时目录包装为 Path。
            scenario = root / "docs" / "cx" / "1_创建用户"  # 构造错误命名的场景目录。
            (scenario / "tasks").mkdir(parents=True)  # 创建任务目录。
            (scenario / "changes").mkdir()  # 创建变更目录。
            (scenario / "00.用例.md").write_text("# 用例\n", encoding="utf-8")  # 写入用例文档。
            (scenario / "00.设计.md").write_text("# 设计\n", encoding="utf-8")  # 写入设计文档。
            (scenario / "tasks" / "01.编写用户实体.md").write_text("# 任务\n", encoding="utf-8")  # 写入任务文档。

            report = validate_single_source(root)  # 执行 docs/cx 校验。

        self.assertFalse(report.ok)  # 错误命名必须失败。
        self.assertIn("scenario folder must be named like docs/cx/01.创建用户: docs/cx/1_创建用户", report.errors)  # 错误必须给出目标格式。

    def test_generic_task_document_name_is_error(self) -> None:
        """任务文档不能使用 00.任务.md 泛名。

        本测试没有参数，也没有返回值；它验证每个任务文件必须用编号加中文名表达关注点。
        """

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 将临时目录包装为 Path。
            scenario = root / "docs" / "cx" / "01.创建用户"  # 构造主成功场景目录。
            tasks = scenario / "tasks"  # 构造 tasks 根目录。
            tasks.mkdir(parents=True)  # 创建 tasks 目录。
            (scenario / "changes").mkdir()  # 创建 changes 目录。
            (scenario / "00.用例.md").write_text("# 用例\n", encoding="utf-8")  # 写入用例文档。
            (scenario / "00.设计.md").write_text("# 设计\n", encoding="utf-8")  # 写入设计文档。
            (tasks / "00.任务.md").write_text("# 任务\n", encoding="utf-8")  # 故意写入泛名任务文档。

            report = validate_single_source(root)  # 执行 docs/cx 校验。

        self.assertFalse(report.ok)  # 泛名任务文档必须失败。
        self.assertIn("task document must be named like tasks/01.编写用户实体.md, not tasks/00.任务.md", report.errors)  # 错误必须指出泛名文件。

    def test_task_folder_is_error(self) -> None:
        """旧式任务文件夹应被拒绝。

        本测试没有参数，也没有返回值；它验证任务详情必须是 `tasks/NN.中文任务名.md` 文件。
        """

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 将临时目录包装为 Path。
            scenario = root / "docs" / "cx" / "01.创建用户"  # 构造主成功场景目录。
            task = scenario / "tasks" / "01.编写用户实体"  # 构造旧式任务文件夹。
            task.mkdir(parents=True)  # 创建旧式任务文件夹。
            (scenario / "changes").mkdir()  # 创建 changes 目录。
            (scenario / "00.用例.md").write_text("# 用例\n", encoding="utf-8")  # 写入用例文档。
            (scenario / "00.设计.md").write_text("# 设计\n", encoding="utf-8")  # 写入设计文档。

            report = validate_single_source(root)  # 执行 docs/cx 校验。

        self.assertFalse(report.ok)  # 旧式任务文件夹必须失败。
        self.assertIn("task documents must be files under tasks/, not directory: docs/cx/01.创建用户/tasks/01.编写用户实体", report.errors)  # 错误必须指出旧目录。

    def test_change_document_requires_working_headings(self) -> None:
        """变更文档必须包含 AI 判断下一步所需章节。

        本测试没有参数，也没有返回值；它验证变更文件不是普通流水账。
        """

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 将临时目录包装为 Path。
            scenario = root / "docs" / "cx" / "01.创建用户"  # 构造主成功场景目录。
            tasks = scenario / "tasks"  # 构造任务目录。
            changes = scenario / "changes"  # 构造变更目录。
            tasks.mkdir(parents=True)  # 创建任务目录及父目录。
            changes.mkdir()  # 创建变更目录。
            (scenario / "00.用例.md").write_text("# 用例\n", encoding="utf-8")  # 写入用例文档。
            (scenario / "00.设计.md").write_text("# 设计\n", encoding="utf-8")  # 写入设计文档。
            (tasks / "01.编写用户实体.md").write_text("# 任务\n", encoding="utf-8")  # 写入任务文档。
            (changes / "编写用户实体.md").write_text("# 变更\n", encoding="utf-8")  # 故意缺少必要章节。

            report = validate_single_source(root)  # 执行 docs/cx 校验。

        self.assertFalse(report.ok)  # 缺少章节必须失败。
        self.assertIn("missing heading ## 现在应该如何 in docs/cx/01.创建用户/changes/编写用户实体.md", report.errors)  # 错误必须指出缺失章节。


if __name__ == "__main__":
    unittest.main()  # 允许直接用 unittest 运行本文件。
