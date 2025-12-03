"""Zen Quote of the Day utility.

Provides a deterministic quote based on the calendar date.
"""

from __future__ import annotations

import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
    "Be like water.",
    "The only constant is change.",
    "Know yourself, know the world.",
    "Patience is a bitter plant, but its fruit is sweet."
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return a deterministic Zen quote for the given date.

    If *date* is None, uses today's date.
    """
    if date is None:
        date = datetime.date.today()
    # Day of year (1-366) modulo number of quotes
    index = (date.timetuple().tm_yday - 1) % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """CLI entry point: print today's quote."""
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    main()
