"""quote_of_the_day.py

Provides a deterministic "quote of the day" based on the current date.

The algorithm:
1. Compute the day-of-year (1‑366) for the given date.
2. Modulo the number of quotes to pick an index.
3. Return the quote at that index.

Both a library function (`get_quote_of_the_day`) and a CLI entry point are exposed.
"""

from __future__ import annotations

import datetime
import sys
from typing import List

# A curated list of whimsical quotes. Feel free to expand!
QUOTES: List[str] = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "I intend to live forever. So far, so good.",
    "If at first you don't succeed, skydiving is not for you.",
    "I am not lazy, I am on energy‑saving mode.",
    "Why do we press harder on a remote control when we know the batteries are dead?",
    "I told my computer I needed a break, and it gave me a coffee mug.",
    "The universe is made of stories, not atoms.",
    "If you think nobody cares if you're alive, try missing a couple of payments.",
    "Life is short. Smile while you still have teeth.",
    "I put the "pro" in procrastination.",
]


def _day_of_year(date: datetime.date) -> int:
    """Return the day of year (1‑366) for *date*.

    This helper exists to make testing easier – it can be mocked.
    """
    return date.timetuple().tm_yday


def get_quote_of_the_day(date: datetime.date | None = None) -> str:
    """Return the quote for *date*.

    If *date* is ``None`` the current local date is used.
    The selection is deterministic: the same date always yields the same quote.
    """
    if date is None:
        date = datetime.date.today()
    day_index = (_day_of_year(date) - 1) % len(QUOTES)
    return QUOTES[day_index]


def _cli() -> None:
    """CLI entry point.

    Prints the quote for today to stdout.
    """
    quote = get_quote_of_the_day()
    print(quote)


if __name__ == "__main__":
    # Allow optional date argument for manual testing: ``python -m ... <YYYY-MM-DD>``
    if len(sys.argv) > 1:
        try:
            custom_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
        print(get_quote_of_the_day(custom_date))
    else:
        _cli()
