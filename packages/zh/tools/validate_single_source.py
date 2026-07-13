#!/usr/bin/env python3
"""校验目标仓库是否遵循 docs/cx 用例、任务与变更的单一文档来源规则。

本文件提供 `validate_single_source` 入口，用于检查 `docs/cx` 下的项目说明、主成功场景、
任务文件和变更文件。主要类是 `ScenarioFolder` 和 `ValidationReport`，主要函数是
`validate_single_source`。
"""

from __future__ import annotations

import re  # 使用正则表达式校验场景文件夹、任务文件和变更文件命名。
from dataclasses import dataclass  # 使用 dataclass 表达校验过程中传递的不可变结果对象。
from pathlib import Path  # 使用 Path 以面向对象方式处理跨平台文件路径。


SCENARIO_FOLDER_RE = re.compile(r"\d{2}\..+\Z")  # 主成功场景目录必须形如 01.创建用户。
TASK_DOCUMENT_RE = re.compile(r"\d{2}\..+\.md\Z")  # 任务文件必须形如 01.编写用户实体.md。
TIMESTAMPED_CHANGE_FILE_RE = re.compile(r"\d{8}T\d{6}")  # 变更文件名禁止携带时间戳。
LEGACY_CX_FILE_NAMES = {"B" + "DD.md", "ENGINEERING" + "_SPEC.md", "CHANGE" + "LOG.md", "GUIDE.md"}  # 旧 cx 文件不再允许出现。
LEGACY_CX_TEXT_RE = re.compile(r"\bB" + r"DD\b|\bGher" + r"kin\b|ENGINEERING" + r"_SPEC|CHANGE" + r"LOG")  # 旧流程关键词不应进入新 cx 文档。
RESERVED_CX_DIRECTORIES = {"docs", "notes"}  # 专题文档和研究笔记目录不是主成功场景。
CHANGE_REQUIRED_HEADINGS = (
    "## 状态",
    "## 关联对象",
    "## 当前事实",
    "## 目标状态",
    "## 主要变化",
    "## 顺序工作清单",
    "## 文件范围",
    "## 验证方式",
    "## 完成动作",
)  # 每个临时变更文件必须完整表达当前工作指令和删除条件。


@dataclass(frozen=True)
class ScenarioFolder:
    """表示一个 docs/cx 下的主成功场景文件夹。

    `root_relative` 是面向用户的相对路径，`directory` 是实际目录对象，其余字段分别指向用例、
    设计、任务目录和变更目录。该类无返回值行为，只保存校验所需路径。
    """

    root_relative: str  # 保存类似 docs/cx/01.创建用户 的可读路径。
    directory: Path  # 保存主成功场景目录的真实文件系统路径。
    usecase_path: Path  # 保存 00.用例.md 的路径。
    design_path: Path  # 保存 00.设计.md 的路径。
    tasks_path: Path  # 保存 tasks 目录的路径。
    changes_path: Path  # 保存 changes 目录的路径。


@dataclass(frozen=True)
class ValidationReport:
    """表示一次 docs/cx 单一来源校验结果。

    `ok` 表示是否没有错误，`errors` 保存必须修复的问题，`warnings` 保存建议关注但不阻断的问题。
    """

    ok: bool  # True 表示没有发现阻断性错误。
    errors: tuple[str, ...]  # 保存所有阻断性错误说明。
    warnings: tuple[str, ...]  # 保存所有非阻断性提醒说明。


