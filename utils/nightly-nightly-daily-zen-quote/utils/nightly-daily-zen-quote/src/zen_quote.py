"""
zen_quote utility
Provides deterministic daily Zen quotes.
"""

from __future__ import annotations
import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go of what you cannot change.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Be present, not perfect.",
    "All we have is now.",
    "Nature does not hurry, yet everything is accomplished.",
    "Peace comes from within."
]


def get_zen_quote(date: datetime.date | None = None) -> str:
    """Return a deterministic Zen quote for the given date.

    If no date is provided, uses today's date.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """CLI entry point: prints today's Zen quote."""
    quote = get_zen_quote()
    print(quote)


if __name__ == "__main__":
    main()
