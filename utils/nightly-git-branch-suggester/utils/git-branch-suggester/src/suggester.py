import argparse
import re
import sys
from typing import Optional


def _sanitize(text: str) -> str:
    """Convert *text* to a kebab‑case slug.

    Steps:
    1. Lower‑case.
    2. Replace any sequence of non‑alphanumeric characters with a single hyphen.
    3. Strip leading/trailing hyphens.
    """
    # Lower‑case and replace non‑alphanumeric with hyphen
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower())
    # Collapse multiple hyphens and trim
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def generate_branch(title: str, prefix: Optional[str] = None, ticket: Optional[str] = None) -> str:
    """Generate a kebab‑case branch name.

    Parameters
    ----------
    title: str
        Human‑readable description (e.g. issue title).
    prefix: str | None
        Optional prefix such as ``feature`` or ``bugfix``.
    ticket: str | int | None
        Optional ticket/issue identifier (will be stringified).
    """
    parts = []
    if prefix:
        parts.append(_sanitize(str(prefix)))
    if ticket:
        parts.append(str(ticket).strip())
    parts.append(_sanitize(title))
    return "-".join(parts)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a kebab‑case Git branch name from a title."
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Human‑readable title or description to base the branch name on.",
    )
    parser.add_argument(
        "--prefix",
        help="Optional prefix (e.g. 'feature', 'bugfix').",
    )
    parser.add_argument(
        "--ticket",
        help="Optional ticket/issue identifier (e.g. '123').",
    )
    return parser


def main(argv: Optional[list] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    branch = generate_branch(args.title, prefix=args.prefix, ticket=args.ticket)
    print(branch)
    return 0


if __name__ == "__main__":
    sys.exit(main())
