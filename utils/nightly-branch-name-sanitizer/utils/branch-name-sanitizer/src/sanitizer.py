"""branch_name_sanitizer/src/sanitizer.py

Utility functions for sanitizing Git branch names.

The main public function is :func:`sanitize_branch_name` which applies a series of
transformations to make a branch name safe for remote URLs and CI pipelines.
"""

import re
from typing import Final

# Characters allowed after sanitisation: lowercase letters, digits, hyphen
_ALLOWED_RE: Final[re.Pattern] = re.compile(r"[^a-z0-9-]")


def _collapse_hyphens(name: str) -> str:
    """Replace multiple consecutive hyphens with a single hyphen.

    Args:
        name: The intermediate branch name.
    Returns:
        A string with no duplicate hyphens.
    """
    return re.sub(r"-+", "-", name)


def sanitize_branch_name(name: str) -> str:
    """Return a URL‑friendly version of *name*.

    The sanitisation steps are:

    1. Strip surrounding whitespace.
    2. Lower‑case the string.
    3. Replace spaces and underscores with hyphens.
    4. Remove any character that is not a lowercase letter, digit, or hyphen.
    5. Collapse consecutive hyphens.
    6. Trim leading/trailing hyphens.

    The function never raises; any input yields a string (possibly empty).

    Args:
        name: Arbitrary branch name.
    Returns:
        Sanitised branch name.
    """
    # 1. Trim whitespace
    sanitized = name.strip()
    # 2. Lower‑case
    sanitized = sanitized.lower()
    # 3. Replace spaces and underscores with hyphens
    sanitized = sanitized.replace(" ", "-").replace("_", "-")
    # 4. Remove disallowed characters
    sanitized = _ALLOWED_RE.sub("", sanitized)
    # 5. Collapse hyphens
    sanitized = _collapse_hyphens(sanitized)
    # 6. Trim leading/trailing hyphens
    sanitized = sanitized.strip("-")
    return sanitized


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Sanitize a Git branch name.")
    parser.add_argument("branch", help="Branch name to sanitise")
    args = parser.parse_args()
    print(sanitize_branch_name(args.branch))
