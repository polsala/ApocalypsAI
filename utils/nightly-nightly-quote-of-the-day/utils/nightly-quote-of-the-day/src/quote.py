#!/usr/bin/env python3
"""
quote.py - Print a random inspirational quote.

The utility is self‑contained and does not require network access.
"""

import random
import sys

# Built‑in collection of quotes
_QUOTES = [
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "Life is 10% what happens to us and 90% how we react to it. – Charles R. Swindoll",
    "The purpose of our lives is to be happy. – Dalai Lama",
    "Turn your wounds into wisdom. – Oprah Winfrey",
    "The best way to predict the future is to invent it. – Alan Kay",
]


def get_random_quote() -> str:
    """Return a random quote from the built‑in collection."""
    return random.choice(_QUOTES)


def main() -> None:
    """CLI entry point."""
    quote = get_random_quote()
    print(quote)


if __name__ == "__main__":
    # Ensure the script can be run directly
    main()
