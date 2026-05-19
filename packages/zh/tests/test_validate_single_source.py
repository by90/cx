from __future__ import annotations

import tempfile  # tempfile 创建自动清理的临时目录。
import unittest  # unittest 是项目规定的 Python 单元测试框架。
from pathlib import Path  # Path 让测试用面向对象方式创建文件路径。

from tools.validate_single_source import validate_single_source  # 引入待测试的文档集校验函数。


class TestValidateSingleSource(unittest.TestCase):
    """覆盖单文档集、多文档集和错误布局。"""

    def test_valid_docs_pass(self) -> None:
        """单功能项目可以直接在 docs 根目录放一个文档集。"""

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 把临时目录转成 Path。
            docs = root / "docs"  # 指向 docs 目录。
            docs.mkdir()  # 创建 docs 目录。
            (docs / "ENGINEERING_SPEC.md").write_text(  # 写入根文档集主文档。
                """# ENGINEERING_SPEC.md

## 4. BDD Scenarios

BDD-TRAIN-001
CHANGE-2026-001

## 6. Test Matrix
""",
                encoding="utf-8",
            )
            (docs / "CHANGELOG.md").write_text("CHANGE-2026-001\n", encoding="utf-8")  # 写入根文档集变更记录。

            report = validate_single_source(root)  # 执行校验。

        self.assertTrue(report.ok, report.errors)  # 单文档集应通过。

    def test_valid_feature_folder_docs_pass(self) -> None:
        """多功能组项目可以把文档集放到 docs 子目录。"""

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 把临时目录转成 Path。
            docs = root / "docs"  # 指向 docs 根目录。
            feature = docs / "1.训练"  # 指向编号功能组文档目录。
            feature.mkdir(parents=True)  # 创建 docs 和功能组目录。
            (docs / "INDEX.md").write_text("# docs index\n", encoding="utf-8")  # 写入根索引。
            (feature / "BDD.md").write_text(  # 写入功能组 BDD 文档。
                "# BDD: 1.训练\n\nFeature: 1.训练\n\nScenario: BDD-TRAIN-001 - Train model\n",
                encoding="utf-8",
            )
            (feature / "ENGINEERING_SPEC.md").write_text(  # 写入功能组主文档。
                "CHANGE-2026-001\nBDD-TRAIN-001\n\n## 6. Test Matrix\n",
                encoding="utf-8",
            )
            (feature / "CHANGELOG.md").write_text("CHANGE-2026-001\n", encoding="utf-8")  # 写入功能组变更记录。

            report = validate_single_source(root)  # 执行校验。

        self.assertTrue(report.ok, report.errors)  # 多文档集布局应通过。

    def test_change_in_changelog_must_appear_in_spec(self) -> None:
        """CHANGE 出现在 changelog 时，也必须出现在同一文档集主文档。"""

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 把临时目录转成 Path。
            docs = root / "docs"  # 指向 docs 目录。
            docs.mkdir()  # 创建 docs 目录。
            (docs / "ENGINEERING_SPEC.md").write_text("# spec\n", encoding="utf-8")  # 主文档故意缺少 CHANGE。
            (docs / "CHANGELOG.md").write_text("CHANGE-2026-001\n", encoding="utf-8")  # 变更记录包含 CHANGE。

            report = validate_single_source(root)  # 执行校验。

        self.assertFalse(report.ok)  # 缺少映射必须失败。
        self.assertIn(  # 错误信息要指向同一文档集。
            "CHANGE-2026-001 appears in docs/CHANGELOG.md but not docs/ENGINEERING_SPEC.md",
            report.errors,
        )

    def test_extra_markdown_doc_is_error(self) -> None:
        """docs 根目录不允许随意长期保存零散规划文档。"""

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 把临时目录转成 Path。
            docs = root / "docs"  # 指向 docs 目录。
            docs.mkdir()  # 创建 docs 目录。
            (docs / "ENGINEERING_SPEC.md").write_text("# spec\n", encoding="utf-8")  # 写入主文档。
            (docs / "CHANGELOG.md").write_text("# changelog\n", encoding="utf-8")  # 写入变更记录。
            (docs / "random_plan.md").write_text("# random\n", encoding="utf-8")  # 写入不允许的孤立文档。

            report = validate_single_source(root)  # 执行校验。

        self.assertFalse(report.ok)  # 孤立文档必须失败。
        self.assertIn("unexpected long-lived docs file: docs/random_plan.md", report.errors)  # 确认错误明确。

    def test_multi_doc_mode_requires_root_index(self) -> None:
        """多功能组模式必须有 docs 根索引。"""

        with tempfile.TemporaryDirectory() as tmpdir:  # 创建临时仓库根目录。
            root = Path(tmpdir)  # 把临时目录转成 Path。
            feature = root / "docs" / "1.训练"  # 指向编号功能组文档目录。
            feature.mkdir(parents=True)  # 创建功能组目录。
            (feature / "BDD.md").write_text(  # 写入必需的 BDD 文档。
                "# BDD: 1.训练\n\nFeature: 1.训练\n\nScenario: BDD-TRAIN-001 - Train model\n",
                encoding="utf-8",
            )
            (feature / "ENGINEERING_SPEC.md").write_text(  # 写入功能组主文档。
                "CHANGE-2026-001\nBDD-TRAIN-001\n\n## 6. Test Matrix\n",
                encoding="utf-8",
            )
            (feature / "CHANGELOG.md").write_text("CHANGE-2026-001\n", encoding="utf-8")  # 写入功能组变更记录。

            report = validate_single_source(root)  # 执行校验。

        self.assertFalse(report.ok)  # 缺少根索引必须失败。
        self.assertIn("multi-doc-set mode requires docs/INDEX.md or docs/README.md", report.errors)  # 确认索引错误。


if __name__ == "__main__":
    unittest.main()
