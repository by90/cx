#!/usr/bin/env python3
"""在 docs/cx 主成功场景的 changes 目录中创建一份变更文档。

本文件提供 `create_change_document` 入口，用于把一次变更写成 AI 可继续执行的单份 Markdown
文档。主要函数是 `change_path_for`、`build_change_text` 和 `create_change_document`。
"""

from __future__ import annotations

import re  # re 用于校验场景、任务编号和文件名片段。
from pathlib import Path  # Path 用于以面向对象方式拼接跨平台路径。


SCENARIO_FOLDER_RE = re.compile(r"\d{2}\..+\Z")  # 主成功场景目录必须形如 01.创建用户。
TASK_NUMBER_RE = re.compile(r"\d{2}\Z")  # 任务编号必须使用两位数字。
SAFE_NAME_RE = re.compile(r'[\\/:*?"<>|\r\n\t]+')  # Windows 和 Markdown 文件名中不应出现这些字符。


def normalize_scenario_name(scenario: str) -> str:
    """把用户传入的场景路径规范化为场景文件夹名。

    `scenario` 可以是 `01.创建用户` 或 `docs/cx/01.创建用户`；返回值是场景文件夹名。
    """

    normalized = scenario.strip().strip("/\\")  # 去除首尾空白和路径分隔符。
    normalized = normalized.replace("\\", "/")  # 统一 Windows 路径分隔符，便于后续处理。
    if normalized.startswith("docs/cx/"):  # 允许调用方传入完整 cx 相对路径。
        normalized = normalized[len("docs/cx/") :]  # 去掉固定前缀，只保留场景名。
    if "/" in normalized:  # 场景名不应再包含子路径。
        raise ValueError("scenario must look like 01.创建用户")  # 报告明确的场景命名要求。
    if not SCENARIO_FOLDER_RE.fullmatch(normalized):  # 校验两位编号加点号的格式。
        raise ValueError("scenario must look like 01.创建用户")  # 报告明确的场景命名要求。
    return normalized  # 返回规范化后的场景文件夹名。


def normalize_task_number(task_number: int | str) -> str:
    """把任务编号规范化为两位数字字符串。

    `task_number` 可以是整数或字符串；返回值是两位数字字符串。
    """

    if isinstance(task_number, int):  # 整数任务号需要补齐两位。
        normalized = f"{task_number:02d}"  # 使用两位数字表达任务编号。
    else:  # 字符串任务号保留用户显式编号。
        normalized = task_number.strip()  # 去除字符串任务号首尾空白。
    if not TASK_NUMBER_RE.fullmatch(normalized):  # 任务号必须正好两位数字。
        raise ValueError("task_number must look like 01")  # 报告明确的任务编号要求。
    return normalized  # 返回两位任务编号。


def safe_filename_part(value: str) -> str:
    """把任务名转换成可用于文件名的片段。

    `value` 是任务名称；返回值是去除危险路径字符后的名称。
    """

    cleaned = SAFE_NAME_RE.sub("", value.strip())  # 移除 Windows 文件名和路径分隔危险字符。
    cleaned = re.sub(r"\s+", "", cleaned)  # 移除连续空白，保持变更文件名紧凑。
    if not cleaned:  # 空任务名无法形成可读文件名。
        raise ValueError("task_name must not be empty")  # 报告任务名不能为空。
    return cleaned  # 返回安全文件名片段。


def change_path_for(
    root: Path,
    scenario: str,
    task_number: int | str,
    task_name: str,
) -> Path:
    """计算变更文档路径。

    `root` 是仓库根目录，`scenario` 是主成功场景，`task_number` 是任务号，`task_name` 是任务名，
    返回值是目标变更文档路径。
    """

    scenario_name = normalize_scenario_name(scenario)  # 规范化场景文件夹名。
    normalize_task_number(task_number)  # 校验任务编号，避免调用方把变更挂到无效任务上。
    safe_task_name = safe_filename_part(task_name)  # 规范化任务名称文件名片段。
    filename = f"{safe_task_name}.md"  # 变更文件名只使用中文变更名，不带时间戳。
    return root / "docs" / "cx" / scenario_name / "changes" / filename  # 返回完整变更文件路径。


def build_change_text(
    task_number: str,
    task_name: str,
    previous: str,
    current: str,
    status: str = "未完成",
) -> str:
    """渲染变更文档内容。

    `task_number` 是任务号，`task_name` 是任务名，`previous` 是之前状态，
    `current` 是现在应该如何处理，`status` 是变更状态；返回值是 Markdown 文本。
    """

    return (  # 使用固定章节保证 AI 可以稳定解析。
        "# 变更\n\n"
        f"## 状态\n{status}\n\n"
        f"## 任务\n{task_number}\n\n"
        f"## 任务名称\n{task_name}\n\n"
        f"## 之前做了什么\n{previous}\n\n"
        f"## 现在应该如何\n{current}\n"
    )  # 返回完整 Markdown 文本。


def create_change_document(
    root: Path,
    scenario: str,
    task_number: int | str,
    task_name: str,
    previous: str,
    current: str,
    status: str = "未完成",
) -> Path:
    """创建一份变更文档。

    `root` 是仓库根目录，`scenario` 是主成功场景，`task_number` 是任务号，`task_name` 是任务名，
    `previous` 是之前状态，`current` 是现在应该如何处理，`status` 是变更状态；返回值是写入的变更文件路径。
    """

    task_id = normalize_task_number(task_number)  # 规范化任务编号。
    path = change_path_for(root, scenario, task_id, task_name)  # 计算目标文件路径。
    path.parent.mkdir(parents=True, exist_ok=True)  # 确保 changes 目录存在。
    text = build_change_text(task_id, task_name, previous, current, status)  # 渲染变更文档内容。
    path.write_text(text, encoding="utf-8")  # 以 UTF-8 无 BOM 写入 Markdown。
    return path  # 返回生成的文件路径。


def main() -> int:
    """拒绝命令行参数方式创建变更文档。

    本方法没有参数；返回值是进程退出码，1 表示用户应通过受控自动化调用函数。
    """

    print("请通过 create_change_document(...) 创建变更文档；本脚本不接收命令行参数。")  # 明确脚本使用方式。
    return 1  # 返回失败退出码，避免误以为已经生成变更。


if __name__ == "__main__":
    raise SystemExit(main())  # 将 main 的返回值作为脚本退出码。
