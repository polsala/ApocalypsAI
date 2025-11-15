#!/usr/bin/env python3
"""
Daily Zen Quote: deterministic daily Zen quote provider.
"""

import argparse
import datetime
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
    "Be like water.",
    "The only constant is change.",
    "Know yourself, know the universe.",
    "Patience is bitter, but its fruit is sweet."
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return the Zen quote for the given date (or today if None)."""
    if date is None:
        date = datetime.date.today()
    index = (date.timetuple().tm_yday - 1) % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    parser = argparse.ArgumentParser(description="Print today's Zen quote.")
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Specify a date (YYYY-MM-DD) to get its quote."
    )
    args = parser.parse_args()
    quote = get_quote(args.date)
    print(quote)


if __name__ == "__main__":
    main()
