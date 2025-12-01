#!/usr/bin/env python3
"""
emoji_forecast – deterministic emoji weather forecast
"""

import sys
from datetime import datetime, date
from typing import Tuple

_WEATHER_MAP: Tuple[str, ...] = ("☀️", "☁️", "🌧️", "❄️")


def generate_forecast(target_date: date) -> str:
    """
    Return an emoji representing the weather for ``target_date``.
    Deterministic: based on day of year modulo len(_WEATHER_MAP).
    """
    day_of_year = target_date.timetuple().tm_yday
    index = day_of_year % len(_WEATHER_MAP)
    return _WEATHER_MAP[index]


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if argv:
        try:
            target = datetime.strptime(argv[0], "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            return 1
    else:
        target = date.today()
    forecast = generate_forecast(target)
    print(f"{target.isoformat()}: {forecast}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
