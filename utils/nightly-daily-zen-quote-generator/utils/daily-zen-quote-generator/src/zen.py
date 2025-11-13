"""Daily Zen Quote Generator.

Provides `get_quote(theme: str | None = None) -> str` and a CLI entry point.
"""

import argparse
import random
from typing import List, Dict, Optional

# Mock rationale: static list of quotes to avoid external dependencies.
QUOTES: List[Dict[str, str]] = [
    {"quote": "The journey of a thousand miles begins with one step.", "theme": "perseverance"},
    {"quote": "Nature does not hurry, yet everything is accomplished.", "theme": "nature"},
    {"quote": "When you realize nothing is lacking, the whole world belongs to you.", "theme": "mindfulness"},
    {"quote": "Fall seven times, stand up eight.", "theme": "perseverance"},
    {"quote": "The oak tree does not grow in a day.", "theme": "nature"},
]


def get_quote(theme: Optional[str] = None) -> str:
    """Return a random quote, optionally filtered by theme.

    Args:
        theme: If provided, only quotes matching this theme are considered.
               Matching is case‑insensitive.

    Returns:
        A quote string.

    Raises:
        ValueError: If no quotes match the requested theme.
    """
    if theme:
        filtered = [q["quote"] for q in QUOTES if q["theme"].lower() == theme.lower()]
        if not filtered:
            raise ValueError(f"No quotes found for theme '{theme}'.")
        pool = filtered
    else:
        pool = [q["quote"] for q in QUOTES]

    # Mock rationale: using random.choice for simplicity; tests patch it.
    return random.choice(pool)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--theme",
        type=str,
        help="Optional theme to filter quotes (e.g., nature, mindfulness, perseverance).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        quote = get_quote(args.theme)
        print(quote)
    except ValueError as exc:
        print(exc)


if __name__ == "__main__":
    main()
