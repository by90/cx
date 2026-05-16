#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


CHANGE_ID_RE = re.compile(r"CHANGE-(\d{4})-(\d{3})")


def next_change_id(changelog_text: str, year: int) -> str:
    numbers = [int(match.group(2)) for match in CHANGE_ID_RE.finditer(changelog_text) if int(match.group(1)) == year]
    next_number = max(numbers, default=0) + 1
    return f"CHANGE-{year}-{next_number:03d}"


def build_entry(change_id: str, title: str, change_type: str, today: str) -> str:
    return f"""
### {change_id} - {title}

- Date: {today}
- Type: {change_type}
- Summary: TODO
- Engineering spec sections: TODO
- Related BDD scenarios: TODO
- Related tests: TODO
- Verification evidence: TODO
""".strip()


def append_change(root: Path, title: str, change_type: str, today: str | None = None) -> str:
    changelog_path = root / "docs" / "CHANGELOG.md"
    changelog_path.parent.mkdir(parents=True, exist_ok=True)
    text = changelog_path.read_text(encoding="utf-8") if changelog_path.exists() else "# CHANGELOG.md\n\n## Unreleased\n"
    actual_today = today or dt.date.today().isoformat()
    year = int(actual_today[:4])
    change_id = next_change_id(text, year)
    entry = build_entry(change_id, title, change_type, actual_today)

    if "## Unreleased" in text:
        text = text.replace("## Unreleased", f"## Unreleased\n\n{entry}", 1)
    else:
        text = text.rstrip() + f"\n\n## Unreleased\n\n{entry}\n"

    changelog_path.write_text(text, encoding="utf-8")
    return change_id


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a CHANGE-* template to docs/CHANGELOG.md")
    parser.add_argument("title")
    parser.add_argument("--type", default="feature", choices=["feature", "bugfix", "refactor", "test", "docs", "research"])
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    change_id = append_change(Path(args.root).resolve(), args.title, args.type)
    print(change_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
