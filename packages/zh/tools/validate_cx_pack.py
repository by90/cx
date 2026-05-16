#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover
    tomllib = None


CX_NAME_RE = re.compile(r"cx-[a-z0-9][a-z0-9-]*\Z")
SEMVER_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\Z")


def load_toml(path: Path) -> dict[str, object]:
    if tomllib is None:
        raise RuntimeError("Python 3.11+ is required for TOML validation")
    return tomllib.loads(path.read_text(encoding="utf-8"))


def validate_manifest(root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = root / "manifest.json"
    if not manifest_path.exists():
        return ["missing manifest.json"]
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("package") != "cx":
        errors.append("manifest package must be cx")
    version = str(data.get("version", ""))
    if not SEMVER_RE.fullmatch(version):
        errors.append("manifest version must use semantic version format")
    for item in data.get("skills", []):
        name = item.get("name", "")
        path = root / item.get("path", "")
        if not CX_NAME_RE.fullmatch(name):
            errors.append(f"manifest skill name is not cx kebab-case: {name!r}")
        if not path.exists():
            errors.append(f"manifest skill path does not exist: {path.relative_to(root)}")
    for item in data.get("agents", []):
        name = item.get("name", "")
        path = root / item.get("path", "")
        if not CX_NAME_RE.fullmatch(name):
            errors.append(f"manifest agent name is not cx kebab-case: {name!r}")
        if not path.exists():
            errors.append(f"manifest agent path does not exist: {path.relative_to(root)}")
    return errors


def validate_agents(root: Path) -> list[str]:
    errors: list[str] = []
    agent_files = sorted(root.glob(".codex/agents/*.toml"))
    if not agent_files:
        return ["no custom agent TOML files found under .codex/agents"]
    seen: set[str] = set()
    for path in agent_files:
        data = load_toml(path)
        name = str(data.get("name", ""))
        description = str(data.get("description", ""))
        instructions = str(data.get("developer_instructions", ""))
        if not CX_NAME_RE.fullmatch(name):
            errors.append(f"{path.relative_to(root)}: agent name must start with cx- and use kebab-case: {name!r}")
        if path.stem != name:
            errors.append(f"{path.relative_to(root)}: file stem must match agent name {name!r}")
        if not description or len(description) < 20:
            errors.append(f"{path.relative_to(root)}: description missing or too short")
        if not instructions or len(instructions) < 80:
            errors.append(f"{path.relative_to(root)}: developer_instructions missing or too short")
        if name in seen:
            errors.append(f"duplicate agent name: {name}")
        seen.add(name)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate cx package manifest and Codex custom agents.")
    parser.add_argument("root", nargs="?", default=".", help="Package root")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    errors = validate_manifest(root) + validate_agents(root)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print("OK cx package metadata and custom agents passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
