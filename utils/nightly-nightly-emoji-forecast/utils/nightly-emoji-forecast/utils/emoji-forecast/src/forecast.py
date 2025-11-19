#!/usr/bin/env python3
"""
emoji_forecast – generate a deterministic emoji weather forecast.

The forecast is based on a fixed mapping of weather conditions to emojis.
A pseudo‑random generator seeded with the ISO date string ensures the same
output for the same date without any network calls.
"""

import sys
import datetime
import random
from typing import List

# Mapping of weather conditions to emojis
WEATHER_EMOJIS: List[tuple[str, str]] = [
    ("Sunny", "🌞"),
    ("Partly Cloudy", "⛅"),
    ("Cloudy", "☁️"),
    ("Rainy", "🌧️"),
    ("Stormy", "⛈️"),
    ("Snowy", "❄️"),
    ("Windy", "🌬️"),
    ("Foggy", "🌫️"),
]


def generate_forecast(date: datetime.date) -> str:
    """Return a deterministic forecast string for the given date.

    The function seeds ``random`` with the ISO representation of ``date`` so
    that the same date always yields the same forecast.
    """
    # Seed random with ISO date string for reproducibility
    random.seed(date.isoformat())
    condition, emoji = random.choice(WEATHER_EMOJIS)
    # Simple chance of a secondary condition
    if random.random() < 0.3:
        secondary, sec_emoji = random.choice(WEATHER_EMOJIS)
        return f"{emoji} {condition} with a chance of {sec_emoji} {secondary}."
    return f"{emoji} {condition}."


def main(argv: List[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if argv:
        try:
            target_date = datetime.date.fromisoformat(argv[0])
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            return 1
    else:
        target_date = datetime.date.today()
    forecast = generate_forecast(target_date)
    print(forecast)
    return 0


if __name__ == "__main__":
    sys.exit(main())
