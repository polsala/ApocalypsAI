#!/usr/bin/env python3
"""
emoji_forecast: generate a deterministic emoji weather forecast for a city.

The forecast is based on a simple hash of the city name to select
sun, cloud, rain, thunder, snow emojis.
"""

import argparse
import hashlib
from typing import List

EMOJI_SETS = [
    "☀️",   # sunny
    "⛅",   # partly cloudy
    "☁️",   # cloudy
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "❄️",   # snow
    "🌪️",  # tornado
]


def _hash_city(city: str) -> int:
    """Return an integer hash of the city name."""
    return int(hashlib.sha256(city.lower().encode()).hexdigest(), 16)


def generate_forecast(city: str, days: int = 3) -> List[str]:
    """Generate a list of emoji forecasts for the next `days` days.

    The selection rotates through ``EMOJI_SETS`` based on the hash of ``city``.
    """
    base = _hash_city(city)
    forecasts: List[str] = []
    for i in range(days):
        idx = (base + i) % len(EMOJI_SETS)
        forecasts.append(EMOJI_SETS[idx])
    return forecasts


def main() -> None:
    parser = argparse.ArgumentParser(description="Emoji weather forecast")
    parser.add_argument("city", nargs="?", default="Nowhere", help="City name")
    parser.add_argument("-d", "--days", type=int, default=3, help="Number of days")
    args = parser.parse_args()
    forecast = generate_forecast(args.city, args.days)
    print(f"Forecast for {args.city}: {' '.join(forecast)}")


if __name__ == "__main__":
    main()
