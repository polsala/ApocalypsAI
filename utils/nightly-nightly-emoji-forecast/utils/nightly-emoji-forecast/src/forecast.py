"""
Emoji Weather Forecast Utility
Provides a whimsical emoji‑based weather forecast for a given date.
Deterministic: uses the date's ordinal to select a forecast.
"""

import sys
from datetime import datetime, date
from typing import List

WEATHER_EMOJIS: List[str] = [
    "☀️ Sunny",
    "🌤️ Partly Cloudy",
    "☁️ Cloudy",
    "🌧️ Rainy",
    "⛈️ Stormy",
    "❄️ Snowy",
    "🌪️ Windy",
    "🌈 Rainbow",
]


def get_forecast(target_date: date) -> str:
    """Return an emoji weather forecast string for the given date."""
    index = target_date.toordinal() % len(WEATHER_EMOJIS)
    return WEATHER_EMOJIS[index]


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    * No arguments → forecast for today.
    * One argument → date in ``YYYY-MM-DD`` format.
    """
    argv = argv or sys.argv[1:]
    if argv:
        try:
            target = datetime.strptime(argv[0], "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            return 1
    else:
        target = date.today()
    print(get_forecast(target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
