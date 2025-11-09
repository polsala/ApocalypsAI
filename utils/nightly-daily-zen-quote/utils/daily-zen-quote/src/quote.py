"""
Daily Zen Quote – deterministic quote of the day.

Provides `get_quote(date: datetime.date | None = None) -> str`.
If `date` is None, uses today's date.
Selection is deterministic: index = date.toordinal() % len(_QUOTES).
"""

from __future__ import annotations

import datetime
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "What you think, you become.",
    "The only constant is change.",
    "Be yourself; everyone else is already taken.",
    "In the middle of difficulty lies opportunity.",
    "Dream big, start small, act now.",
    "Kindness is a language which the deaf can hear and the blind can see.",
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return the quote for the given date.

    Args:
        date: Optional date; defaults to today.

    Returns:
        A deterministic quote string.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """CLI entry point: prints today's quote."""
    print(get_quote())


if __name__ == "__main__":
    main()
