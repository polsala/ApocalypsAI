#!/usr/bin/env python3
"""
zen-quote-of-the-day

Prints a deterministic quote based on the supplied date (default: today).
The quote is selected by taking the date's ordinal value and using it as an
index into a static list of quotes.
"""

import argparse
import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "What you think, you become.",
    "The only constant is change.",
    "Be yourself; everyone else is already taken.",
    "In the middle of difficulty lies opportunity.",
    "When the mind is still, the universe surrenders.",
    "Let go or be dragged.",
    "The obstacle is the path.",
    "Silence is a source of great strength."
]


def _select_quote(date: datetime.date) -> str:
    """Return a quote deterministically chosen for *date*.

    The selection algorithm is simple and fully deterministic:
    ``index = date.toordinal() % len(_QUOTES)``.
    """
    idx = date.toordinal() % len(_QUOTES)
    return _QUOTES[idx]


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="zen-quote",
        description="Print a deterministic Zen quote for a given date."
    )
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="ISO date (YYYY-MM-DD). Defaults to today."
    )
    args = parser.parse_args(argv)

    target_date = args.date or datetime.date.today()
    quote = _select_quote(target_date)
    print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
