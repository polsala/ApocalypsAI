"""
Daily motivation quote utility
Provides random motivational quotes.
"""

import random
import sys
from typing import List, Optional, Dict

# Built‑in collection of quotes
QUOTES: List[Dict[str, str]] = [
    {
        "text": "The only limit to our realization of tomorrow is our doubts of today.",
        "author": "Franklin D. Roosevelt",
        "category": "inspiration",
    },
    {
        "text": "I am not lazy, I am on energy‑saving mode.",
        "author": "Anonymous",
        "category": "humor",
    },
    {
        "text": "Knowledge speaks, but wisdom listens.",
        "author": "Jimi Hendrix",
        "category": "wisdom",
    },
    {
        "text": "Dream big and dare to fail.",
        "author": "Norman Vaughan",
        "category": "inspiration",
    },
]


def get_random_quote(category: Optional[str] = None) -> Dict[str, str]:
    """
    Return a random quote dict. If ``category`` is provided, only quotes
    matching that category are considered.

    Raises:
        ValueError: If no quotes match the requested category.
    """
    pool = QUOTES
    if category:
        pool = [q for q in QUOTES if q["category"] == category.lower()]
        if not pool:
            raise ValueError(f"No quotes found for category '{category}'.")
    return random.choice(pool)


def format_quote(quote: Dict[str, str]) -> str:
    """Pretty‑print a quote with an emoji based on its category."""
    emoji_map = {
        "inspiration": "💡",
        "humor": "😂",
        "wisdom": "🧠",
    }
    emoji = emoji_map.get(quote["category"], "✨")
    return f'{emoji} "{quote["text"]}" – {quote["author"]}'


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Print a random motivational quote."
    )
    parser.add_argument(
        "--category",
        help="Filter quotes by category (inspiration, humor, wisdom).",
    )
    args = parser.parse_args(argv)

    try:
        quote = get_random_quote(args.category)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(format_quote(quote))
    return 0


if __name__ == "__main__":
    sys.exit(main())
