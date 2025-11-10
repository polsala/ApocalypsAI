"""
Daily Zen Quote Generator

Provides a simple function to retrieve a random zen quote.
"""

import random
import argparse
from typing import List, Optional, Dict

_QUOTES: List[Dict[str, str]] = [
    {"text": "The journey of a thousand miles begins with one step.", "theme": "journey"},
    {"text": "When the mind is still, the universe surrenders.", "theme": "mind"},
    {"text": "Simplicity is the ultimate sophistication.", "theme": "simplicity"},
    {"text": "Let go of what you are, and become what you might be.", "theme": "growth"},
    {"text": "Silence is a source of great strength.", "theme": "silence"},
]


def get_quote(theme: Optional[str] = None) -> str:
    """
    Return a random quote. If theme is provided, only quotes matching the theme are considered.

    Args:
        theme: Optional theme to filter quotes.

    Returns:
        A quote string.

    Raises:
        ValueError: If no quotes match the given theme.
    """
    candidates = _QUOTES
    if theme:
        candidates = [q for q in _QUOTES if q["theme"] == theme]
        if not candidates:
            raise ValueError(f"No quotes found for theme '{theme}'.")
    chosen = random.choice(candidates)
    return chosen["text"]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random zen quote.")
    parser.add_argument(
        "--theme",
        type=str,
        help="Optional theme to filter quotes (e.g., 'mind', 'journey').",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        quote = get_quote(args.theme)
        print(quote)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
