"""Quote Keeper utility.

Provides a simple API to retrieve random quotes, optionally filtered by tag.
Can be used as a library or via ``python -m src.quote_keeper``.
"""

import argparse
import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class Quote:
    text: str
    author: str
    tags: List[str]

# Built‑in collection of quotes.
_QUOTES: List[Quote] = [
    Quote(
        text="The only limit to our realization of tomorrow is our doubts of today.",
        author="Franklin D. Roosevelt",
        tags=["motivation", "future"],
    ),
    Quote(
        text="In the middle of difficulty lies opportunity.",
        author="Albert Einstein",
        tags=["inspiration", "challenge"],
    ),
    Quote(
        text="Life is what happens when you're busy making other plans.",
        author="John Lennon",
        tags=["life"],
    ),
    Quote(
        text="Be yourself; everyone else is already taken.",
        author="Oscar Wilde",
        tags=["humor", "self"],
    ),
]


def _filter_by_tag(quotes: List[Quote], tag: str) -> List[Quote]:
    """Return only quotes that contain *tag* (case‑insensitive)."""
    return [q for q in quotes if tag.lower() in (t.lower() for t in q.tags)]


def get_random_quote(tag: Optional[str] = None) -> Quote:
    """Return a random :class:`Quote`.

    Args:
        tag: Optional tag to filter the quote pool.

    Raises:
        ValueError: If a tag is supplied but no quotes match.
    """
    pool = _QUOTES
    if tag:
        pool = _filter_by_tag(pool, tag)
        if not pool:
            raise ValueError(f"No quotes found for tag '{tag}'.")
    return random.choice(pool)


def _format_quote(q: Quote) -> str:
    return f'"{q.text}"\n  — {q.author}'


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Print a random inspirational quote.")
    parser.add_argument(
        "--tag",
        help="Filter quotes by tag (e.g., motivation, humor).",
    )
    args = parser.parse_args(argv)

    try:
        quote = get_random_quote(args.tag)
    except ValueError as exc:
        parser.error(str(exc))
        return 2  # argparse error code

    print(_format_quote(quote))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
