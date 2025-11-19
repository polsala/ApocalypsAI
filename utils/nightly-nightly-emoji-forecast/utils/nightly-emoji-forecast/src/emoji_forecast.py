"""
emoji_forecast.py

Provides a deterministic emoji weather forecast based on a date string.
"""

import hashlib
import sys
from typing import List

WEATHER_EMOJIS: List[str] = [
    "☀️",   # Sunny
    "🌤️",   # Partly sunny
    "⛅",    # Partly cloudy
    "🌥️",   # Mostly cloudy
    "☁️",   # Cloudy
    "🌦️",   # Light rain
    "🌧️",   # Rain
    "⛈️",   # Thunderstorm
    "🌨️",   # Snow
    "❄️",   # Snowflake
    "🌪️",   # Tornado
    "🌈",   # Rainbow
]

def _hash_date(date_str: str) -> int:
    """Return a deterministic integer hash for the given date string."""
    return int(hashlib.sha256(date_str.encode("utf-8")).hexdigest(), 16)

def forecast(date_str: str) -> str:
    """
    Return an emoji representing the weather forecast for ``date_str``.

    The function is deterministic: the same ``date_str`` always yields the same emoji.
    """
    idx = _hash_date(date_str) % len(WEATHER_EMOJIS)
    return WEATHER_EMOJIS[idx]

def main(argv: List[str] | None = None) -> int:
    """CLI entry point."""
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python -m src.emoji_forecast <YYYY-MM-DD>", file=sys.stderr)
        return 1
    date_str = argv[0]
    print(forecast(date_str))
    return 0

if __name__ == "__main__":
    sys.exit(main())
