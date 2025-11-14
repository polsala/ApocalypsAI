#!/usr/bin/env python3
"""
whimsical-quote-of-the-day

Prints a deterministic quote based on the current date.
"""

import argparse
import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "I’m not lazy, I’m on energy‑saving mode.",
    "If at first you don’t succeed, skydiving is not for you.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Life is short. Smile while you still have teeth.",
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return a quote deterministically chosen for *date*.

    If *date* is ``None`` the function uses ``datetime.date.today()``.
    The selection algorithm is:
        seed = (ISO week number * 7) + weekday
        index = seed % len(_QUOTES)
    This yields a stable quote for any calendar day without any randomness.
    """
    if date is None:
        date = datetime.date.today()
    # ISO week number (1‑53) and weekday (Monday=0 … Sunday=6)
    iso_week = date.isocalendar()[1]
    weekday = date.weekday()
    seed = iso_week * 7 + weekday
    return _QUOTES[seed % len(_QUOTES)]


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="quote-of-the-day",
        description="Print a whimsical quote of the day."
    )
    parser.add_argument(
        "--date",
        help="Override date in YYYY-MM-DD format (for testing).",
    )
    args = parser.parse_args(argv)

    if args.date:
        try:
            date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            print(f"Invalid date format: {exc}", file=sys.stderr)
            return 1
    else:
        date = None

    print(get_quote(date))
    return 0


if __name__ == "__main__":
    sys.exit(main())