class ScenarioScanner:
    """封装 docs/cx 目录扫描逻辑，避免把路径遍历细节散落到校验函数中。"""

    def __init__(self, root: Path = Path(".")) -> None:
        """创建扫描器。

        `root` 表示目标仓库根目录，默认值是当前工作目录；本方法只保存路径，无返回值。
        """

        self.root = root  # 保存目标仓库根目录，供后续方法复用。
        self.docs_dir = root / "docs"  # 保存 docs 根目录，便于扫描旧 cx 文件。
        self.cx_dir = self.docs_dir / "cx"  # 保存新的 cx 单一文档根目录。

    def scenario_folders(self) -> list[ScenarioFolder]:
        """返回 docs/cx 下所有主成功场景目录。

        本方法没有参数；返回值是按名称排序后的 `ScenarioFolder` 列表。
        """

        if not self.cx_dir.exists():  # docs/cx 不存在时没有可扫描的场景。
            return []  # 返回空列表，让上层统一报告缺失目录。
        folders: list[ScenarioFolder] = []  # 收集发现的主成功场景文件夹。
        for child in sorted(self.cx_dir.iterdir()):  # 按名称稳定遍历 docs/cx 的直接子项。
            if child.is_dir() and child.name not in RESERVED_CX_DIRECTORIES:  # 排除专题文档和研究笔记目录。
                folders.append(self._build_scenario(child))  # 将目录转换成带固定路径字段的对象。
        return folders  # 返回所有直接场景目录。

    def legacy_cx_files(self) -> list[Path]:
        """返回 docs 下残留的旧 cx 文件路径。

        本方法没有参数；返回值是旧文件名命中的 Path 列表。
        """

        if not self.docs_dir.exists():  # docs 不存在时没有旧文件可扫描。
            return []  # 返回空列表，缺失 docs/cx 的错误由上层处理。
        return sorted(  # 使用排序保证错误输出稳定。
            path  # 返回命中的旧文件路径。
            for path in self.docs_dir.rglob("*")  # 递归扫描 docs 下所有路径。
            if path.is_file() and path.name in LEGACY_CX_FILE_NAMES  # 只把旧 cx 固定文件名视为错误。
        )

    def _build_scenario(self, directory: Path) -> ScenarioFolder:
        """把一个目录包装成 `ScenarioFolder`。

        `directory` 是主成功场景候选目录；返回值是包含约定文件路径的 `ScenarioFolder`。
        """

        return ScenarioFolder(  # 构造不可变的路径对象。
            root_relative=f"docs/cx/{directory.name}",  # 记录面向用户的相对路径。
            directory=directory,  # 保存真实目录路径。
            usecase_path=directory / "00.用例.md",  # 计算用例文档路径。
            design_path=directory / "00.设计.md",  # 计算设计文档路径。
            tasks_path=directory / "tasks",  # 计算任务目录路径。
            changes_path=directory / "changes",  # 计算变更目录路径。
        )


def read_text(path: Path) -> str:
    """读取 UTF-8 文本。

    `path` 是目标文件路径；文件不存在时返回空字符串，存在时返回文件内容。
    """

    if path.exists():  # 只有文件存在时才读取，避免把缺失文件变成异常。
        return path.read_text(encoding="utf-8")  # cx 文档统一按 UTF-8 无 BOM 读取。
    return ""  # 缺失文件返回空文本，让调用方继续收集其它错误。


def markdown_files(directory: Path) -> list[Path]:
    """返回某个目录直接包含的 Markdown 文件。

    `directory` 是要扫描的目录；返回值只包含当前层级的 `.md` 文件。
    """

    if not directory.exists():  # 目录不存在时没有文件可返回。
        return []  # 返回空列表，便于调用方直接遍历。
    return sorted(path for path in directory.glob("*.md") if path.is_file())  # 只收集当前目录的 Markdown 文件。


