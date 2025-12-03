"""forecast.py

Provides a deterministic, emoji‑based weather forecast for a date range.

The algorithm:
1. Parse the ISO‑format start and end dates.
2. Seed ``random`` with the *start* date string – this guarantees repeatability.
3. For each day in the inclusive range, pick an emoji from a fixed list.
4. Return a list of ``"YYYY‑MM‑DD: <emoji>"`` strings.

No external network calls are performed; the utility is fully offline.
"""

from __future__ import annotations

import random
from datetime import date, timedelta
from typing import List

_WEATHER_EMOJIS: List[str] = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌩️",  # lightning
    "🌨️",  # snow
    "🌪️",  # tornado
    "🌈",  # rainbow
    "❄️",  # snowflake
    "🌫️",  # fog
]


def _date_range(start: date, end: date) -> List[date]:
    """Return a list of dates from *start* to *end* inclusive.

    # Mock rationale: simple loop, no external libs needed.
    """
    days = (end - start).days
    return [start + timedelta(days=i) for i in range(days + 1)]


def generate_forecast(start_date: str, end_date: str) -> List[str]:
    """Generate a deterministic emoji forecast.

    Parameters
    ----------
    start_date: str
        ISO‑format date string (e.g., ``"2023-09-01"``).
    end_date: str
        ISO‑format date string; must be >= ``start_date``.

    Returns
    -------
    List[str]
        List of ``"YYYY‑MM‑DD: <emoji>"`` strings.
    """
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    if end < start:
        raise ValueError("end_date must be on or after start_date")

    # Seed with the start date string for deterministic output.
    random.seed(start_date)

    forecast_lines: List[str] = []
    for current in _date_range(start, end):
        emoji = random.choice(_WEATHER_EMOJIS)
        forecast_lines.append(f"{current.isoformat()}: {emoji}")
    return forecast_lines


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate an emoji weather forecast for a date range.")
    parser.add_argument("start", help="Start date (ISO format, e.g., 2023-09-01)")
    parser.add_argument("end", help="End date (ISO format, e.g., 2023-09-05)")
    args = parser.parse_args()
    for line in generate_forecast(args.start, args.end):
        print(line)
