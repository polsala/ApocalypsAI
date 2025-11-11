"""git-branch-sanitizer

Utility to transform arbitrary strings into safe, kebab‑case Git branch names.

Provides both a library function `sanitize_branch_name` and a tiny CLI wrapper.
"""

import argparse
import re
from typing import Final

# Characters allowed in a Git branch name (simplified): alphanumerics, hyphens, underscores, slashes, and dots.
# For our sanitizer we restrict to alphanumerics and hyphens only.

_ALLOWED_PATTERN: Final = re.compile(r"[^a-z0-9-]")


def sanitize_branch_name(name: str) -> str:
    """Return a sanitized, kebab‑case version of *name*.

    Steps:
    1. Lower‑case the string.
    2. Replace spaces, underscores, and dots with hyphens.
    3. Remove any character not matching ``[a-z0-9-]``.
    4. Collapse multiple hyphens into a single hyphen.
    5. Strip leading/trailing hyphens.
    """
    # 1. Lower‑case
    sanitized = name.lower()
    # 2. Replace separators with hyphens
    sanitized = re.sub(r"[\s_\.]+", "-", sanitized)
    # 3. Remove illegal characters
    sanitized = _ALLOWED_PATTERN.sub("", sanitized)
    # 4. Collapse consecutive hyphens
    sanitized = re.sub(r"-+", "-", sanitized)
    # 5. Trim hyphens at the ends
    sanitized = sanitized.strip("-")
    return sanitized


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Sanitize a Git branch name into kebab‑case.")
    parser.add_argument("branch_name", help="The raw branch name to sanitize")
    args = parser.parse_args()
    print(sanitize_branch_name(args.branch_name))


if __name__ == "__main__":
    _cli()
