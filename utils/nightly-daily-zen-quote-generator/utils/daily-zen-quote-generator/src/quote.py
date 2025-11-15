"""
Daily Zen Quote Generator – deterministic quote of the day.

Provides `get_quote(date: datetime.date | None = None) -> str` which returns a
quote selected from a static list based on the supplied date (or today).
"""

from __future__ import annotations

import datetime
from typing import List

_QUOTES: List[str] = [
    "🧘 “The only limit to our realization of tomorrow is our doubts today.” – Franklin D. Roosevelt",
    "🌱 “In the middle of difficulty lies opportunity.” – Albert Einstein",
    "🚀 “What we think, we become.” – Buddha",
    "💡 “The best way to predict the future is to invent it.” – Alan Kay",
    "🌊 “Do not wait for the perfect moment, take the moment and make it perfect.” – Zoey",
]


def _select_index(target_date: datetime.date) -> int:
    """Return deterministic index for the given date."""
    return target_date.toordinal() % len(_QUOTES)


def get_quote(date: datetime.date | None = None) -> str:
    """
    Return the quote for *date*.

    If *date* is ``None`` the current local date is used.
    """
    if date is None:
        date = datetime.date.today()
    idx = _select_index(date)
    return _QUOTES[idx]


def main() -> None:
    """CLI entry‑point."""
    print(get_quote())


if __name__ == "__main__":
    main()
