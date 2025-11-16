"""
emoji_forecast utility.

Provides a deterministic emoji based on the current date.
"""

from __future__ import annotations
import datetime
from typing import List

_EMOJIS: List[str] = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "⛅",   # cloudy
    "🌥️",  # mostly cloudy
    "☁️",  # overcast
    "🌦️",  # light rain
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌨️",  # snow
    "❄️",   # snowflake
    "🌪️",  # tornado
    "🌈",   # rainbow
]


def get_daily_emoji(date: datetime.date | None = None) -> str:
    """Return an emoji representing the "weather" for the given date.

    If no date is supplied, uses today's date.
    The selection is deterministic: day_of_year % len(_EMOJIS).
    """
    if date is None:
        date = datetime.date.today()
    index = (date.timetuple().tm_yday - 1) % len(_EMOJIS)
    return _EMOJIS[index]


def main() -> None:
    """CLI entry point."""
    print(get_daily_emoji())


if __name__ == "__main__":
    main()
