"""daily-zen-quote utility

Provides a deterministic Zen quote based on the current date.

Public API:
    - get_daily_quote(date: Optional[datetime.date] = None) -> str
    - main() – CLI entry point
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from typing import List, Optional

# A short collection of Zen‑style quotes. Feel free to extend.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the middle of difficulty lies opportunity.",
    "Nature does not hurry, yet everything is accomplished.",
    "The only constant is change.",
    "Know the rules well, so you can break them wisely.",
    "A single spark can start a great fire.",
]


def _day_of_year(target_date: date) -> int:
    """Return the day of year (1‑365/366) for *target_date*.

    This helper is isolated for easier testing and potential mocking.
    """
    return target_date.timetuple().tm_yday


def get_daily_quote(target_date: Optional[date] = None) -> str:
    """Return a deterministic Zen quote for *target_date*.

    If *target_date* is ``None`` the current local date is used.
    The quote is selected by computing ``day_of_year % len(QUOTES)``.
    """
    if target_date is None:
        target_date = date.today()
    day_index = _day_of_year(target_date) % len(QUOTES)
    return QUOTES[day_index]


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a deterministic daily Zen quote.")
    parser.add_argument(
        "--date",
        type=str,
        help="Optional date in YYYY-MM-DD format. Defaults to today.",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    args = _parse_args(argv)
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            print(f"Error: invalid date format '{args.date}'. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = None
    quote = get_daily_quote(target_date)
    print(quote)


if __name__ == "__main__":
    main()
