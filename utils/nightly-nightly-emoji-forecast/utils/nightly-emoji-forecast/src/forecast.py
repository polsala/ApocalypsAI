"""forecast.py

Provides a deterministic emoji "weather" forecast based on a given date.

The algorithm is deliberately simple and offline:
    1. Compute the day of year (1‑365/366).
    2. Take the remainder modulo the number of emojis.
    3. Return the emoji at that index.

The module can be used as a library or executed as a CLI to print today's forecast.
"""

from __future__ import annotations

import datetime
import sys
from typing import List

# List of emojis – order matters for deterministic mapping
EMOJIS: List[str] = [
    "☀️",  # 0
    "🌤️",  # 1
    "⛅",   # 2
    "🌥️",  # 3
    "☁️",  # 4
    "🌦️",  # 5
    "🌧️",  # 6
    "⛈️",  # 7
    "🌩️",  # 8
    "❄️",  # 9
    "🌨️",  #10
    "🌪️",  #11
]


def get_emoji_forecast(date: datetime.date) -> str:
    """Return the emoji forecast for *date*.

    The mapping is deterministic and does **not** depend on external data.
    """
    # ``timetuple().tm_yday`` gives 1‑based day of year
    day_of_year = date.timetuple().tm_yday
    index = day_of_year % len(EMOJIS)
    return EMOJIS[index]


def _cli() -> None:
    """CLI entry point – prints the forecast for today.

    Usage:
        python -m utils.nightly-emoji-forecast.src.forecast
    """
    today = datetime.date.today()
    forecast = get_emoji_forecast(today)
    print(f"{today.isoformat()}: {forecast}")


if __name__ == "__main__":
    # Allow optional date argument for quick manual testing
    if len(sys.argv) > 1:
        try:
            input_date = datetime.date.fromisoformat(sys.argv[1])
        except ValueError as exc:
            print(f"Invalid date format: {sys.argv[1]} (expected YYYY-MM-DD)", file=sys.stderr)
            sys.exit(1)
        print(f"{input_date.isoformat()}: {get_emoji_forecast(input_date)}")
    else:
        _cli()
