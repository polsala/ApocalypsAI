import argparse
import re
from typing import Optional


def _slugify(text: str) -> str:
    """Convert *text* to a kebab‑case slug.

    Steps:
    1. Lower‑case.
    2. Replace any run of non‑alphanumeric characters with a single hyphen.
    3. Strip leading/trailing hyphens.
    """
    lowered = text.lower()
    # Replace any sequence of characters that are not a‑z or 0‑9 with a hyphen
    slug = re.sub(r"[^a-z0-9]+", "-", lowered)
    return slug.strip("-")


def suggest_branch_name(description: str, issue_number: Optional[int] = None) -> str:
    """Return a kebab‑case branch name.

    If *issue_number* is provided, it is prefixed (e.g. ``42-fix-bug``).
    """
    base = _slugify(description)
    if issue_number is not None:
        return f"{issue_number}-{base}"
    return base


def _parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a kebab‑case git branch name from a description."
    )
    parser.add_argument(
        "description",
        help="Short description or issue title to turn into a branch name.",
    )
    parser.add_argument(
        "--issue",
        type=int,
        help="Optional issue number to prefix the branch name.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    branch = suggest_branch_name(args.description, args.issue)
    print(branch)


if __name__ == "__main__":
    main()
