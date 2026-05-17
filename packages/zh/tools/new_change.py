#!/usr/bin/env python3
"""向目标文档集的 CHANGELOG.md 追加一条 CHANGE 记录。"""

from __future__ import annotations

import argparse  # argparse 用于把命令行参数解析成 Python 对象。
import datetime as dt  # datetime 用于生成默认日期。
import re  # re 用于用正则表达式识别已有 CHANGE 编号。
from pathlib import Path  # Path 用于安全拼接跨平台文件路径。


CHANGE_ID_RE = re.compile(r"CHANGE-(\d{4})-(\d{3})")  # 匹配 CHANGE-年份-序号。
ROOT_DOC_SET_NAMES = {"", ".", "docs", "root"}  # 这些名字表示使用 docs 根文档集。
DEFAULT_CHANGELOG = "# CHANGELOG.md\n\n## Unreleased\n"  # 新 changelog 的最小可用内容。


def next_change_id(changelog_text: str, year: int) -> str:
    """根据当前年份和已有文本生成下一个 CHANGE 编号。"""

    numbers = [  # 收集同一年已经使用过的序号。
        int(match.group(2))  # 第二个分组是三位序号，把它转成整数便于比较。
        for match in CHANGE_ID_RE.finditer(changelog_text)  # 遍历 changelog 中所有 CHANGE 编号。
        if int(match.group(1)) == year  # 只统计目标年份的编号，避免跨年冲突。
    ]
    next_number = max(numbers, default=0) + 1  # 没有已有编号时从 1 开始，否则取最大值加 1。
    return f"CHANGE-{year}-{next_number:03d}"  # 把序号补齐三位，形成稳定 ID。


def changelog_path_for(root: Path, doc_set: str | None) -> Path:
    """根据文档集名称计算 changelog 路径。"""

    normalized = (doc_set or "").strip().strip("/\\")  # 清理空白和首尾路径分隔符。
    if normalized in ROOT_DOC_SET_NAMES:  # 根文档集直接使用 docs/CHANGELOG.md。
        return root / "docs" / "CHANGELOG.md"  # 返回根 changelog 路径。
    if normalized.startswith("docs/") or normalized.startswith("docs\\"):  # 允许用户传入 docs/<group>。
        normalized = normalized[5:]  # 去掉 docs/ 前缀，避免得到 docs/docs/<group>。
    return root / "docs" / normalized / "CHANGELOG.md"  # 返回功能组 changelog 路径。


def build_entry(
    change_id: str,
    title: str,
    change_type: str,
    today: str,
    branch: str,
    base_branch: str,
    feature_group: str,
) -> str:
    """把一条 CHANGE 记录渲染成 Markdown 文本。"""

    return f"""
### {change_id} - {title}

- Date: {today}
- Type: {change_type}
- Status: planned
- Branch: {branch}
- Base branch: {base_branch}
- Feature group: {feature_group}
- Summary: TODO
- Related scenarios: TODO
- Related tests: TODO
- Verification evidence: TODO
""".strip()  # 去掉模板首尾空行，让插入逻辑控制空行数量。


def append_under_unreleased(text: str, entry: str) -> str:
    """把新条目按创建顺序追加到 Unreleased 小节末尾。"""

    if "## Unreleased" not in text:  # 如果旧文件没有 Unreleased 小节，就补一个小节。
        return text.rstrip() + f"\n\n## Unreleased\n\n{entry}\n"  # 把条目放进新小节。
    header_index = text.index("## Unreleased")  # 找到 Unreleased 标题的起点。
    search_start = header_index + len("## Unreleased")  # 从标题后面开始找下一个二级标题。
    next_header_index = text.find("\n## ", search_start)  # 下一个二级标题表示 Unreleased 结束。
    if next_header_index == -1:  # 没有后续版本小节时，追加到文件末尾。
        return text.rstrip() + f"\n\n{entry}\n"  # 保留旧条目顺序，再追加新条目。
    before = text[:next_header_index].rstrip()  # 取出 Unreleased 小节已有内容。
    after = text[next_header_index:]  # 保留后续版本小节。
    return before + f"\n\n{entry}\n" + after  # 把新条目插入 Unreleased 末尾。


def append_change(
    root: Path,
    title: str,
    change_type: str,
    doc_set: str | None = None,
    today: str | None = None,
    branch: str = "TODO",
    base_branch: str = "dev",
) -> str:
    """创建 CHANGE 编号，并写入目标文档集的 changelog。"""

    changelog_path = changelog_path_for(root, doc_set)  # 根据文档集选择目标 changelog。
    changelog_path.parent.mkdir(parents=True, exist_ok=True)  # 确保目标 docs 目录已经存在。
    text = changelog_path.read_text(encoding="utf-8") if changelog_path.exists() else DEFAULT_CHANGELOG  # 读取旧文本或模板。
    actual_today = today or dt.date.today().isoformat()  # 没传日期时使用今天。
    year = int(actual_today[:4])  # CHANGE 编号按日期年份分组。
    change_id = next_change_id(text, year)  # 生成下一个稳定编号。
    feature_group = doc_set or "root"  # 记录该变更所属功能组。
    entry = build_entry(change_id, title, change_type, actual_today, branch, base_branch, feature_group)  # 生成 Markdown 条目。
    updated_text = append_under_unreleased(text, entry)  # 把条目追加到 Unreleased 小节末尾。
    changelog_path.write_text(updated_text, encoding="utf-8")  # 用 UTF-8 写回 changelog。
    return change_id  # 返回编号，方便脚本和测试继续使用。


def main() -> int:
    """从命令行追加一条 CHANGE 记录。"""

    parser = argparse.ArgumentParser(description="Append a CHANGE-* entry to a target docs changelog.")  # 创建命令行解析器。
    parser.add_argument("title")  # 读取变更标题。
    parser.add_argument("--type", default="feature", choices=["feature", "bugfix", "refactor", "test", "docs", "research"])  # 读取变更类型。
    parser.add_argument("--root", default=".")  # 读取目标仓库根目录。
    parser.add_argument("--doc-set", default=None)  # 读取目标文档集名称。
    parser.add_argument("--branch", default="TODO")  # 读取当前工作分支。
    parser.add_argument("--base-branch", default="dev")  # 读取合并目标分支。
    parser.add_argument("--date", default=None)  # 允许自动化传入固定日期。
    args = parser.parse_args()  # 解析所有命令行参数。

    change_id = append_change(  # 调用核心函数写入 changelog。
        Path(args.root).resolve(),  # 把仓库根目录转换为绝对路径。
        args.title,  # 传入标题。
        args.type,  # 传入变更类型。
        doc_set=args.doc_set,  # 传入目标文档集。
        today=args.date,  # 传入可选日期。
        branch=args.branch,  # 传入工作分支。
        base_branch=args.base_branch,  # 传入合并目标分支。
    )
    print(change_id)  # 输出编号，方便用户复制到任务记录或自动化日志。
    return 0  # 返回成功退出码。


if __name__ == "__main__":
    raise SystemExit(main())  # 让脚本退出码等于 main 的返回值。
