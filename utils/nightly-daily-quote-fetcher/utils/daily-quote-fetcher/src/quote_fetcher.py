#!/usr/bin/env python3
"""Quote fetcher utility.

Prints a random quote, optionally filtered by category.
"""

import argparse
import random
from typing import List, Dict

# Embedded quote database – keeps the utility offline.
QUOTES: List[Dict[str, str]] = [
    {"text": "The only limit to our realization of tomorrow is our doubts of today.", "category": "inspiration"},
    {"text": "Life is what happens when you're busy making other plans.", "category": "life"},
    {"text": "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.", "category": "philosophy"},
    {"text": "In the middle of difficulty lies opportunity.", "category": "inspiration"},
]


def get_quotes(category: str = None) -> List[Dict[str, str]]:
    """Return all quotes, optionally filtered by *category* (case‑insensitive)."""
    if category:
        filtered = [q for q in QUOTES if q["category"].lower() == category.lower()]
        return filtered
    return QUOTES


def pick_random(quotes: List[Dict[str, str]]) -> Dict[str, str]:
    """Pick a random quote from *quotes* list.

    Separated for easier mocking in tests.
    """
    return random.choice(quotes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random quote.")
    parser.add_argument(
        "--category",
        help="Filter quotes by category (e.g., inspiration, life, philosophy).",
    )
    args = parser.parse_args()
    available = get_quotes(args.category)
    if not available:
        print(f"No quotes found for category '{args.category}'.")
        return
    quote = pick_random(available)
    print(f'"{quote["text"]}" — {quote["category"].title()}')


if __name__ == "__main__":
    main()
