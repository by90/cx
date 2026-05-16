#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
import re


SEMVER_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\Z")


def load_manifest(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def names(data: dict[str, object], key: str) -> list[str]:
    return sorted(str(item["name"]) for item in data.get(key, []))


def run(command: list[str], cwd: Path) -> int:
    print("$ " + " ".join(command))
    completed = subprocess.run(command, cwd=cwd, text=True)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate cx multilingual release repository.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    en = root / "packages" / "en"
    zh = root / "packages" / "zh"
    errors: list[str] = []

    if not en.exists():
        errors.append("missing packages/en")
    if not zh.exists():
        errors.append("missing packages/zh")
    if not (root / "SKILLS").exists():
        errors.append("missing public SKILLS directory for shskills")
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1

    en_manifest = load_manifest(en / "manifest.json")
    zh_manifest = load_manifest(zh / "manifest.json")
    if en_manifest.get("version") != zh_manifest.get("version"):
        errors.append("package version mismatch between English and Chinese packages")
    if not SEMVER_RE.fullmatch(str(en_manifest.get("version", ""))):
        errors.append("package version must use semantic version format")
    for key in ("skills", "agents"):
        if names(en_manifest, key) != names(zh_manifest, key):
            errors.append(f"{key} mismatch between English and Chinese packages")

    readme_text = "\n".join(
        (root / name).read_text(encoding="utf-8") for name in ("README.md", "README.zh-CN.md")
    )
    if "shskills install" not in readme_text:
        errors.append("root README files must document direct shskills install/update")
    for obsolete in ("install-command", "scripts\\cx", "scripts/cx"):
        if obsolete in readme_text:
            errors.append(f"root README files must not require cloned cx scripts: {obsolete}")

    for lang, package, manifest in (("en", en, en_manifest), ("zh", zh, zh_manifest)):
        public_skill_root = root / "SKILLS" / lang
        if not public_skill_root.exists():
            errors.append(f"missing public shskills source: SKILLS/{lang}")
            continue

        manifest_skill_names = names(manifest, "skills")
        public_skill_names = sorted(path.parent.name for path in public_skill_root.glob("cx-*/SKILL.md"))
        if public_skill_names != manifest_skill_names:
            errors.append(f"SKILLS/{lang} skill names do not match packages/{lang}/manifest.json")

        for skill_name in manifest_skill_names:
            package_skill = package / ".agents" / "skills" / skill_name / "SKILL.md"
            public_skill = public_skill_root / skill_name / "SKILL.md"
            if not public_skill.exists():
                errors.append(f"missing public skill file: {public_skill.relative_to(root)}")
                continue
            if package_skill.read_text(encoding="utf-8") != public_skill.read_text(encoding="utf-8"):
                errors.append(
                    f"public skill differs from package source: {public_skill.relative_to(root)}"
                )

    for package in (en, zh):
        for command in (
            [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
            [sys.executable, "tools/validate_skill_pack.py", "."],
            [sys.executable, "tools/validate_cx_pack.py", "."],
            [sys.executable, "tools/validate_single_source.py", "examples/python_ml_project"],
        ):
            code = run(command, cwd=package)
            if code != 0:
                errors.append(f"validation failed in {package.relative_to(root)}: {' '.join(command)}")

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print("OK multilingual cx release validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
