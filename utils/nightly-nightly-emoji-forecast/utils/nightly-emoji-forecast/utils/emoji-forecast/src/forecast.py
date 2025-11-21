#!/usr/bin/env python3
"""
emoji_forecast: Generate a whimsical emoji weather forecast based on the current date.
"""

from __future__ import annotations

import datetime
import sys
from typing import List

EMOJI_SEQUENCE: List[str] = [
    "☀️",
    "🌤️",
    "⛅",
    "🌥️",
    "☁️",
    "🌦️",
    "🌧️",
    "⛈️",
    "🌩️",
    "🌨️",
    "❄️",
    "🌪️",
]


def get_forecast_for_date(date: datetime.date) -> str:
    """Deterministically generate an emoji forecast string for the given date.

    The day of the year (1‑366) is used to select three consecutive emojis
    from EMOJI_SEQUENCE, wrapping around the list as needed.

    Args:
        date: The date for which to generate the forecast.

    Returns:
        A string of three emojis representing the forecast.
    """
    day_index = (date.timetuple().tm_yday - 1) % len(EMOJI_SEQUENCE)
    forecast = [
        EMOJI_SEQUENCE[(day_index + i) % len(EMOJI_SEQUENCE)]
        for i in range(3)
    ]
    return "".join(forecast)


def main() -> None:
    today = datetime.date.today()
    forecast = get_forecast_for_date(today)
    print(forecast)


if __name__ == "__main__":
    main()
