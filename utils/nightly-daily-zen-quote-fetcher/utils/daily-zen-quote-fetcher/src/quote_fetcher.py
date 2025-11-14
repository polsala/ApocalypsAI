"""Daily Zen Quote Fetcher utility.

Provides a deterministic quote based on the current date.
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
    "Peace comes from within. Do not seek it without.",
]


def _select_quote_for_date(date: datetime.date) -> str:
    """Select a quote based on the given date.

    Deterministic: uses the ordinal of the date modulo the number of quotes.
    """
    index = date.toordinal() % len(_QUOTES)
    return _QUOTES[index]


def get_today_quote() -> str:
    """Return the quote for today."""
    today = datetime.date.today()
    return _select_quote_for_date(today)


def main() -> None:
    """CLI entry point."""
    print(get_today_quote())


if __name__ == "__main__":
    main()
