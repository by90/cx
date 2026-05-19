#!/usr/bin/env python3
"""Validate cx documentation-set layout for a target repository."""

from __future__ import annotations

import argparse  # argparse 负责把命令行参数解析成 Python 对象。
import re  # re 负责用正则表达式寻找 CHANGE ID 和 BDD ID。
from dataclasses import dataclass  # dataclass 用来声明轻量结果对象。
from pathlib import Path  # Path 用面向对象方式处理文件路径。


CHANGE_ID_RE = re.compile(r"CHANGE-\d{4}-\d{3}")  # 匹配稳定变更编号。
BDD_ID_RE = re.compile(r"BDD-[A-Z0-9]+-\d{3}")  # 匹配稳定行为场景编号。
ROOT_INDEX_DOCS = {"INDEX.md", "README.md"}  # 多文档集模式下 docs 根目录允许的索引文件。
DOC_SET_FILES = {"BDD.md", "ENGINEERING_SPEC.md", "CHANGELOG.md"}  # 一个研发文档集必须包含的核心文件。
OPTIONAL_DOC_SET_FILES = {"INDEX.md", "README.md"}  # 文档集目录内允许存在的说明文件。


@dataclass(frozen=True)
class DocSet:
    """Describe one folder that owns an engineering spec and changelog."""

    root_relative: str  # 保存面向用户的相对路径，便于报错。
    directory: Path  # 保存实际目录对象，便于读取文件。
    spec_path: Path  # 保存 ENGINEERING_SPEC.md 的完整路径。
    changelog_path: Path  # 保存 CHANGELOG.md 的完整路径。


@dataclass(frozen=True)
class ValidationReport:
    """Return validation success, errors, and warnings as one object."""

    ok: bool  # True 表示没有错误。
    errors: tuple[str, ...]  # errors 保存必须修复的问题。
    warnings: tuple[str, ...]  # warnings 保存建议关注的问题。


def read_text(path: Path) -> str:
    """Read UTF-8 text, returning an empty string when the file is absent."""

    if path.exists():  # 文件存在时才读取，避免 FileNotFoundError。
        return path.read_text(encoding="utf-8")  # 所有 cx 文档都按 UTF-8 读取。
    return ""  # 缺失文件返回空文本，让调用方继续收集其它错误。


def markdown_files(directory: Path) -> set[str]:
    """Return Markdown file names directly inside one directory."""

    if not directory.exists():  # 目录不存在时没有 Markdown 文件。
        return set()  # 返回空集合，方便后续集合运算。
    return {path.name for path in directory.glob("*.md") if path.is_file()}  # 只收集当前层文件名。


def discover_doc_sets(root: Path) -> list[DocSet]:
    """Find root or feature-folder documentation sets under docs/."""

    docs_dir = root / "docs"  # cx 约定所有长期文档都在 docs 目录下。
    doc_sets: list[DocSet] = []  # 用列表保存发现的文档集。
    root_spec = docs_dir / "ENGINEERING_SPEC.md"  # 单文档集模式的主文档路径。
    root_changelog = docs_dir / "CHANGELOG.md"  # 单文档集模式的变更记录路径。
    if root_spec.exists() or root_changelog.exists():  # 只要出现任一核心文件，就把根目录视作文档集候选。
        doc_sets.append(  # 保存根文档集，稍后再验证两个文件是否齐全。
            DocSet(
                root_relative="docs",  # 根文档集的用户可读路径。
                directory=docs_dir,  # 根文档集所在目录。
                spec_path=root_spec,  # 根文档集主文档。
                changelog_path=root_changelog,  # 根文档集变更记录。
            )
        )
    if docs_dir.exists():  # 只有 docs 存在时才扫描子目录。
        for child in sorted(path for path in docs_dir.iterdir() if path.is_dir()):  # 逐个检查一级功能目录。
            child_spec = child / "ENGINEERING_SPEC.md"  # 功能目录主文档路径。
            child_changelog = child / "CHANGELOG.md"  # 功能目录变更记录路径。
            if child_spec.exists() or child_changelog.exists():  # 出现任一核心文件就视作文档集候选。
                doc_sets.append(  # 保存功能组文档集。
                    DocSet(
                        root_relative=f"docs/{child.name}",  # 功能组文档集的用户可读路径。
                        directory=child,  # 功能组文档集所在目录。
                        spec_path=child_spec,  # 功能组主文档。
                        changelog_path=child_changelog,  # 功能组变更记录。
                    )
                )
    return doc_sets  # 返回所有候选文档集。


