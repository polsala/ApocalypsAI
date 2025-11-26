#!/usr/bin/env python3
"""
forecast.py – Generate a deterministic emoji weather forecast for a given date.

The module provides a simple public API:
    * ``get_daily_emoji_forecast(date: Optional[datetime.date]) -> str``
    * ``main()`` – CLI entry point that prints today's forecast.
"""

import datetime
import hashlib
from typing import Optional

# A small, whimsical palette of weather‑related emojis.
EMOJI_CHOICES = [
    "☀️",  # sunny
    "🌤️",  # sun behind small cloud
    "⛅",   # sun behind cloud
    "🌥️",  # sun behind large cloud
    "☁️",  # cloudy
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "❄️",  # snow
    "🌪️",  # tornado
    "🌈",  # rainbow
]


def _seed_from_date(date: datetime.date) -> int:
    """Create an integer seed from a date using SHA‑256.

    The deterministic hash guarantees the same output for the same input date.
    """
    date_str = date.isoformat()
    digest = hashlib.sha256(date_str.encode()).hexdigest()
    return int(digest, 16)


def get_daily_emoji_forecast(date: Optional[datetime.date] = None) -> str:
    """Return a single emoji representing the "weather" for *date*.

    If *date* is ``None`` the function uses ``datetime.date.today()``.
    """
    if date is None:
        date = datetime.date.today()
    seed = _seed_from_date(date)
    index = seed % len(EMOJI_CHOICES)
    return EMOJI_CHOICES[index]


def main() -> None:
    """CLI entry point – prints today's emoji forecast to stdout."""
    forecast = get_daily_emoji_forecast()
    print(f"Today's emoji forecast: {forecast}")


if __name__ == "__main__":
    main()
