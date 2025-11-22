"""forecast.py

Provides a deterministic emoji "weather" forecast for a given date.

Functions:
    get_forecast(date: datetime.date) -> str
        Returns an emoji representing the forecast for *date*.

CLI usage:
    python -m forecast [YYYY-MM-DD]
        Prints the forecast for today or the supplied date.
"""

from __future__ import annotations

import argparse
import datetime
import sys
from typing import List

# List of emojis representing whimsical weather conditions.
EMOJIS: List[str] = [
    "☀️",  # Sunny
    "🌤️",  # Partly sunny
    "⛅",   # Cloudy
    "🌥️",  # Overcast
    "🌧️",  # Rainy
    "⛈️",  # Thunderstorm
    "❄️",  # Snowy
    "🌪️",  # Tornado (just for fun)
]


def get_forecast(date: datetime.date) -> str:
    """Return a deterministic emoji forecast for *date*.

    The forecast is chosen by taking the ordinal of the date modulo the number of emojis.
    """
    index = date.toordinal() % len(EMOJIS)
    return EMOJIS[index]


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic emoji weather forecast")
    parser.add_argument(
        "date",
        nargs="?",
        help="Date in YYYY-MM-DD format (defaults to today)",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            print(f"Invalid date format: {args.date}. Expected YYYY-MM-DD", file=sys.stderr)
            return 1
    else:
        target_date = datetime.date.today()

    forecast = get_forecast(target_date)
    print(f"Forecast for {target_date.isoformat()}: {forecast}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
