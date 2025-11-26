"""Emoji Weather Forecast utility.

Provides a deterministic, whimsical \"weather\" emoji based on a given date.
"""

from __future__ import annotations

import datetime
import sys
from typing import List

EMOJIS: List[str] = ["☀️", "🌤️", "⛅", "🌥️", "☁️", "🌧️", "⛈️", "❄️"]


def get_emoji_forecast(date: datetime.date) -> str:
    """Return an emoji representing the forecast for *date*.

    The algorithm is deterministic and offline:
    1. Compute the sum of year, month, and day.
    2. Take the remainder modulo the number of emojis.
    3. Return the emoji at that index.
    """
    idx = (date.year + date.month + date.day) % len(EMOJIS)
    return EMOJIS[idx]


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Usage:
        python -m nightly_emoji_forecast src/forecast.py [YYYY-MM-DD]

    If a date is omitted, today's date is used.
    """
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) > 1:
        print("Usage: forecast.py [YYYY-MM-DD]")
        return 1

    if argv:
        try:
            target_date = datetime.date.fromisoformat(argv[0])
        except ValueError:
            print(f"Invalid date format: {argv[0]!r}. Expected YYYY-MM-DD.")
            return 1
    else:
        target_date = datetime.date.today()

    forecast = get_emoji_forecast(target_date)
    print(f"Forecast for {target_date.isoformat()}: {forecast}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
