"""
emoji_forecast utility.
Generates a deterministic emoji weather forecast for a date range.
"""

import datetime
import random
from typing import List

# Mapping of weather conditions to emojis
_WEATHER_EMOJIS = [
    "☀️",
    "🌤️",
    "⛅",
    "🌥️",
    "☁️",
    "🌦️",
    "🌧️",
    "⛈️",
    "🌩️",
    "❄️",
    "🌨️",
    "🌪️",
]


def _seed_random(start: str, end: str) -> None:
    """Seed the random generator based on the date range for deterministic output.

    Parameters
    ----------
    start: str
        ISO‑format start date (YYYY‑MM‑DD).
    end: str
        ISO‑format end date (YYYY‑MM‑DD).
    """
    seed_str = f"{start}:{end}"
    random.seed(seed_str)


def _date_range(start: str, end: str) -> List[datetime.date]:
    """Return a list of dates inclusive between *start* and *end*.

    Raises
    ------
    ValueError
        If *start* is after *end*.
    """
    start_dt = datetime.date.fromisoformat(start)
    end_dt = datetime.date.fromisoformat(end)
    if start_dt > end_dt:
        raise ValueError("start date must be before or equal to end date")
    delta = (end_dt - start_dt).days
    return [start_dt + datetime.timedelta(days=i) for i in range(delta + 1)]


def generate_forecast(start_date: str, end_date: str) -> List[str]:
    """Generate a list of emoji strings, one per day in the range.

    Parameters
    ----------
    start_date: str
        ISO‑format start date (inclusive).
    end_date: str
        ISO‑format end date (inclusive).

    Returns
    -------
    List[str]
        Emoji representing the weather for each day.
    """
    _seed_random(start_date, end_date)
    dates = _date_range(start_date, end_date)
    return [random.choice(_WEATHER_EMOJIS) for _ in dates]


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python -m src.forecast <start_date> <end_date>")
        sys.exit(1)
    start, end = sys.argv[1], sys.argv[2]
    for day, emoji in zip(_date_range(start, end), generate_forecast(start, end)):
        print(f"{day.isoformat()}: {emoji}")
