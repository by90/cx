"""Small SemVer release helper for Codex App and local maintainers."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from datetime import date
from pathlib import Path
from typing import Any

SEMVER = (
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?"
    r"(?:\+[0-9A-Za-z.-]+)?"
)
SEMVER_RE = re.compile(f"^{SEMVER}$")
VERSION_HEADING_RE = re.compile(rf"^## v({SEMVER})\b", re.MULTILINE)


class SemverError(ValueError):
    """Raised when version files or command arguments are invalid."""


def validate_semver(value: str) -> str:
    """Return a stripped SemVer value or fail with a clear message."""

    version = value.strip()
    if not SEMVER_RE.fullmatch(version):
        raise SemverError(f"{value!r} is not valid SemVer")
    return version


def release_tuple(version: str) -> tuple[int, int, int]:
    """Return the numeric SemVer core for simple forward comparisons."""

    core = version.split("-", 1)[0].split("+", 1)[0]
    major, minor, patch = core.split(".")
    return int(major), int(minor), int(patch)


def read_version(root: Path) -> str:
    """Read the repository VERSION source."""

    path = root / "VERSION"
    if not path.exists():
        raise SemverError("VERSION file is missing")
    return validate_semver(path.read_text(encoding="utf-8"))


def write_version(root: Path, version: str) -> None:
    """Write the repository VERSION source."""

    (root / "VERSION").write_text(f"{version}\n", encoding="utf-8")


def read_pyproject_version(root: Path) -> str | None:
    """Read [project].version from pyproject.toml when the file exists."""

    path = root / "pyproject.toml"
    if not path.exists():
        return None
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    try:
        version = data["project"]["version"]
    except KeyError as error:
        raise SemverError("pyproject.toml missing [project].version") from error
    return validate_semver(str(version))


def write_pyproject_version(root: Path, version: str) -> bool:
    """Replace [project].version when pyproject.toml exists."""

    path = root / "pyproject.toml"
    if not path.exists():
        return False
    lines = path.read_text(encoding="utf-8").splitlines()
    in_project = False
    replaced = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "[project]":
            in_project = True
            continue
        if stripped.startswith("[") and in_project:
            in_project = False
        if in_project and re.match(r"^version\s*=", stripped):
            lines[index] = f'version = "{version}"'
            replaced = True
            break
    if not replaced:
        raise SemverError("pyproject.toml missing [project].version")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def next_version(current: str, bump: str) -> str:
    """Return the next SemVer value for the project release rule."""

    major, minor, patch = release_tuple(validate_semver(current))
    if bump == "feature-group":
        return f"{major}.{minor + 1}.0"
    if bump in {"patch", "change", "bugfix", "adjustment"}:
        return f"{major}.{minor}.{patch + 1}"
    raise SemverError("bump must be feature-group or patch")


def read_documented_versions(root: Path) -> list[str]:
    """Read all valid version headings from docs/VERSIONS.md."""

    path = root / "docs" / "VERSIONS.md"
    if not path.exists():
        raise SemverError("docs/VERSIONS.md is missing")
    text = path.read_text(encoding="utf-8")
    bad_headings = [
        line
        for line in text.splitlines()
        if line.startswith("## v")
        and not re.match(rf"^## v{SEMVER}(?:\s+-\s+.+)?$", line)
    ]
    if bad_headings:
        raise SemverError(f"invalid version heading: {bad_headings[0]}")
    return [match.group(1) for match in VERSION_HEADING_RE.finditer(text)]


def insert_version_entry(
    root: Path,
    version: str,
    title: str,
    feature_group: str,
    summary: str,
    evidence: str,
) -> None:
    """Insert a new human-facing version entry in docs/VERSIONS.md."""

    path = root / "docs" / "VERSIONS.md"
    text = path.read_text(encoding="utf-8")
    if re.search(rf"^## v{re.escape(version)}\b", text, re.MULTILINE):
        raise SemverError(f"docs/VERSIONS.md already contains v{version}")
    entry = "\n".join(
        [
            f"## v{version} - {title}",
            "",
            f"- Date: {date.today().isoformat()}",
            f"- Feature groups: {feature_group}",
            f"- Summary: {summary}",
            f"- Source changes: see feature group CHANGELOG entries.",
            f"- Verification evidence: {evidence}",
            "",
        ]
    )
    first_version = re.search(r"^## ", text, re.MULTILINE)
    if first_version:
        before = text[: first_version.start()].rstrip()
        after = text[first_version.start() :].lstrip()
        new_text = f"{before}\n\n{entry}\n{after}"
    else:
        new_text = f"{text.rstrip()}\n\n{entry}"
    path.write_text(new_text, encoding="utf-8")


def check_version_files(root: Path) -> dict[str, Any]:
    """Validate SemVer files and return a machine-readable summary."""

    version = read_version(root)
    pyproject_version = read_pyproject_version(root)
    if pyproject_version is not None and pyproject_version != version:
        raise SemverError(
            f"pyproject.toml version {pyproject_version} does not match VERSION {version}"
        )
    documented_versions = read_documented_versions(root)
    return {
        "status": "ok",
        "version": version,
        "pyproject_version": pyproject_version,
        "documented_versions": documented_versions,
    }


def emit(data: dict[str, Any], json_output: bool) -> None:
    """Print command output for humans or Codex App JSON parsing."""

    if json_output:
        print(json.dumps(data, ensure_ascii=False, sort_keys=True))
        return
    for key, value in data.items():
        print(f"{key}: {value}")


def command_check(args: argparse.Namespace) -> int:
    """Handle the check subcommand."""

    root = Path(args.root).resolve()
    emit(check_version_files(root), args.json)
    return 0


def command_prepare(args: argparse.Namespace) -> int:
    """Handle the prepare subcommand."""

    root = Path(args.root).resolve()
    version = validate_semver(args.version)
    current = read_version(root)
    if release_tuple(version) <= release_tuple(current):
        raise SemverError(f"new version {version} must be greater than {current}")
    write_version(root, version)
    updated_files = ["VERSION", "docs/VERSIONS.md"]
    if write_pyproject_version(root, version):
        updated_files.insert(1, "pyproject.toml")
    insert_version_entry(
        root,
        version,
        args.title,
        args.feature_group,
        args.summary,
        args.evidence,
    )
    data = check_version_files(root)
    data["updated_files"] = updated_files
    emit(data, args.json)
    return 0


def command_next(args: argparse.Namespace) -> int:
    """Handle the next subcommand."""

    root = Path(args.root).resolve()
    current = read_version(root)
    version = next_version(current, args.bump)
    emit(
        {
            "status": "ok",
            "current_version": current,
            "bump": args.bump,
            "next_version": version,
        },
        args.json,
    )
    return 0


def git_output(root: Path, *args: str) -> str:
    """Run git and return stripped stdout."""

    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def command_tag(args: argparse.Namespace) -> int:
    """Handle the tag subcommand."""

    root = Path(args.root).resolve()
    version = read_version(root)
    tag = f"v{version}"
    branch = git_output(root, "branch", "--show-current")
    if branch != "main" and not args.allow_non_main:
        raise SemverError(
            "tag may only be created on main unless --allow-non-main is set"
        )
    exists = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
        capture_output=True,
        text=True,
    )
    if exists.returncode == 0:
        raise SemverError(f"tag {tag} already exists")
    message = args.message or f"Release {version}"
    subprocess.run(
        ["git", "-C", str(root), "tag", "-a", tag, "-m", message],
        check=True,
    )
    emit({"status": "ok", "tag": tag, "message": message}, args.json)
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description="Project SemVer helper")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=".", help="repository root")
    common.add_argument("--json", action="store_true", help="emit JSON output")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", parents=[common])
    check.set_defaults(func=command_check)

    next_parser = subparsers.add_parser("next", parents=[common])
    next_parser.add_argument(
        "bump",
        choices=["feature-group", "patch", "change", "bugfix", "adjustment"],
        help="feature-group bumps minor in 0.x.x; patch/change/bugfix/adjustment bumps patch",
    )
    next_parser.set_defaults(func=command_next)

    prepare = subparsers.add_parser("prepare", parents=[common])
    prepare.add_argument("version", help="new SemVer value without v prefix")
    prepare.add_argument("title", help="human-facing version title")
    prepare.add_argument("--feature-group", default="未指定")
    prepare.add_argument("--summary", default="未填写")
    prepare.add_argument("--evidence", default="未填写")
    prepare.set_defaults(func=command_prepare)

    tag = subparsers.add_parser("tag", parents=[common])
    tag.add_argument("--message", default=None)
    tag.add_argument("--allow-non-main", action="store_true")
    tag.set_defaults(func=command_tag)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command line interface."""

    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except SemverError as error:
        print(str(error), file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        print(error.stderr or str(error), file=sys.stderr)
        return error.returncode


if __name__ == "__main__":
    raise SystemExit(main())
