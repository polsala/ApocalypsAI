#!/usr/bin/env python3
"""
emoji forecast utility
"""

import hashlib
import sys
from typing import Dict

WEATHER_EMOJIS: Dict[int, str] = {
    0: "☀️",  # sunny
    1: "⛅",  # partly cloudy
    2: "☁️",  # cloudy
    3: "🌧️",  # rain
    4: "⛈️",  # thunderstorm
    5: "❄️",  # snow
    6: "🌫️",  # fog
}


def location_to_emoji(location: str) -> str:
    """Deterministically map a location string to a weather emoji.

    The function hashes the location with SHA‑256, interprets the hex digest as an integer,
    and uses modulo arithmetic to select an emoji from ``WEATHER_EMOJIS``.
    """
    h = hashlib.sha256(location.encode("utf-8")).hexdigest()
    idx = int(h, 16) % len(WEATHER_EMOJIS)
    return WEATHER_EMOJIS[idx]


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: forecast.py <location>")
        sys.exit(1)
    location = " ".join(argv)
    emoji = location_to_emoji(location)
    print(f"Weather forecast for {location}: {emoji}")


if __name__ == "__main__":
    main()
