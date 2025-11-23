#!/usr/bin/env python3
"""
git_branch_sanitizer

Provides a function to sanitize strings into valid Git branch names.
"""

import re
import argparse
import sys
from typing import List


def sanitize_branch(name: str) -> str:
    """
    Convert an arbitrary string into a Git‑compatible branch name.

    Steps:
    1. Lower‑case the string.
    2. Replace spaces and underscores with hyphens.
    3. Remove characters other than alphanumerics, hyphens, slashes, and dots.
    4. Collapse consecutive hyphens.
    5. Strip leading/trailing hyphens or slashes.

    Parameters
    ----------
    name: str
        The raw branch name.

    Returns
    -------
    str
        A sanitized branch name.
    """
    # 1. lower case
    sanitized = name.lower()
    # 2. replace spaces and underscores with hyphens
    sanitized = re.sub(r"[\s_]+", "-", sanitized)
    # 3. keep only allowed characters
    sanitized = re.sub(r"[^a-z0-9\-./]+", "", sanitized)
    # 4. collapse multiple hyphens
    sanitized = re.sub(r"-{2,}", "-", sanitized)
    # 5. strip leading/trailing hyphens or slashes
    sanitized = sanitized.strip("-/")
    return sanitized


def _cli(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="git-branch-sanitizer",
        description="Sanitize a string into a safe Git branch name."
    )
    parser.add_argument("branch", help="Raw branch name to sanitize")
    args = parser.parse_args(argv)
    print(sanitize_branch(args.branch))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
