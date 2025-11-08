#!/usr/bin/env python3
"""
branch-name-sanitizer

Provides a function to convert arbitrary strings into safe Git branch names
using kebab‑case rules.
"""

import re
import sys
from typing import Final

# Allowed characters after sanitization: lowercase letters, digits, hyphen
_ALLOWED_RE: Final[re.Pattern] = re.compile(r'[^a-z0-9-]')


def sanitize_branch_name(name: str) -> str:
    """
    Convert *name* into a Git‑compatible branch name.

    Steps:
    1. Lower‑case.
    2. Replace spaces, underscores, dots, and slashes with hyphens.
    3. Remove any character not in ``[a-z0-9-]``.
    4. Collapse consecutive hyphens.
    5. Strip leading/trailing hyphens.

    >>> sanitize_branch_name("Feature: Add New UI!")
    'feature-add-new-ui'
    """
    # 1. lower case
    s = name.lower()
    # 2. replace separators with hyphen
    s = re.sub(r'[\s_/\\.]+', '-', s)
    # 3. remove disallowed characters
    s = _ALLOWED_RE.sub('', s)
    # 4. collapse multiple hyphens
    s = re.sub(r'-{2,}', '-', s)
    # 5. strip hyphens
    s = s.strip('-')
    return s


def _cli() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python -m utils.branch-name-sanitizer.src.sanitizer <branch-name>",
            file=sys.stderr,
        )
        sys.exit(1)
    input_name = sys.argv[1]
    print(sanitize_branch_name(input_name))


if __name__ == "__main__":
    _cli()
