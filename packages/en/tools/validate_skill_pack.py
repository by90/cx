#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", re.DOTALL)
KEY_VALUE_RE = re.compile(r"^(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.+?)\s*$")
CX_NAME_RE = re.compile(r"cx-[a-z0-9][a-z0-9-]*\Z")
SEMVER_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\Z")


@dataclass(frozen=True)
class SkillValidationResult:
    path: Path
    ok: bool
    errors: tuple[str, ...]


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}

    values: dict[str, str] = {}
    for line in match.group("body").splitlines():
        parsed = KEY_VALUE_RE.match(line.strip())
        if parsed:
            values[parsed.group("key")] = parsed.group("value").strip().strip('"')
    return values


def validate_skill_file(path: Path) -> SkillValidationResult:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    errors: list[str] = []

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    version = frontmatter.get("version", "")

    if not name:
        errors.append("missing frontmatter field: name")
    elif not CX_NAME_RE.fullmatch(name):
        errors.append(f"skill name must start with cx- and use lowercase kebab-case: {name!r}")

    if name and path.parent.name != name:
        errors.append(f"skill directory must match name: directory={path.parent.name!r}, name={name!r}")

    if not description:
        errors.append("missing frontmatter field: description")
    elif len(description) < 40:
        errors.append("description is too short to trigger reliably")

    if not version:
        errors.append("missing frontmatter field: version")
    elif not SEMVER_RE.fullmatch(version):
        errors.append(f"version must use semantic version format: {version!r}")

    if len(text.split()) < 80:
        errors.append("skill body is too short to be useful")

    return SkillValidationResult(path=path, ok=not errors, errors=tuple(errors))


def validate_skill_tree(root: Path) -> list[SkillValidationResult]:
    skill_files = sorted(root.glob(".agents/skills/*/SKILL.md"))
    results = [validate_skill_file(path) for path in skill_files]

    seen: dict[str, Path] = {}
    for result in list(results):
        name = parse_frontmatter(result.path.read_text(encoding="utf-8")).get("name", "")
        if not name:
            continue
        if name in seen:
            duplicate_error = f"duplicate skill name {name!r}; first seen at {seen[name]}"
            results.append(SkillValidationResult(result.path, False, (duplicate_error,)))
        else:
            seen[name] = result.path

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate cx Codex Agent Skill files.")
    parser.add_argument("root", nargs="?", default=".", help="Package or repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    results = validate_skill_tree(root)

    if not results:
        print("No skill files found under .agents/skills/*/SKILL.md")
        return 1

    failed = [result for result in results if not result.ok]
    for result in results:
        relative_path = result.path.relative_to(root)
        if result.ok:
            print(f"OK   {relative_path}")
        else:
            print(f"FAIL {relative_path}")
            for error in result.errors:
                print(f"  - {error}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
