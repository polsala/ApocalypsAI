import re
import sys
from typing import List

DEFAULT_TYPE = "feat"
KNOWN_TYPES = {"feat", "fix", "chore", "docs", "style", "refactor", "test", "build"}


def _slugify(text: str) -> str:
    """Convert arbitrary text to a kebab‑case slug.

    Steps:
    1. Drop non‑ASCII characters (including emojis).
    2. Replace any non‑alphanumeric sequence with a single space.
    3. Split on whitespace, lower‑case, and join with hyphens.
    """
    # Remove emojis and other non‑ASCII characters
    text = text.encode("ascii", "ignore").decode()
    # Replace non‑alphanumeric characters with spaces
    text = re.sub(r"[^A-Za-z0-9]+", " ", text)
    parts = text.strip().lower().split()
    return "-".join(parts)


def generate_branch_name(title: str) -> str:
    """Convert an issue title into a conventional git branch name.

    The function looks for an optional leading type keyword (e.g. "Fix:", "Docs -").
    If found and recognised, that keyword becomes the branch prefix; otherwise the
    default prefix ``feat`` is used. The remainder of the title is slugified.

    Examples
    --------
    >>> generate_branch_name("Fix typo in README")
    'fix/typo-in-readme'
    >>> generate_branch_name("Add user login page")
    'feat/add-user-login-page'
    """
    # Detect a leading type keyword followed by punctuation/space
    prefix_match = re.match(r"^\s*([A-Za-z]+)[\s:/-]+", title)
    branch_type = DEFAULT_TYPE
    remainder = title
    if prefix_match:
        possible = prefix_match.group(1).lower()
        if possible in KNOWN_TYPES:
            branch_type = possible
            remainder = title[prefix_match.end():]

    slug = _slugify(remainder)
    if not slug:
        slug = "unnamed"
    return f"{branch_type}/{slug}"


def _cli():
    if len(sys.argv) != 2:
        print("Usage: python -m branch_namer \"Issue title\"")
        sys.exit(1)
    print(generate_branch_name(sys.argv[1]))

if __name__ == "__main__":
    _cli()
