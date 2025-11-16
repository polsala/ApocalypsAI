#!/usr/bin/env python3
"""
forecast.py

Generate a deterministic emoji weather forecast for a given date.
"""

import argparse
import datetime
import hashlib
import random
from typing import List

# 🎉 A curated list of weather‑related emojis.
EMOJI_MAP: List[str] = [
    "☀️",   # sunny
    "🌤️",  # partly sunny
    "⛅",    # cloudy
    "🌥️",  # overcast
    "🌦️",  # rain showers
    "🌧️",  # rain
    "⛈️",   # thunderstorm
    "🌨️",  # snow
    "🌪️",  # tornado (just for fun)
]


def _seed_from_date(date: datetime.date) -> int:
    """Create a reproducible integer seed from a date.

    The ISO‑format string of the date is hashed with SHA‑256 and the first
    eight hex characters are interpreted as a 32‑bit integer.
    """
    h = hashlib.sha256(date.isoformat().encode()).hexdigest()
    return int(h[:8], 16)


def generate_forecast(date: datetime.date) -> List[str]:
    """Return a list of three emojis representing the day's forecast.

    The selection is deterministic for a given ``date``.
    """
    seed = _seed_from_date(date)
    rng = random.Random(seed)
    # Choose three emojis (repeats are allowed for simplicity).
    return [rng.choice(EMOJI_MAP) for _ in range(3)]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emoji weather forecast")
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Date in YYYY-MM-DD (default: today)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    target_date = args.date or datetime.date.today()
    forecast = generate_forecast(target_date)
    print(" ".join(forecast))


if __name__ == "__main__":
    main()
