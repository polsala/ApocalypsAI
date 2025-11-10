#!/usr/bin/env python3
"""
Simple Conventional Commits linter.
"""

import re
import sys
from pathlib import Path
from typing import List

# Allowed types per Conventional Commits
ALLOWED_TYPES = {
    "feat", "fix", "docs", "style", "refactor", "perf",
    "test", "build", "ci", "chore", "revert"
}

HEADER_REGEX = re.compile(
    r"^(?P<type>\w+)(\((?P<scope>[^)]+)\))?(?P<breaking>!)?: (?P<description>.+)$"
)

def is_valid_header(line: str) -> bool:
    """Validate the first line of a commit message."""
    match = HEADER_REGEX.match(line.strip())
    if not match:
        return False
    commit_type = match.group("type")
    return commit_type in ALLOWED_TYPES

def lint_message(message: str) -> List[str]:
    """Return a list of error strings; empty list means the message is valid."""
    lines = message.strip("\n").splitlines()
    if not lines:
        return ["Commit message is empty."]
    header = lines[0]
    errors = []
    if not is_valid_header(header):
        errors.append(f"Invalid header: '{header}'")
    # Optional: enforce blank line after header if body exists
    if len(lines) > 1 and lines[1].strip() != "":
        errors.append("Second line should be blank when body is present.")
    return errors

def read_message(path: str = None) -> str:
    """Read commit message from a file or stdin."""
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Conventional Commits linter")
    parser.add_argument("path", nargs="?", help="Path to commit message file")
    args = parser.parse_args()
    msg = read_message(args.path)
    errors = lint_message(msg)
    if errors:
        for err in errors:
            print(f"❌ {err}", file=sys.stderr)
        return 1
    print("✅ Commit message looks good.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
