"""
emoji forecast utility
"""

import sys
from datetime import date, datetime
from typing import List

# List of weather emojis ordered from clear to extreme
_WEATHER_EMOJIS: List[str] = [
    "☀️",   # sunny
    "🌤️",  # partly sunny
    "⛅",   # partly cloudy
    "🌥️",  # mostly cloudy
    "☁️",   # cloudy
    "🌦️",  # light rain
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "❄️",   # snow
    "🌪️",  # tornado
    "🌈",   # rainbow
    "🌫️",  # fog
]

def _seed_from_date(d: date) -> int:
    """Create a simple deterministic seed from a date.

    The seed is the sum of year, month, and day. This keeps the algorithm
    lightweight and fully offline.
    """
    return d.year + d.month + d.day

def get_forecast(d: date) -> str:
    """Return a three‑emoji forecast for the given date.

    The algorithm:
    1. Compute a deterministic integer seed from the date.
    2. Derive three indices using simple modular arithmetic.
    3. Map each index to an emoji (allowing repeats).
    """
    seed = _seed_from_date(d)
    n = len(_WEATHER_EMOJIS)
    idx1 = seed % n
    idx2 = (seed * 7) % n  # multiplier chosen arbitrarily for variety
    idx3 = (seed * 13) % n # another arbitrary multiplier
    return _WEATHER_EMOJIS[idx1] + _WEATHER_EMOJIS[idx2] + _WEATHER_EMOJIS[idx3]

def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Usage: forecast.py <YYYY-MM-DD>
    """
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: forecast.py <YYYY-MM-DD>", file=sys.stderr)
        return 1
    try:
        d = datetime.strptime(argv[0], "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
        return 1
    print(get_forecast(d))
    return 0

if __name__ == "__main__":
    sys.exit(main())