def validate_doc_set(doc_set: DocSet) -> tuple[list[str], list[str]]:
    """Validate one documentation set and return errors plus warnings."""

    errors: list[str] = []  # 收集当前文档集的错误。
    warnings: list[str] = []  # 收集当前文档集的警告。
    if doc_set.root_relative != "docs" and not re.fullmatch(r"\d+\..+", doc_set.directory.name):
        errors.append(f"feature documentation folder must be named like docs/1.配置系统: {doc_set.root_relative}")
    bdd_path = doc_set.directory / "BDD.md"
    if doc_set.root_relative != "docs" and not bdd_path.exists():
        errors.append(f"missing {doc_set.root_relative}/BDD.md")
    if not doc_set.spec_path.exists():  # 每个文档集必须有研发主文档。
        errors.append(f"missing {doc_set.root_relative}/ENGINEERING_SPEC.md")  # 报告缺失主文档。
    if not doc_set.changelog_path.exists():  # 每个文档集必须有变更记录。
        errors.append(f"missing {doc_set.root_relative}/CHANGELOG.md")  # 报告缺失变更记录。

    allowed = DOC_SET_FILES | OPTIONAL_DOC_SET_FILES  # 文档集目录内允许核心文件和说明文件。
    for doc_name in sorted(markdown_files(doc_set.directory) - allowed):  # 找出额外 Markdown 文件。
        errors.append(f"unexpected long-lived docs file: {doc_set.root_relative}/{doc_name}")  # 阻止孤立文档。

    spec_text = read_text(doc_set.spec_path)  # 读取主文档文本。
    bdd_text = read_text(bdd_path)
    changelog_text = read_text(doc_set.changelog_path)  # 读取变更记录文本。
    change_ids_in_changelog = set(CHANGE_ID_RE.findall(changelog_text))  # 提取 changelog 中的变更编号。
    change_ids_in_spec = set(CHANGE_ID_RE.findall(spec_text))  # 提取主文档中的变更编号。
    for change_id in sorted(change_ids_in_changelog - change_ids_in_spec):  # 每个 changelog 变更都必须回指主文档。
        errors.append(  # 把缺失映射写成清楚的错误。
            f"{change_id} appears in {doc_set.root_relative}/CHANGELOG.md but not "
            f"{doc_set.root_relative}/ENGINEERING_SPEC.md"
        )

    if bdd_text and doc_set.root_relative != "docs":
        expected = doc_set.directory.name
        if f"# BDD: {expected}" not in bdd_text and f"Feature: {expected}" not in bdd_text:
            errors.append(f"{doc_set.root_relative}/BDD.md must use the same BDD or Feature name as its folder")

    bdd_ids = sorted(set(BDD_ID_RE.findall(spec_text + "\n" + bdd_text)))  # 提取 BDD 场景编号。
    if doc_set.spec_path.exists() and not bdd_ids:  # 主文档存在但没有 BDD ID 时给警告。
        warnings.append(f"no BDD-* scenario IDs found in {doc_set.root_relative}/ENGINEERING_SPEC.md")  # 提醒补行为场景。
    if bdd_ids and "## 6. Test Matrix" not in spec_text:  # 有 BDD ID 就必须有测试矩阵。
        errors.append(f"BDD IDs exist but Test Matrix section is missing in {doc_set.root_relative}/ENGINEERING_SPEC.md")  # 报告矩阵缺失。
    return errors, warnings  # 返回当前文档集结果。


