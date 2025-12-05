import argparse
import re
from typing import List


def _normalize_token(token: str) -> str:
    """Return a lower‑cased alphanumeric token.

    Non‑alphanumeric characters are stripped; empty tokens are ignored.
    """
    cleaned = re.sub(r"[^a-z0-9]+", "", token.lower())
    return cleaned


def slugify(text: str, separator: str = "-") -> str:
    """Convert *text* into a kebab‑case slug.

    Steps:
    1. Split on whitespace and punctuation.
    2. Normalise each token (lower‑case, keep alphanumerics only).
    3. Join non‑empty tokens with *separator*.
    """
    # Split on any sequence of non‑word characters
    raw_tokens: List[str] = re.split(r"[\W_]+", text)
    tokens = [_normalize_token(tok) for tok in raw_tokens]
    # Filter out empty strings that may arise from stripping
    tokens = [t for t in tokens if t]
    return separator.join(tokens)


def build_branch_name(title: str, prefix: str | None = None, separator: str = "-") -> str:
    """Return a full branch name.

    If *prefix* is provided, it is slugified and prepended to the slugified title.
    """
    slug = slugify(title, separator=separator)
    if not slug:
        raise ValueError("Title produced an empty slug")
    if prefix:
        prefix_slug = slugify(prefix, separator=separator)
        return f"{prefix_slug}{separator}{slug}" if prefix_slug else slug
    return slug


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a kebab‑case Git branch name from a title.")
    parser.add_argument("title", help="The issue title or description to convert.")
    parser.add_argument("--prefix", help="Optional prefix (e.g. feat, fix, chore).", default=None)
    parser.add_argument(
        "--separator",
        help="Separator character to use (default: '-')",
        default="-",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    try:
        branch = build_branch_name(args.title, prefix=args.prefix, separator=args.separator)
        print(branch)
    except ValueError as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
