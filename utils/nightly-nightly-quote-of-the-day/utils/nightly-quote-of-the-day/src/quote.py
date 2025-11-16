"""Quote of the Day utility.

Provides a deterministic quote based on the supplied date (or today).
"""

from __future__ import annotations

import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "Life is 10% what happens to us and 90% how we react to it. – Charles R. Swindoll",
    "The purpose of our lives is to be happy. – Dalai Lama",
    "Turn your wounds into wisdom. – Oprah Winfrey",
    "The best way to predict the future is to invent it. – Alan Kay",
    "In the middle of difficulty lies opportunity. – Albert Einstein",
    "Stay hungry, stay foolish. – Steve Jobs",
    "Do not wait to strike till the iron is hot; but make it hot by striking. – William Butler Yeats",
    "What we think, we become. – Buddha",
    "The journey of a thousand miles begins with one step. – Lao Tzu",
]


def _select_index(date: datetime.date) -> int:
    """Return an index into _QUOTES based on the day of year."""
    # Use day of year (1-366) modulo number of quotes
    return (date.timetuple().tm_yday - 1) % len(_QUOTES)


def get_quote(date: datetime.date | None = None) -> str:
    """Return a deterministic quote for the given date.

    Args:
        date: Optional date; defaults to today in UTC.

    Returns:
        A quote string.
    """
    if date is None:
        date = datetime.datetime.utcnow().date()
    idx = _select_index(date)
    return _QUOTES[idx]


def _cli() -> None:
    """Simple CLI entry point."""
    if len(sys.argv) > 1:
        try:
            # Mock rationale: parsing user‑provided date string
            date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        except ValueError as exc:
            print(f"Invalid date format: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        date = None
    print(get_quote(date))


if __name__ == "__main__":
    _cli()
