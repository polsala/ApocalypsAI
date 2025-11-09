#!/usr/bin/env python3
"""
Daily Zen Quote Generator

Provides a deterministic "Zen" quote for a given date (defaults to today).
Useful for adding a touch of inspiration to scripts, CI logs, or terminal prompts.
"""

import argparse
import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
    "In the middle of difficulty lies opportunity.",
    "Be like water.",
    "All is flux, nothing stays the same.",
    "Know yourself, know the world."
]


def _quote_index_for(date: datetime.date) -> int:
    """Deterministically map a date to an index in _QUOTES.

    The algorithm combines the ISO year and week number, then mods by the
    number of available quotes. This yields a stable, repeatable mapping that
    changes roughly weekly.
    """
    year, week, _ = date.isocalendar()
    return (year * 100 + week) % len(_QUOTES)


def get_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for the given date (or today)."""
    if date is None:
        date = datetime.date.today()
    idx = _quote_index_for(date)
    return _QUOTES[idx]


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="zen-quote",
        description="Print a deterministic Zen quote for today (or a given date)."
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date in YYYY-MM-DD format. Defaults to today."
    )
    args = parser.parse_args(argv)

    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            print(f"Invalid date format: {exc}", file=sys.stderr)
            return 1
    else:
        target_date = datetime.date.today()

    print(get_quote(target_date))
    return 0


if __name__ == "__main__":
    sys.exit(main())
