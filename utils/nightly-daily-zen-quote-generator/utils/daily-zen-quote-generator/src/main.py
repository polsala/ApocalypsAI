#!/usr/bin/env python3
"""
Daily Zen Quote Generator

Prints a random Zen‑inspired quote. Optionally filter by tag.
"""

import argparse
import random
import sys
from typing import List, Optional, Tuple

Quote = Tuple[str, List[str]]  # (text, tags)

_QUOTES: List[Quote] = [
    ("The journey of a thousand miles begins with one step.", ["motivation", "zen"]),
    ("When the mind is still, the universe surrenders.", ["mindfulness", "zen"]),
    ("Simplicity is the ultimate sophistication.", ["simplicity", "zen"]),
    ("Let go of the illusion of control.", ["freedom", "zen"]),
    ("Silence is a source of great strength.", ["silence", "zen"]),
]


def get_random_quote(tag: Optional[str] = None) -> str:
    """Return a random quote, optionally filtered by a tag.

    Args:
        tag: Optional tag to filter quotes.
    Raises:
        ValueError: If no quotes match the provided tag.
    """
    if tag:
        filtered = [q for q, tags in _QUOTES if tag.lower() in (t.lower() for t in tags)]
        if not filtered:
            raise ValueError(f"No quotes found for tag '{tag}'.")
        pool = filtered
    else:
        pool = [q for q, _ in _QUOTES]
    # Mock rationale: random.choice is deterministic when patched in tests.
    return random.choice(pool)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="daily-zen-quote-generator",
        description="Print a random Zen‑inspired quote."
    )
    parser.add_argument(
        "-t", "--tag",
        help="Filter quotes by tag (e.g., 'mindfulness')."
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    try:
        quote = get_random_quote(args.tag)
        print(quote)
        return 0
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
