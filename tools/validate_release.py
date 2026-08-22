#!/usr/bin/env python3
"""验证 cx 双语发行的结构、元数据、镜像和单一来源静态合同。"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
import re

SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?\Z"
)


def load_manifest(path: Path) -> dict[str, object]:
    """读取一个 UTF-8 安装包清单。

    Args:
        path: 待读取的清单文件路径。

    Returns:
        清单根对象的字段字典。
    """
    # 清单编码固定为 UTF-8，解析错误保持原始异常并中止验证。
    return json.loads(path.read_text(encoding="utf-8"))


def names(data: dict[str, object], key: str) -> list[str]:
    """提取并排序清单中一个对象列表的名称。

    Args:
        data: 已解析的安装包清单。
        key: 要读取的对象列表字段。

    Returns:
        供双语集合比较使用的稳定名称列表。
    """
    # 稳定排序消除清单书写顺序对双语集合比较的影响。
    return sorted(str(item["name"]) for item in data.get(key, []))


def relative_files(root: Path) -> list[Path]:
    """列出技能目录中的全部相对文件路径。

    Args:
        root: 技能源或安装包镜像根目录。

    Returns:
        按路径排序的相对文件列表。
    """
    # 递归文件集合用于同时比较技能正文和脚本等支持资源。
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


def run(command: list[str], cwd: Path) -> int:
    """运行一个非单元测试型静态验证命令。

    Args:
        command: Python 解释器和静态验证器参数。
        cwd: 验证器需要使用的当前目录。

    Returns:
        子进程原始退出码。
    """
    # 先打印完整命令，使发行证据能追溯实际执行入口。
    print("$ " + " ".join(command))
    # 静态验证器直接继承当前终端并返回真实退出状态。
    completed = subprocess.run(command, cwd=cwd, text=True)
    # 调用者统一把非零退出码登记为发行错误。
    return completed.returncode


def current_branch(root: Path) -> str | None:
    """读取待发行仓库的当前 Git 分支。

    Args:
        root: cx 源仓库根目录。

    Returns:
        当前分支名称；Git 命令失败或结果为空时返回空值。
    """
    # 分支读取不修改仓库，只为 main 发行门禁提供事实。
    completed = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    # Git 自身失败时由发行门禁统一报告分支缺失。
    if completed.returncode != 0:
        return None
    # 去除终端换行，空分支结果统一表达为空值。
    return completed.stdout.strip() or None


def main() -> int:
    """执行双语 cx 发行的全部静态门禁。

    Returns:
        所有静态门禁通过时返回零，否则返回一。
    """
    # 根目录参数只服务仓库内发行验证，不接收测试开关。
    parser = argparse.ArgumentParser(
        description="Validate cx multilingual release repository."
    )
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    # 解析后的绝对根目录用于构造双语包和公共技能源路径。
    root = Path(args.root).resolve()
    # 中英文安装包是发行验证的两个固定对象。
    en = root / "packages" / "en"
    zh = root / "packages" / "zh"
    # 所有静态问题集中收集，便于一次修复完整发行状态。
    errors: list[str] = []

    # 发行所需根目录和版本文件缺失时直接形成结构错误。
    if not en.exists():
        errors.append("missing packages/en")
    if not zh.exists():
        errors.append("missing packages/zh")
    if not (root / "SKILLS").exists():
        errors.append("missing public SKILLS directory for shskills")
    if not (root / "VERSION").exists():
        errors.append("missing root VERSION")
    if not (root / "CHANGELOG.md").exists():
        errors.append("missing root CHANGELOG.md")
    if errors:
        # 根结构不完整时无法安全执行后续文件读取。
        for error in errors:
            print(f"ERROR {error}")
        return 1

    # 正式发行验证只允许在 main 分支执行。
    branch = current_branch(root)
    if branch != "main":
        errors.append(
            "release validation must run on main before version commits or release tags"
        )

    # 根版本是双语安装包共同使用的唯一发行版本。
    root_version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER_RE.fullmatch(root_version):
        errors.append("root VERSION must use SemVer format")

    # 双语清单必须与根版本和彼此保持一致。
    en_manifest = load_manifest(en / "manifest.json")
    zh_manifest = load_manifest(zh / "manifest.json")
    if en_manifest.get("version") != zh_manifest.get("version"):
        errors.append("package version mismatch between English and Chinese packages")
    if (
        en_manifest.get("version") != root_version
        or zh_manifest.get("version") != root_version
    ):
        errors.append("package manifests must match root VERSION")
    if not SEMVER_RE.fullmatch(str(en_manifest.get("version", ""))):
        errors.append("package version must use SemVer format")

    # 当前版本必须在变更记录中拥有标准日期标题。
    changelog_text = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if "## [Unreleased]" not in changelog_text:
        errors.append("root CHANGELOG.md must contain ## [Unreleased]")
    release_heading = re.compile(
        rf"^## \[{re.escape(root_version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$", re.MULTILINE
    )
    if not release_heading.search(changelog_text):
        errors.append("root CHANGELOG.md must contain a dated section for root VERSION")

    # 技能与代理集合分别进行双语名称比较。
    for key in ("skills", "agents"):
        if names(en_manifest, key) != names(zh_manifest, key):
            errors.append(f"{key} mismatch between English and Chinese packages")

    # 双语根说明必须公开当前安装入口并移除旧克隆脚本入口。
    readme_text = "\n".join(
        (root / name).read_text(encoding="utf-8")
        for name in ("README.md", "README.zh-CN.md")
    )
    if "shskills install" not in readme_text:
        errors.append("root README files must document direct shskills install/update")
    for obsolete in ("install-command", "scripts\\cx", "scripts/cx"):
        if obsolete in readme_text:
            errors.append(
                f"root README files must not require cloned cx scripts: {obsolete}"
            )

    # 每种语言分别比较公共技能源和可安装包中的完整技能树。
    for lang, package, manifest in (("en", en, en_manifest), ("zh", zh, zh_manifest)):
        public_skill_root = root / "SKILLS" / lang
        if not public_skill_root.exists():
            errors.append(f"missing public shskills source: SKILLS/{lang}")
            continue

        # 清单技能名称必须等于公共目录实际技能名称。
        manifest_skill_names = names(manifest, "skills")
        public_skill_names = sorted(
            path.parent.name for path in public_skill_root.glob("cx-*/SKILL.md")
        )
        if public_skill_names != manifest_skill_names:
            errors.append(
                f"SKILLS/{lang} skill names do not match packages/{lang}/manifest.json"
            )

        # 每个技能同时比较文件集合和逐文件字节内容。
        for skill_name in manifest_skill_names:
            package_skill_root = package / ".agents" / "skills" / skill_name
            public_skill_directory = public_skill_root / skill_name
            package_files = relative_files(package_skill_root)
            public_files = relative_files(public_skill_directory)
            if package_files != public_files:
                errors.append(
                    f"public skill tree differs from package source: "
                    f"{public_skill_directory.relative_to(root)}"
                )
                continue
            # 相同相对路径的源文件与镜像必须逐字节一致。
            for relative_path in public_files:
                package_file = package_skill_root / relative_path
                public_file = public_skill_directory / relative_path
                if package_file.read_bytes() != public_file.read_bytes():
                    errors.append(
                        f"public skill file differs from package source: "
                        f"{public_file.relative_to(root)}"
                    )

    # 两个安装包只运行结构、元数据和单一来源静态验证器。
    for package in (en, zh):
        example = package / "examples" / "python_ml_project"
        # 当前发行合同明确不创建、不发现也不运行单元测试。
        for command, cwd in (
            ([sys.executable, "tools/validate_skill_pack.py", "."], package),
            ([sys.executable, "tools/validate_cx_pack.py", "."], package),
            (
                [sys.executable, str(package / "tools" / "validate_single_source.py")],
                example,
            ),
        ):
            code = run(command, cwd=cwd)
            if code != 0:
                errors.append(
                    f"validation failed in {package.relative_to(root)}: {' '.join(command)}"
                )

    # 任一静态问题都会阻止发行，并逐项输出真实失败原因。
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    # 所有静态合同满足后输出唯一成功标记。
    print("OK multilingual cx release validation passed")
    return 0


if __name__ == "__main__":
    # 模块入口把静态验证退出码原样交给终端和持续集成环境。
    raise SystemExit(main())
