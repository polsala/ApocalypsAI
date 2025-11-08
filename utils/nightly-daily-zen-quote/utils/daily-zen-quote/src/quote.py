"""
Daily Zen Quote utility
Provides a deterministic quote based on the current date.
"""

import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "What you think, you become.",
    "The only constant is change.",
    "Be yourself; everyone else is already taken.",
    "In the middle of difficulty lies opportunity.",
    "Less is more.",
    "Patience is bitter, but its fruit is sweet.",
    "The obstacle is the path.",
    "Know thyself."
]


def _select_quote(date: datetime.date) -> str:
    """Select a quote deterministically based on the given date.

    The algorithm is simple and offline:
        index = (year + month + day) % len(_QUOTES)
    """
    idx = (date.year + date.month + date.day) % len(_QUOTES)
    return _QUOTES[idx]


def get_quote(date: datetime.date | None = None) -> str:
    """Return the zen quote for the given date (or today if None)."""
    if date is None:
        date = datetime.date.today()
    return _select_quote(date)


def main() -> None:
    """CLI entry point that prints today's quote."""
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    sys.exit(main())
