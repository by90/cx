#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


def read_version(root: Path) -> str:
    return (root / "VERSION").read_text(encoding="utf-8").strip()


def manifest_paths(root: Path) -> list[Path]:
    return [root / "packages" / "en" / "manifest.json", root / "packages" / "zh" / "manifest.json"]


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    version_path = root / "VERSION"
    changelog_path = root / "CHANGELOG.md"

    if not version_path.exists():
        return ["missing VERSION"]

    version = read_version(root)
    if not SEMVER_RE.fullmatch(version):
        errors.append(f"VERSION must be a SemVer 2.0.0 value without a leading v: {version!r}")

    for path in manifest_paths(root):
        if not path.exists():
            errors.append(f"missing {path.relative_to(root)}")
            continue
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest.get("version") != version:
            errors.append(f"{path.relative_to(root)} version must equal VERSION {version}")

    if not changelog_path.exists():
        errors.append("missing CHANGELOG.md")
    else:
        changelog = changelog_path.read_text(encoding="utf-8")
        if "## [Unreleased]" not in changelog:
            errors.append("CHANGELOG.md must keep a top-level ## [Unreleased] section")
        release_heading = re.compile(rf"^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$", re.MULTILINE)
        if not release_heading.search(changelog):
            errors.append(f"CHANGELOG.md must contain a dated section for [{version}]")

    return errors


def write_version(root: Path, version: str) -> None:
    if not SEMVER_RE.fullmatch(version):
        raise ValueError(f"not a SemVer 2.0.0 value: {version}")

    (root / "VERSION").write_text(version + "\n", encoding="utf-8")
    for path in manifest_paths(root):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["version"] = version
        path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def bump(current: str, part: str) -> str:
    match = SEMVER_RE.fullmatch(current)
    if not match:
        raise ValueError(f"current VERSION is not SemVer: {current}")
    if match.group(4) or match.group(5):
        raise ValueError("automatic bump only supports stable X.Y.Z versions")

    major, minor, patch = (int(match.group(index)) for index in (1, 2, 3))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage the cx package release version.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    show_parser = subparsers.add_parser("show", help="Print VERSION")
    show_parser.add_argument("root", nargs="?", default=".", help="Repository root")

    check_parser = subparsers.add_parser("check", help="Validate VERSION, manifests, and CHANGELOG.md")
    check_parser.add_argument("root", nargs="?", default=".", help="Repository root")

    set_parser = subparsers.add_parser("set", help="Set VERSION and package manifest versions")
    set_parser.add_argument("root", help="Repository root")
    set_parser.add_argument("version", help="SemVer value such as 2.0.0")

    bump_parser = subparsers.add_parser("bump", help="Bump stable VERSION and package manifest versions")
    bump_parser.add_argument("root", help="Repository root")
    bump_parser.add_argument("part", choices=("major", "minor", "patch"))

    args = parser.parse_args()
    root = Path(args.root).resolve()

    try:
        if args.command == "show":
            print(read_version(root))
            return 0
        if args.command == "check":
            errors = validate(root)
            for error in errors:
                print(f"ERROR {error}")
            if errors:
                return 1
            print("OK cx version metadata passed")
            return 0
        if args.command == "set":
            write_version(root, args.version)
            print(args.version)
            return 0
        if args.command == "bump":
            next_version = bump(read_version(root), args.part)
            write_version(root, next_version)
            print(next_version)
            return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
