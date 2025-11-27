"""emoji_forecast
A tiny deterministic emoji‑weather generator.

Public API:
    get_forecast(date: datetime.date) -> str
    main() – CLI entry point
"""

from __future__ import annotations

import argparse
import datetime
import sys
from typing import List

# Mock rationale: deterministic, no external calls, pure stdlib.

EMOJIS: List[str] = [
    "☀️",  # Sunny
    "🌤️",  # Partly Cloudy
    "🌧️",  # Rainy
    "⛈️",  # Stormy
    "🌨️",  # Snowy
    "🌈",  # Rainbow
    "🌪️",  # Tornado
    "🌫️",  # Foggy
    "🌙",  # Clear Night
]


def _emoji_for_day(day_of_year: int) -> str:
    """Return the emoji corresponding to a day of the year.

    The mapping is deterministic: (day_of_year - 1) modulo the number of emojis.
    """
    index = (day_of_year - 1) % len(EMOJIS)
    return EMOJIS[index]


def get_forecast(date: datetime.date | None = None) -> str:
    """Return a human‑readable forecast string for *date*.

    If *date* is ``None`` the current local date is used.
    """
    if date is None:
        date = datetime.date.today()
    day_of_year = date.timetuple().tm_yday
    emoji = _emoji_for_day(day_of_year)
    return f"Today's forecast: {emoji}"


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic emoji weather forecast")
    parser.add_argument(
        "date",
        nargs="?",
        help="Date in YYYY-MM-DD format (defaults to today)",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            print(f"Error: invalid date format – {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = None
    forecast = get_forecast(target_date)
    print(forecast)


if __name__ == "__main__":
    main()