def validate_single_source(root: Path, allowed_docs: set[str] | None = None) -> ValidationReport:
    """Validate either one root docs set or many feature-folder docs sets."""

    extra_allowed_docs = allowed_docs or set()  # 调用方可以额外允许根目录 Markdown 文件。
    docs_dir = root / "docs"  # 所有长期文档必须在 docs 目录下。
    errors: list[str] = []  # 收集全局错误。
    warnings: list[str] = []  # 收集全局警告。

    if not docs_dir.exists():  # 没有 docs 目录直接失败。
        errors.append("missing docs directory")  # 报告缺失 docs。
        return ValidationReport(ok=False, errors=tuple(errors), warnings=tuple(warnings))  # 提前返回。

    doc_sets = discover_doc_sets(root)  # 找出根文档集和功能组文档集。
    if not doc_sets:  # 至少需要一个文档集。
        errors.append("missing docs/ENGINEERING_SPEC.md or docs/<feature-group>/ENGINEERING_SPEC.md")  # 报告缺失主文档。

    has_root_set = any(doc_set.root_relative == "docs" for doc_set in doc_sets)  # 判断是否存在根文档集。
    has_child_sets = any(doc_set.root_relative != "docs" for doc_set in doc_sets)  # 判断是否存在功能组文档集。
    if has_root_set and has_child_sets:  # 多功能组模式下不允许根目录同时承载具体研发文档。
        errors.append("multi-doc-set mode must keep docs/ root to INDEX.md or README.md; move root spec/changelog into a feature folder")  # 报告布局冲突。
    if has_child_sets and not any((docs_dir / name).exists() for name in ROOT_INDEX_DOCS):  # 多功能组需要根索引。
        errors.append("multi-doc-set mode requires docs/INDEX.md or docs/README.md")  # 报告缺失索引。

    root_allowed = ROOT_INDEX_DOCS | extra_allowed_docs  # 根目录默认只允许索引和用户额外白名单。
    if has_root_set and not has_child_sets:  # 单文档集模式允许根目录放核心文件。
        root_allowed = root_allowed | DOC_SET_FILES  # 加入 ENGINEERING_SPEC.md 和 CHANGELOG.md。
    for doc_name in sorted(markdown_files(docs_dir) - root_allowed):  # 检查根目录多余 Markdown 文件。
        errors.append(f"unexpected long-lived docs file: docs/{doc_name}")  # 报告孤立根文档。

    for doc_set in doc_sets:  # 逐个验证文档集内部规则。
        doc_errors, doc_warnings = validate_doc_set(doc_set)  # 验证单个文档集。
        errors.extend(doc_errors)  # 合并错误。
        warnings.extend(doc_warnings)  # 合并警告。

    return ValidationReport(ok=not errors, errors=tuple(errors), warnings=tuple(warnings))  # 汇总最终结果。


def main() -> int:
    """Run the validator from the command line."""

    parser = argparse.ArgumentParser(description="Validate cx documentation-set policy.")  # 创建命令行解析器。
    parser.add_argument("root", nargs="?", default=".", help="Target repository root")  # 读取目标仓库路径。
    parser.add_argument(  # 支持额外允许的 docs 根目录 Markdown 文件。
        "--allow-doc",
        action="append",
        default=[],
        help="Additional allowed Markdown file name in docs/",
    )
    args = parser.parse_args()  # 解析命令行参数。

    root = Path(args.root).resolve()  # 把目标路径转换成绝对路径。
    report = validate_single_source(root, allowed_docs=set(args.allow_doc))  # 执行校验。

    for warning in report.warnings:  # 逐条输出警告。
        print(f"WARN  {warning}")  # 警告不导致失败。
    for error in report.errors:  # 逐条输出错误。
        print(f"ERROR {error}")  # 错误会导致非零退出码。

    if report.ok:  # 没有错误时校验通过。
        print("OK documentation-set policy passed")  # 输出成功信息。
        return 0  # 返回成功退出码。
    return 1  # 返回失败退出码。


if __name__ == "__main__":
    raise SystemExit(main())  # 让脚本退出码等于 main 的返回值。
