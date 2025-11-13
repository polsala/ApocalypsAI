"""
quote.py - deterministic daily Zen quote selector.
"""

import datetime
import sys
from typing import List, Optional

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
]


def _filter_by_theme(quotes: List[str], theme: Optional[str]) -> List[str]:
    if not theme:
        return quotes
    theme_lower = theme.lower()
    return [q for q in quotes if theme_lower in q.lower()]


def get_quote(date: Optional[datetime.date] = None, theme: Optional[str] = None) -> str:
    """
    Return a deterministic quote for the given date and optional theme.
    If no quote matches the theme, fall back to the full list.
    """
    if date is None:
        date = datetime.date.today()
    pool = _filter_by_theme(_QUOTES, theme)
    if not pool:
        pool = _QUOTES
    # Deterministic index based on date ordinal and theme hash
    seed = date.toordinal() + (hash(theme) if theme else 0)
    index = seed % len(pool)
    return pool[index]


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Print a daily Zen quote.")
    parser.add_argument(
        "--theme",
        "-t",
        help="Optional theme to filter quotes (case‑insensitive).",
    )
    args = parser.parse_args()
    quote = get_quote(theme=args.theme)
    print(quote)


if __name__ == "__main__":
    main()
