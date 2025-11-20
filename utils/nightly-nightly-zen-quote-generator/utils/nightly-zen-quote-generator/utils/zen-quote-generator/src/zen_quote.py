"""Zen Quote Generator utility.

Provides a CLI to print a random Zen quote, optionally filtered by tag.
"""

import argparse
import random
import sys
from typing import List, Dict, Optional

_QUOTES: List[Dict[str, object]] = [
    {"text": "The obstacle is the path.", "author": "Zen Proverb", "tags": ["mindfulness"]},
    {"text": "When you realize nothing is lacking, the whole world belongs to you.", "author": "Zen Proverb", "tags": ["mindfulness", "gratitude"]},
    {"text": "If you cannot find the truth within yourself, look outside.", "author": "Zen Proverb", "tags": ["humor"]},
    {"text": "A journey of a thousand miles begins with a single step.", "author": "Lao Tzu", "tags": ["motivation"]},
    {"text": "The quieter you become, the more you can hear.", "author": "Ram Dass", "tags": ["mindfulness"]},
]


def _filter_quotes(tag: Optional[str]) -> List[Dict[str, object]]:
    if tag is None:
        return _QUOTES
    filtered = [q for q in _QUOTES if tag in q["tags"]]
    if not filtered:
        raise ValueError(f"No quotes found for tag '{tag}'.")
    return filtered


def get_random_quote(tag: Optional[str] = None) -> Dict[str, object]:
    """Return a random quote dict, optionally filtered by tag."""
    candidates = _filter_quotes(tag)
    return random.choice(candidates)


def format_quote(quote: Dict[str, object]) -> str:
    return f"“{quote['text']}” – {quote['author']}"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument("--tag", help="Filter quotes by tag.")
    args = parser.parse_args(argv)

    try:
        quote = get_random_quote(args.tag)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(format_quote(quote))
    return 0


if __name__ == "__main__":
    sys.exit(main())
