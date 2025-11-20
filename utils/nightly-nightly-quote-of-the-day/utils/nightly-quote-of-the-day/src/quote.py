#!/usr/bin/env python3
"""
quote.py - Print a random quote.

Usage:
    python -m src.quote [--category CATEGORY]

If CATEGORY is provided, only quotes from that category are considered.
"""

import argparse
import random
from typing import List, Tuple

# Built‑in collection of quotes (text, author, category)
_QUOTES: List[Tuple[str, str, str]] = [
    ("The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt", "inspiration"),
    ("Life is what happens when you're busy making other plans.", "John Lennon", "life"),
    ("In the middle of difficulty lies opportunity.", "Albert Einstein", "wisdom"),
    ("Be yourself; everyone else is already taken.", "Oscar Wilde", "humor"),
    ("Do or do not. There is no try.", "Yoda", "fiction"),
]


def get_quotes(category: str | None = None) -> List[Tuple[str, str, str]]:
    """Return list of quotes, optionally filtered by category."""
    if category:
        filtered = [q for q in _QUOTES if q[2] == category.lower()]
        return filtered
    return _QUOTES


def pick_random(quotes: List[Tuple[str, str, str]]) -> Tuple[str, str, str]:
    """Pick a random quote from the list."""
    return random.choice(quotes)


def format_quote(quote: Tuple[str, str, str]) -> str:
    """Format a quote tuple for display."""
    text, author, _ = quote
    return f'"{text}" — {author}'


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random inspirational quote.")
    parser.add_argument(
        "--category",
        help="Filter quotes by category (e.g., inspiration, life, wisdom, humor, fiction).",
    )
    args = parser.parse_args()
    quotes = get_quotes(args.category)
    if not quotes:
        print(f"No quotes found for category '{args.category}'.")
        return
    selected = pick_random(quotes)
    print(format_quote(selected))


if __name__ == "__main__":
    main()
