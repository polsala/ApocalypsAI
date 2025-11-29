"""quote_of_the_day.py

Provides a deterministic *Quote of the Day* based on the current date.

Public API
----------
- ``get_quote(date: datetime.date | None = None) -> str``
- ``main()`` – CLI entry point that prints the quote.
"""

from __future__ import annotations

import datetime
import random
from typing import List

# A small, curated list of quotes. Feel free to extend.
_QUOTES: List[str] = [
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "In the middle of difficulty lies opportunity. – Albert Einstein",
    "What we think, we become. – Buddha",
    "The best way to predict the future is to invent it. – Alan Kay",
    "Life is what happens when you're busy making other plans. – John Lennon",
]


def _seed_for_date(date: datetime.date) -> int:
    """Return a deterministic seed derived from *date*.

    Using ``date.toordinal()`` yields a stable integer for any given calendar day.
    """
    return date.toordinal()


def get_quote(date: datetime.date | None = None) -> str:
    """Return the quote for *date*.

    If *date* is ``None`` the function uses ``datetime.date.today()``.
    The selection is deterministic: the same date always yields the same quote.
    """
    if date is None:
        date = datetime.date.today()
    seed = _seed_for_date(date)
    rng = random.Random(seed)
    return rng.choice(_QUOTES)


def main() -> None:
    """CLI entry point – prints the quote for today to stdout."""
    print(get_quote())


if __name__ == "__main__":
    main()
