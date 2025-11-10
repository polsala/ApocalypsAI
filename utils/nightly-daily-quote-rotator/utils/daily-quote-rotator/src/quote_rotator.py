"""Daily Quote Rotator utility.

Provides a deterministic quote for a given date.
"""

from __future__ import annotations

import argparse
import datetime
import sys
from typing import List

# A small offset to make the rotation start away from the first quote.
_OFFSET = 7

_QUOTES: List[str] = [
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "Life is 10% what happens to us and 90% how we react to it. – Charles R. Swindoll",
    "The purpose of our lives is to be happy. – Dalai Lama",
    "Turn your wounds into wisdom. – Oprah Winfrey",
    "The best way to predict the future is to invent it. – Alan Kay",
    "You miss 100% of the shots you don’t take. – Wayne Gretzky",
    "In the middle of difficulty lies opportunity. – Albert Einstein",
    "What we think, we become. – Buddha",
    "The journey of a thousand miles begins with one step. – Lao Tzu",
    "Stay hungry, stay foolish. – Steve Jobs",
]


def get_quote_for_date(date: datetime.date) -> str:
    """Return the deterministic quote for *date*.
    """
    index = (date.toordinal() + _OFFSET) % len(_QUOTES)
    return _QUOTES[index]


def parse_date(arg: str) -> datetime.date:
    """Parse a YYYY‑MM‑DD string into a date, raising argparse.ArgumentTypeError on failure.
    """
    try:
        return datetime.datetime.strptime(arg, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date format: {arg!r}. Expected YYYY-MM-DD.") from exc


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print a deterministic daily quote.")
    parser.add_argument(
        "date",
        nargs="?",
        type=parse_date,
        help="Date in YYYY-MM-DD format. Defaults to today.",
    )
    args = parser.parse_args(argv)

    target_date = args.date or datetime.date.today()
    quote = get_quote_for_date(target_date)
    print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
