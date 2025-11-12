import re
import sys
from typing import List, Optional


def _slugify(text: str) -> str:
    """Convert *text* to a kebab‑case slug.

    Steps:
    1. Lower‑case.
    2. Replace spaces and underscores with hyphens.
    3. Remove any character that is not alphanumeric or a hyphen.
    4. Collapse multiple hyphens.
    5. Strip leading/trailing hyphens.
    6. Truncate to 50 characters.
    """
    # 1. Lower‑case
    text = text.lower()
    # 2. Replace spaces/underscores with hyphens
    text = re.sub(r"[\s_]+", "-", text)
    # 3. Remove disallowed characters
    text = re.sub(r"[^a-z0-9-]", "", text)
    # 4. Collapse multiple hyphens
    text = re.sub(r"-+", "-", text)
    # 5. Strip hyphens at the ends
    text = text.strip("-")
    # 6. Truncate
    return text[:50]


def _resolve_conflict(base: str, existing: List[str]) -> str:
    """Append a numeric suffix to *base* until it is not in *existing*.

    The first conflict becomes ``base-1``.
    """
    if base not in existing:
        return base
    counter = 1
    while True:
        candidate = f"{base}-{counter}"
        if candidate not in existing:
            return candidate
        counter += 1


def generate_branch_name(title: str, existing_branches: Optional[List[str]] = None) -> str:
    """Public API: generate a unique branch name from *title*.

    Parameters
    ----------
    title:
        The raw string (e.g., an issue title).
    existing_branches:
        Optional list of branch names that already exist. If ``None`` an empty list is assumed.
    """
    if existing_branches is None:
        existing_branches = []
    slug = _slugify(title)
    unique = _resolve_conflict(slug, existing_branches)
    return unique


def _parse_existing(arg: str) -> List[str]:
    """Parse a comma‑separated string of existing branch names.

    This helper is used only by the CLI entry‑point.
    """
    return [b.strip() for b in arg.split(",") if b.strip()]


def main(argv: List[str] = None) -> int:
    """Simple CLI wrapper.

    Expected usage:
        python -m branch_name_generator "Some title" --existing "branch1,branch2"
    Returns exit code 0 on success.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Generate a kebab‑case Git branch name.")
    parser.add_argument("title", help="Raw title to convert")
    parser.add_argument(
        "--existing",
        default="",
        help="Comma‑separated list of existing branch names to avoid collisions",
    )
    args = parser.parse_args(argv)

    existing = _parse_existing(args.existing)
    result = generate_branch_name(args.title, existing)
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
