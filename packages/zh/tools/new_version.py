#!/usr/bin/env python3
"""向 docs/VERSIONS.md 追加一次版本发布记录。"""

from __future__ import annotations

import argparse  # argparse 用于把命令行参数解析成 Python 对象。
import datetime as dt  # datetime 用于生成默认日期。
import re  # re 用于校验版本号格式。
from pathlib import Path  # Path 用于安全拼接文件路径。


VERSION_RE = re.compile(r"v\d+\.\d+\.\d+\Z")  # 匹配 v0.0.1 这样的语义化版本。
FEATURE_FOLDER_RE = re.compile(r"\d{3}_[a-z0-9]+(?:_[a-z0-9]+)*\Z")  # 匹配 001_project_template 这类功能组名。
DEFAULT_VERSIONS = "# VERSIONS.md\n\n## Versions\n"  # 新版本索引文件的最小内容。


def join_values(values: tuple[str, ...], fallback: str = "TODO") -> str:
    """把多个值合并成一行 Markdown 友好的文本。"""

    cleaned = [value.strip() for value in values if value.strip()]  # 去掉空白值，避免输出空条目。
    if cleaned:  # 如果调用方提供了有效值，就使用这些值。
        return ", ".join(cleaned)  # 用逗号连接，便于阅读和搜索。
    return fallback  # 没有值时返回占位文本。


def validate_feature_groups(groups: tuple[str, ...]) -> None:
    """确保版本条目只引用合法编号功能组。"""

    for group in groups:  # 逐个检查调用方传入的功能组。
        if not FEATURE_FOLDER_RE.fullmatch(group):  # 功能组名必须和 docs 目录名一致。
            raise ValueError("feature group must look like 001_project_template")  # 报告可直接修复的格式要求。


def build_entry(
    version: str,
    title: str,
    today: str,
    groups: tuple[str, ...],
    changes: tuple[str, ...],
    release_branch: str,
) -> str:
    """把版本信息渲染成 Markdown 条目。"""

    group_text = join_values(groups)  # 把功能组列表变成单行文本。
    change_text = join_values(changes)  # 把变更编号列表变成单行文本。
    return f"""
## {version} - {title}

- Date: {today}
- Feature groups: {group_text}
- Changes: {change_text}
- Release branch: {release_branch}
- Summary: TODO
- Verification evidence: TODO
""".strip()  # 去掉模板首尾空行，让追加逻辑负责空行。


def append_version(
    root: Path,
    version: str,
    title: str,
    today: str | None = None,
    groups: tuple[str, ...] = (),
    changes: tuple[str, ...] = (),
    release_branch: str = "dev",
) -> str:
    """校验版本号，并把版本条目写入 docs/VERSIONS.md。"""

    if not VERSION_RE.fullmatch(version):  # 版本号必须显式使用 vX.Y.Z 格式。
        raise ValueError("version must look like v0.0.1")  # 抛出清楚错误，方便调用方修正。
    validate_feature_groups(groups)  # 版本索引只能记录编号功能组。
    versions_path = root / "docs" / "VERSIONS.md"  # 版本索引固定放在 docs 根目录。
    versions_path.parent.mkdir(parents=True, exist_ok=True)  # 确保 docs 目录存在。
    text = versions_path.read_text(encoding="utf-8") if versions_path.exists() else DEFAULT_VERSIONS  # 读取旧文本或模板。
    actual_today = today or dt.date.today().isoformat()  # 没传日期时使用今天。
    entry = build_entry(version, title, actual_today, groups, changes, release_branch)  # 生成版本条目。
    updated_text = text.rstrip() + f"\n\n{entry}\n"  # 按创建顺序追加版本记录。
    versions_path.write_text(updated_text, encoding="utf-8")  # 用 UTF-8 写回文件。
    return version  # 返回版本号，方便测试和脚本使用。


def main() -> int:
    """从命令行追加一次版本记录。"""

    parser = argparse.ArgumentParser(description="Append a version entry to docs/VERSIONS.md.")  # 创建命令行解析器。
    parser.add_argument("version")  # 读取版本号，例如 v0.0.1。
    parser.add_argument("title")  # 读取版本标题。
    parser.add_argument("--root", default=".")  # 读取目标仓库根目录。
    parser.add_argument("--date", default=None)  # 允许自动化传入固定日期。
    parser.add_argument("--group", action="append", default=[])  # 允许重复传入完成功能组。
    parser.add_argument("--change", action="append", default=[])  # 允许重复传入关联变更编号。
    parser.add_argument("--release-branch", default="dev")  # 读取发布来源分支。
    args = parser.parse_args()  # 解析所有命令行参数。

    append_version(  # 调用核心函数写入版本索引。
        Path(args.root).resolve(),  # 把仓库根目录转换为绝对路径。
        args.version,  # 传入版本号。
        args.title,  # 传入版本标题。
        today=args.date,  # 传入可选日期。
        groups=tuple(args.group),  # 把功能组列表转成不可变元组。
        changes=tuple(args.change),  # 把变更列表转成不可变元组。
        release_branch=args.release_branch,  # 传入发布来源分支。
    )
    print(args.version)  # 输出版本号，方便自动化读取。
    return 0  # 返回成功退出码。


if __name__ == "__main__":
    raise SystemExit(main())  # 让脚本退出码等于 main 的返回值。
