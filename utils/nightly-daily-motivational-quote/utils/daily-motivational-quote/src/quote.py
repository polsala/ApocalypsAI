"""
Daily Motivational Quote utility.

Provides `get_random_quote` and a simple CLI.
"""

import argparse
import random
from typing import List, Optional, Dict

# Built‑in collection of quotes
_QUOTES: List[Dict[str, str]] = [
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "work"},
    {"text": "Life is what happens when you're busy making other plans.", "author": "John Lennon", "category": "life"},
    {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt", "category": "confidence"},
    {"text": "Do not wait to strike till the iron is hot; but make it hot by striking.", "author": "William Butler Yeats", "category": "action"},
    {"text": "The best time to plant a tree was 20 years ago. The second best time is now.", "author": "Chinese Proverb", "category": "growth"},
]


def get_random_quote(category: Optional[str] = None) -> Dict[str, str]:
    """Return a random quote, optionally filtered by *category*.

    Args:
        category: If provided, only quotes matching this category are considered.

    Returns:
        A dict with keys ``text`` and ``author``.
    """
    pool = _QUOTES
    if category:
        pool = [q for q in _QUOTES if q["category"] == category]
        if not pool:
            raise ValueError(f"No quotes found for category '{category}'.")
    chosen = random.choice(pool)
    return {"text": chosen["text"], "author": chosen["author"]}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random motivational quote.")
    parser.add_argument(
        "-c",
        "--category",
        help="Filter quotes by category (e.g., work, life, confidence).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        quote = get_random_quote(args.category)
        print(f'"{quote["text"]}" — {quote["author"]}')
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
