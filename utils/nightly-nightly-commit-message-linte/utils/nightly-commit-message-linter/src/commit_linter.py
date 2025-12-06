"""commit_linter.py

A tiny validator for Conventional Commits subject lines.

Usage:
    python -m nightly_commit_message_linter [path]
    # If *path* is omitted, reads from stdin.

Exit codes:
    0 – valid
    1 – invalid
"""

import re
import sys
from pathlib import Path
from typing import List

# Allowed types according to Conventional Commits (a subset that covers most cases)
ALLOWED_TYPES = {
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "chore",
    "build",
    "ci",
    "revert",
}

# Regex for the subject line:
#   type(optional(scope))?: description
#   - type: one of ALLOWED_TYPES
#   - scope: any non‑empty string without parentheses
#   - description: at least one non‑space character, should not end with a period
SUBJECT_REGEX = re.compile(
    r"^(?P<type>{types})(\((?P<scope>[^)]+)\))?: (?P<desc>.+)$".format(
        types="|".join(sorted(ALLOWED_TYPES))
    )
)


def load_message(source: str | None) -> str:
    """Return the commit message string.

    If *source* is ``None`` read from ``stdin``; otherwise treat it as a file path.
    """
    if source is None:
        return sys.stdin.read()
    return Path(source).read_text(encoding="utf-8")


def validate_subject(subject: str) -> List[str]:
    """Validate a single subject line.

    Returns a list of error strings; empty list means the subject is valid.
    """
    errors: List[str] = []
    match = SUBJECT_REGEX.match(subject.strip())
    if not match:
        errors.append(
            "Subject does not match '<type>(<scope>)?: <description>' pattern."
        )
        return errors

    # Additional sanity checks on description
    desc = match.group("desc")
    if desc.endswith('.'):
        errors.append("Description should not end with a period.")
    if desc[0].isupper():
        errors.append("Description should start with a lowercase letter.")
    return errors


def main(argv: List[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    source_path = argv[0] if argv else None
    message = load_message(source_path)
    # Only the first line matters for this linter
    subject = message.splitlines()[0] if message else ""
    errors = validate_subject(subject)
    if errors:
        print("Invalid commit message:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("Commit message is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
