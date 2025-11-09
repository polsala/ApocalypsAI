"""suggester.py

Utility to generate a kebab‑case git branch name from an issue title.

The module provides:
- `suggest_branch_name(title: str, prefix: str = "feat") -> str`
- A small CLI wrapper using ``argparse``.

All logic is pure Python; no external services are called.
"""

import argparse
import re
from typing import Final

MAX_SLUG_LENGTH: Final[int] = 50

def _slugify(text: str) -> str:
    """Convert *text* to a kebab‑case slug.

    Steps:
    1. Lower‑case the string.
    2. Replace any sequence of non‑alphanumeric characters with a single hyphen.
    3. Strip leading/trailing hyphens.
    4. Collapse multiple hyphens.
    """
    # 1. lower case
    lowered = text.lower()
    # 2. replace non‑alnum with hyphen
    replaced = re.sub(r"[^a-z0-9]+", "-", lowered)
    # 3. strip hyphens
    stripped = replaced.strip("-")
    # 4. collapse multiple hyphens (already handled by regex, but keep for safety)
    collapsed = re.sub(r"-+", "-", stripped)
    return collapsed


def suggest_branch_name(title: str, prefix: str = "feat") -> str:
    """Return a branch name like ``"feat/add-user-login"``.

    The *title* is slugified and truncated to ``MAX_SLUG_LENGTH`` characters.
    The *prefix* is also slugified (to guard against accidental spaces).
    """
    if not title:
        raise ValueError("Title must be a non‑empty string")
    slug = _slugify(title)
    # Truncate to length limit while preserving whole words when possible
    if len(slug) > MAX_SLUG_LENGTH:
        # Cut at the last hyphen before the limit
        cut_point = slug.rfind("-", 0, MAX_SLUG_LENGTH)
        if cut_point == -1:
            slug = slug[:MAX_SLUG_LENGTH]
        else:
            slug = slug[:cut_point]
    clean_prefix = _slugify(prefix)
    return f"{clean_prefix}/{slug}"


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a kebab‑case git branch name from an issue title."
    )
    parser.add_argument("title", help="Issue or feature title to convert")
    parser.add_argument(
        "--prefix",
        default="feat",
        help="Branch prefix (default: 'feat')",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    try:
        branch = suggest_branch_name(args.title, args.prefix)
        print(branch)
    except ValueError as exc:
        # In a CLI context we exit with a non‑zero status
        print(f"Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
