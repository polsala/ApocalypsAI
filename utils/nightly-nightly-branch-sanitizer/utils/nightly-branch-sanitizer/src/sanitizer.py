import re
import sys
from typing import Final

_INVALID_RE: Final = re.compile(r'[^a-z0-9-]+')
_WHITESPACE_RE: Final = re.compile(r'[\s_]+')


def sanitize_branch(name: str) -> str:
    """
    Convert an arbitrary string into a safe Git branch name.

    Steps:
    1. Strip leading/trailing whitespace.
    2. Lower‑case.
    3. Replace spaces and underscores with a single hyphen.
    4. Remove any character that is not a‑z, 0‑9 or hyphen.
    5. Collapse consecutive hyphens.
    6. Trim leading/trailing hyphens.

    >>> sanitize_branch(" My Feature #1! ")
    'my-feature-1'
    """
    # 1 & 2
    cleaned = name.strip().lower()
    # 3
    cleaned = _WHITESPACE_RE.sub('-', cleaned)
    # 4
    cleaned = _INVALID_RE.sub('', cleaned)
    # 5
    cleaned = re.sub(r'-{2,}', '-', cleaned)
    # 6
    cleaned = cleaned.strip('-')
    return cleaned


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python sanitizer.py \"<branch name>\"")
        sys.exit(1)
    print(sanitize_branch(sys.argv[1]))


if __name__ == "__main__":
    _cli()
