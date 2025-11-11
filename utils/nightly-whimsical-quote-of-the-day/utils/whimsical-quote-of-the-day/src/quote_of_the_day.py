"""quote_of_the_day
~~~~~~~~~~~~~~~~~~
Provides a deterministic "quote of the day" based on the current date.

Public API
----------
- ``get_quote(date: datetime.date | None = None) -> str``
- ``main()`` – CLI entry point
"""

from __future__ import annotations

import argparse
import datetime
import sys
from typing import List

# A curated list of whimsical, inspirational quotes.
_QUOTES: List[str] = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "Dreams are like rainbows – only visible when you chase them.",
    "When life gives you lemons, make lemonade… and then find someone whose life gave them vodka.",
    "A journey of a thousand miles begins with a single step… onto the couch.",
    "If at first you don’t succeed, redefine success.",
    "The only constant is change – except for taxes and this quote list.",
    "Be yourself; everyone else is already taken.",
    "In the middle of difficulty lies opportunity – and maybe a snack.",
    "Do not go gentle into that good night; rage, rage against the coffee shortage.",
    "Life is short. Smile while you still have teeth.",
]


def _index_for_date(target_date: datetime.date) -> int:
    """Return a deterministic index into ``_QUOTES`` for *target_date*.

    The algorithm is deliberately simple: convert the date to its ordinal
    (days since 0001‑01‑01) and take the modulo length of the quote list.
    """
    return target_date.toordinal() % len(_QUOTES)


def get_quote(date: datetime.date | None = None) -> str:
    """Return the quote for *date* (defaults to ``datetime.date.today()``).

    Parameters
    ----------
    date: datetime.date | None
        The date for which to retrieve the quote. If ``None`` the current
        local date is used.
    """
    if date is None:
        date = datetime.date.today()
    idx = _index_for_date(date)
    return _QUOTES[idx]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quote_of_the_day",
        description="Print a deterministic inspirational quote for today.",
    )
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Optional date (YYYY-MM-DD) to fetch the quote for.",
    )
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    quote = get_quote(args.date)
    print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
