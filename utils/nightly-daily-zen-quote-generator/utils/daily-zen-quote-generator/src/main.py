#!/usr/bin/env python3
"""
Daily Zen Quote Generator – deterministic quote of the day.

Provides:
- `get_quote_of_the_day(date: datetime.date | None = None) -> str`
- CLI entry point printing the quote.
"""

from __future__ import annotations
import datetime
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step. – Lao Tzu",
    "What you think, you become. – Buddha",
    "Simplicity is the ultimate sophistication. – Leonardo da Vinci",
    "Stay hungry, stay foolish. – Steve Jobs",
    "In the middle of difficulty lies opportunity. – Albert Einstein",
]


def get_quote_of_the_day(date: datetime.date | None = None) -> str:
    """Return the quote for the given date.

    If *date* is ``None``, uses today's date.
    The selection is deterministic: ``(date.toordinal() % len(_QUOTES))``.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def _main() -> None:
    quote = get_quote_of_the_day()
    print(quote)


if __name__ == "__main__":
    _main()
