"""Zen Quote utility.

Provides random Zen‑inspired quotes, optionally filtered by category.
"""

import argparse
import random
import sys
from typing import List, Optional

_QUOTES = {
    "life": [
        "The journey of a thousand miles begins with one step.",
        "Life is a series of natural and spontaneous changes.",
    ],
    "work": [
        "Choose a job you love, and you will never have to work a day in your life.",
        "Quality is not an act, it is a habit.",
    ],
    "nature": [
        "In every walk with nature one receives far more than he seeks.",
        "The earth has music for those who listen.",
    ],
    "default": [
        "Simplicity is the ultimate sophistication.",
        "The only constant is change.",
    ],
}


def _flatten_quotes() -> List[str]:
    """Return a flat list of all quotes across categories."""
    all_quotes: List[str] = []
    for cat_quotes in _QUOTES.values():
        all_quotes.extend(cat_quotes)
    return all_quotes


def get_random_quote(category: Optional[str] = None) -> str:
    """Return a random quote.

    Args:
        category: Optional category name. If omitted or unknown, selects from all quotes.

    Returns:
        A randomly chosen quote string.
    """
    if category and category in _QUOTES:
        pool = _QUOTES[category]
    else:
        pool = _flatten_quotes()
    # Mock rationale: deterministic selection is achieved in tests via patching random.choice.
    return random.choice(pool)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print a random Zen‑inspired quote.")
    parser.add_argument(
        "--category",
        choices=list(_QUOTES.keys()),
        help="Quote category (default: any).",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    quote = get_random_quote(args.category)
    print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
