"""Quote Dispenser utility.

Provides a small CLI to print a random motivational quote.
All data is stored locally; no network access required.
"""

import argparse
import random
from typing import List, Optional, Dict

# Built‑in collection of quotes.
_QUOTES: List[Dict[str, List[str]]] = [
    {
        "text": "Believe you can and you're halfway there.",
        "author": "Theodore Roosevelt",
        "tags": ["inspiration", "confidence"]
    },
    {
        "text": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "tags": ["work", "passion"]
    },
    {
        "text": "Life is what happens when you're busy making other plans.",
        "author": "John Lennon",
        "tags": ["life", "humor"]
    },
    {
        "text": "If at first you don’t succeed, call it version 1.0.",
        "author": "Unknown",
        "tags": ["humor", "programming"]
    },
]


def _filter_quotes(tag: Optional[str]) -> List[Dict[str, List[str]]]:
    if tag is None:
        return _QUOTES
    return [q for q in _QUOTES if tag.lower() in (t.lower() for t in q["tags"])]


def get_random_quote(tag: Optional[str] = None) -> Dict[str, List[str]]:
    """Return a random quote dict optionally filtered by tag.

    Raises:
        ValueError: If no quotes match the supplied tag.
    """
    candidates = _filter_quotes(tag)
    if not candidates:
        raise ValueError(f"No quotes found for tag '{tag}'.")
    return random.choice(candidates)


def format_quote(quote: Dict[str, List[str]]) -> str:
    """Format a quote dict into a printable string."""
    return f"“{quote['text']}” – {quote['author']}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random motivational quote.")
    parser.add_argument(
        "--tag",
        help="Filter quotes by tag (e.g., inspiration, humor).",
        type=str,
        default=None,
    )
    args = parser.parse_args()
    try:
        quote = get_random_quote(args.tag)
        print(format_quote(quote))
    except ValueError as exc:
        print(exc)


if __name__ == "__main__":
    main()
