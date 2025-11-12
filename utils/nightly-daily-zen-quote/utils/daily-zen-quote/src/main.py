"""
Daily Zen Quote – deterministic Zen quote of the day.

Provides a CLI that prints a quote based on the current date.
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
    "Be present, not perfect.",
    "All is water.",
    "The only constant is change.",
    "Know yourself, know the world."
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for the given date.

    If *date* is ``None``, uses today's date.
    """
    if date is None:
        date = datetime.date.today()
    # Compute index based on day of year (1‑366)
    index = (date.timetuple().tm_yday - 1) % len(_QUOTES)
    return _QUOTES[index]


def main() -> int:
    """CLI entry point."""
    quote = get_quote()
    print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
