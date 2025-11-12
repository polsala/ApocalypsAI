#!/usr/bin/env python3
"""
Daily Zen Quote Generator

Provides a deterministic quote of the day from a static list.
"""

import sys
from datetime import datetime, date
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "What you think, you become.",
    "The only constant is change.",
    "Be yourself; everyone else is already taken."
]


def _select_quote(target_date: date) -> str:
    """Deterministically select a quote based on the date.

    The index is calculated as (year + month + day) % len(_QUOTES).
    """
    idx = (target_date.year + target_date.month + target_date.day) % len(_QUOTES)
    return _QUOTES[idx]


def get_quote(target_date: date | None = None) -> str:
    """Return the quote for *target_date* (defaults to today in UTC)."""
    if target_date is None:
        target_date = datetime.utcnow().date()
    return _select_quote(target_date)


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Prints the quote of the day. Optional argument: ``YYYY-MM-DD`` to get a quote for a specific date.
    """
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) > 1:
        print("Usage: daily-zen-quote-generator [YYYY-MM-DD]", file=sys.stderr)
        return 1

    if argv:
        try:
            target = datetime.strptime(argv[0], "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            return 1
    else:
        target = None

    print(get_quote(target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
