#!/usr/bin/env python3
"""
emoji_forecast: deterministic emoji weather forecast based on date.
"""

import sys
from datetime import datetime, date

WEATHER_CYCLE = ["☀️", "⛅", "🌧️", "❄️"]  # sun, partly cloudy, rain, snow


def get_forecast(target_date: date) -> str:
    """Return an emoji representing the weather for the given date.

    Deterministic: uses day of year modulo length of ``WEATHER_CYCLE``.
    """
    day_of_year = target_date.timetuple().tm_yday
    index = day_of_year % len(WEATHER_CYCLE)
    return WEATHER_CYCLE[index]


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python -m emoji_forecast <YYYY-MM-DD>")
        sys.exit(1)
    try:
        target = datetime.strptime(argv[0], "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)
    print(get_forecast(target))


if __name__ == "__main__":
    main()