def validate_scenario_folder(scenario: ScenarioFolder) -> tuple[list[str], list[str]]:
    """校验一个主成功场景目录。

    `scenario` 是候选主成功场景；返回值是错误列表和警告列表。
    """

    errors: list[str] = []  # 收集当前场景的阻断性错误。
    warnings: list[str] = []  # 收集当前场景的非阻断性提醒。
    if not SCENARIO_FOLDER_RE.fullmatch(scenario.directory.name):  # 场景文件夹必须使用两位数字和点号命名。
        errors.append(f"scenario folder must be named like docs/cx/01.创建用户: {scenario.root_relative}")  # 报告命名错误。
    if not scenario.usecase_path.exists():  # 每个场景必须有用例文档。
        errors.append(f"missing {scenario.root_relative}/00.用例.md")  # 报告缺失用例文档。
    if not scenario.design_path.exists():  # 每个场景必须有设计文档。
        errors.append(f"missing {scenario.root_relative}/00.设计.md")  # 报告缺失设计文档。
    if not scenario.tasks_path.is_dir():  # 每个场景必须有任务目录。
        errors.append(f"missing {scenario.root_relative}/tasks/")  # 报告缺失任务目录。
    if not scenario.changes_path.is_dir():  # 每个场景必须有变更目录。
        errors.append(f"missing {scenario.root_relative}/changes/")  # 报告缺失变更目录。
    errors.extend(validate_task_root(scenario))  # 合并任务目录校验错误。
    errors.extend(validate_change_root(scenario))  # 合并变更目录校验错误。
    errors.extend(validate_legacy_text(scenario))  # 合并旧流程关键词校验错误。
    if not markdown_files(scenario.changes_path):  # 没有变更文件时提醒 AI 无法从变更判断下一步。
        warnings.append(f"no change documents found in {scenario.root_relative}/changes/")  # 给出非阻断提醒。
    return errors, warnings  # 返回当前场景校验结果。


def validate_task_root(scenario: ScenarioFolder) -> list[str]:
    """校验场景的 tasks 目录。

    `scenario` 是所属主成功场景；返回值是任务文件相关错误。
    """

    errors: list[str] = []  # 收集任务文件错误。
    if not scenario.tasks_path.exists():  # tasks 缺失时上层已经报错。
        return errors  # 直接返回，避免继续扫描不存在目录。
    task_files = markdown_files(scenario.tasks_path)  # 收集 tasks 目录下的任务 Markdown 文件。
    task_dirs = sorted(path for path in scenario.tasks_path.iterdir() if path.is_dir())  # 收集旧式任务子目录。
    for task_dir in task_dirs:  # 逐个拒绝旧式任务子目录。
        errors.append(f"task documents must be files under tasks/, not directory: {scenario.root_relative}/tasks/{task_dir.name}")  # 报告旧式任务目录。
    if not task_files:  # 至少需要一个任务文件承接用例拆分。
        errors.append(f"missing task documents under {scenario.root_relative}/tasks/")  # 报告任务列表为空。
    for task_file in task_files:  # 逐个校验任务文件名。
        task_path = task_file.relative_to(scenario.directory).as_posix()  # 生成场景内相对路径。
        if task_file.name == "00.任务.md":  # 泛名任务文件不能表达任务关注点。
            errors.append(f"task document must be named like tasks/01.编写用户实体.md, not {task_path}")  # 报告泛名任务文件。
        elif not TASK_DOCUMENT_RE.fullmatch(task_file.name):  # 任务文件必须使用编号加中文名。
            errors.append(f"task document must be named like tasks/01.编写用户实体.md: {scenario.root_relative}/{task_path}")  # 报告任务命名错误。
    return errors  # 返回任务文件错误。


def validate_change_root(scenario: ScenarioFolder) -> list[str]:
    """校验场景的 changes 目录。

    `scenario` 是所属主成功场景；返回值是变更目录相关错误。
    """

    errors: list[str] = []  # 收集变更目录错误。
    if not scenario.changes_path.exists():  # changes 缺失时上层已经报错。
        return errors  # 直接返回，避免继续扫描不存在目录。
    for child in sorted(scenario.changes_path.iterdir()):  # 稳定遍历变更目录。
        if child.is_dir():  # 变更目录下不应再建子目录。
            errors.append(f"change documents must be files, not directory: {scenario.root_relative}/changes/{child.name}")  # 报告多余子目录。
    for change_file in markdown_files(scenario.changes_path):  # 逐个校验变更文档。
        if TIMESTAMPED_CHANGE_FILE_RE.search(change_file.name):  # 变更文件名不能继续携带时间戳。
            errors.append(f"change file must not contain timestamp: {scenario.root_relative}/changes/{change_file.name}")  # 报告命名错误。
        change_text = read_text(change_file)  # 读取变更文件内容。
        for heading in CHANGE_REQUIRED_HEADINGS:  # 检查所有必要章节。
            if heading not in change_text:  # 缺少章节会让 AI 无法判断当前工作。
                errors.append(f"missing heading {heading} in {scenario.root_relative}/changes/{change_file.name}")  # 报告缺失章节。
    return errors  # 返回变更目录错误。


