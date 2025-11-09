#!/usr/bin/env python3
"""
Utility to sanitize Git branch names into a safe kebab‑case format.
"""

import re
import sys
from typing import List


def sanitize_branch(name: str) -> str:
    """Convert a branch name to a safe kebab‑case string.

    Steps:
    1. Strip leading/trailing whitespace.
    2. Replace spaces and underscores with hyphens.
    3. Remove characters that are not alphanumeric, hyphen, or dot.
    4. Collapse multiple hyphens into one.
    5. Lowercase the result.
    6. Ensure it does not start or end with a hyphen.
    """
    # 1
    sanitized = name.strip()
    # 2
    sanitized = re.sub(r"[ _]+", "-", sanitized)
    # 3
    sanitized = re.sub(r"[^a-zA-Z0-9\-.]", "", sanitized)
    # 4
    sanitized = re.sub(r"-{2,}", "-", sanitized)
    # 5
    sanitized = sanitized.lower()
    # 6
    sanitized = sanitized.strip("-")
    return sanitized


def main(argv: List[str] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: sanitize_branch.py <branch-name>", file=sys.stderr)
        return 1
    name = argv[0]
    print(sanitize_branch(name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
