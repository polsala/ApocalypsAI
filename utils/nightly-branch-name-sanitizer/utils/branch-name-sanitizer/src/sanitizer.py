"""branch-name-sanitizer utility

Provides a function to convert arbitrary strings into Git‑safe branch names.
"""

import re
import sys
from typing import Final

_MAX_LENGTH: Final[int] = 50

def _replace_invalid_chars(name: str) -> str:
    """Replace any character that is not a letter, digit, or hyphen with a hyphen.
    """
    # '# Mock rationale: we only need a simple regex; no external libs required.'
    return re.sub(r"[^a-z0-9-]", "-", name.lower())

def _collapse_hyphens(name: str) -> str:
    """Collapse consecutive hyphens into a single hyphen.
    """
    # '# Mock rationale: regex handles the collapse efficiently.'
    return re.sub(r"-+", "-", name)

def _trim(name: str) -> str:
    """Trim leading/trailing hyphens and enforce max length.
    """
    name = name.strip("-")
    if len(name) > _MAX_LENGTH:
        name = name[:_MAX_LENGTH].rstrip("-")
    return name

def _ensure_leading_letter(name: str) -> str:
    """If the name does not start with a letter, prepend 'branch-'.
    """
    if not name or not name[0].isalpha():
        name = f"branch-{name}"
    return name

def sanitize_branch_name(raw_name: str) -> str:
    """Convert *raw_name* into a Git‑safe, kebab‑case branch name.

    Steps:
    1. Lower‑case the input.
    2. Replace any non‑alphanumeric/hyphen character with a hyphen.
    3. Collapse multiple hyphens.
    4. Trim leading/trailing hyphens and enforce a 50‑char limit.
    5. Ensure the result starts with a letter.
    """
    if not isinstance(raw_name, str):
        raise TypeError("raw_name must be a string")
    name = _replace_invalid_chars(raw_name)
    name = _collapse_hyphens(name)
    name = _trim(name)
    name = _ensure_leading_letter(name)
    return name

def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.sanitizer <raw-branch-name>")
        sys.exit(1)
    raw = sys.argv[1]
    print(sanitize_branch_name(raw))

if __name__ == "__main__":
    _cli()