def validate_legacy_text(scenario: ScenarioFolder) -> list[str]:
    """校验场景文档不再携带旧流程关键词。

    `scenario` 是所属主成功场景；返回值是旧关键词相关错误。
    """

    errors: list[str] = []  # 收集旧流程关键词错误。
    for doc_path in sorted(scenario.directory.rglob("*.md")):  # 扫描当前场景下所有 Markdown 文档。
        text = read_text(doc_path)  # 读取文档内容。
        if LEGACY_CX_TEXT_RE.search(text):  # 新流程不应出现旧流程关键字。
            relative_path = doc_path.relative_to(scenario.directory).as_posix()  # 生成场景内相对路径。
            errors.append(f"legacy cx wording is not allowed in {scenario.root_relative}/{relative_path}")  # 报告旧词残留。
    return errors  # 返回旧关键词错误。


def validate_single_source(root: Path = Path(".")) -> ValidationReport:
    """校验目标仓库的 docs/cx 单一来源规则。

    `root` 是目标仓库根目录，默认是当前工作目录；返回值是 `ValidationReport`。
    """

    scanner = ScenarioScanner(root)  # 创建面向目标仓库的扫描器。
    errors: list[str] = []  # 收集所有阻断性错误。
    warnings: list[str] = []  # 收集所有非阻断性提醒。
    if not scanner.cx_dir.is_dir():  # cx 根目录必须存在。
        errors.append("missing docs/cx directory")  # 报告缺失新的 cx 文档根目录。
        return ValidationReport(ok=False, errors=tuple(errors), warnings=tuple(warnings))  # 缺失根目录时提前返回。
    for legacy_path in scanner.legacy_cx_files():  # 扫描 docs 下旧 cx 固定文件名。
        errors.append(f"legacy cx document is not allowed: {legacy_path.relative_to(root).as_posix()}")  # 报告旧文件残留。
    scenarios = scanner.scenario_folders()  # 收集所有主成功场景。
    if not scenarios:  # 至少需要一个主成功场景承载用例流程。
        errors.append("missing docs/cx/01.主成功场景 folder")  # 报告缺失场景目录。
    for scenario in scenarios:  # 逐个校验主成功场景。
        scenario_errors, scenario_warnings = validate_scenario_folder(scenario)  # 校验单个场景。
        errors.extend(scenario_errors)  # 合并场景错误。
        warnings.extend(scenario_warnings)  # 合并场景提醒。
    return ValidationReport(ok=not errors, errors=tuple(errors), warnings=tuple(warnings))  # 返回最终校验报告。


def main() -> int:
    """从当前工作目录运行 docs/cx 单一来源校验。

    本方法没有参数；返回值是进程退出码，0 表示通过，1 表示失败。
    """

    report = validate_single_source(Path(".").resolve())  # 按当前工作目录执行校验，不接收命令行参数。
    for warning in report.warnings:  # 输出所有非阻断提醒。
        print(f"WARN  {warning}")  # 以 WARN 前缀区分提醒。
    for error in report.errors:  # 输出所有阻断错误。
        print(f"ERROR {error}")  # 以 ERROR 前缀区分错误。
    if report.ok:  # 没有错误时校验通过。
        print("OK docs/cx single-source policy passed")  # 输出成功信息。
        return 0  # 返回成功退出码。
    return 1  # 有错误时返回失败退出码。


if __name__ == "__main__":
    raise SystemExit(main())  # 将 main 的返回值作为脚本退出码。
