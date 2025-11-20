#!/usr/bin/env python3
"""
zen.py - Simple utility to display a random Zen quote.
"""

import random
import argparse
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "When the mind is still, the universe surrenders.",
    "Let go or be dragged.",
    "The obstacle is the path."
]

_ASCII_ART = r"""
      __
     /  \\
    |    |
    |    |
    |____|
   /______\\
"""


def get_random_quote() -> str:
    """Return a random Zen quote."""
    return random.choice(_QUOTES)


def format_quote(quote: str, art: bool = False) -> str:
    """Return formatted quote, optionally prefixed with ASCII art."""
    if art:
        return f"{_ASCII_ART}\n{quote}"
    return quote


def main() -> None:
    parser = argparse.ArgumentParser(description="Display a random Zen quote.")
    parser.add_argument(
        "-a",
        "--art",
        action="store_true",
        help="Include ASCII art with the quote"
    )
    args = parser.parse_args()
    quote = get_random_quote()
    print(format_quote(quote, art=args.art))


if __name__ == "__main__":
    main()
