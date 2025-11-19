"""emoji_forecast
===================

Provides a deterministic emoji‑based weather forecast for a given ``datetime.date``.

The implementation is deliberately lightweight: it uses only the Python standard
library and a fixed list of emojis. The forecast is derived from the day‑of‑year
modulo the number of available emojis, guaranteeing the same output for the
same input date.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from typing import List

# A curated, whimsical list of weather emojis.
_WEATHER_EMOJIS: List[str] = [
    "☀️",   # Sunny
    "🌤️",   # Mostly sunny
    "⛅",    # Partly cloudy
    "🌥️",   # Mostly cloudy
    "☁️",   # Overcast
    "🌧️",   # Light rain
    "⛈️",   # Thunderstorm
    "🌩️",   # Lightning
    "❄️",   # Snow
    "🌪️",   # Tornado
]


def get_emoji_forecast(target_date: date) -> str:
    """Return an emoji representing the weather for *target_date*.

    The algorithm is deterministic and offline:

    1. Compute the day of year (1‑366).
    2. Take ``day_of_year % len(_WEATHER_EMOJIS)``.
    3. Return the emoji at that index.

    Parameters
    ----------
    target_date: datetime.date
        The date for which to generate the forecast.

    Returns
    -------
    str
        A single emoji string.
    """
    day_of_year = target_date.timetuple().tm_yday
    index = day_of_year % len(_WEATHER_EMOJIS)
    return _WEATHER_EMOJIS[index]


def _parse_cli_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="nightly-emoji-forecast",
        description="Generate a deterministic emoji weather forecast for a given date.",
    )
    parser.add_argument(
        "date",
        type=str,
        help="Date in ISO format (YYYY-MM-DD).",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = _parse_cli_args(argv)
    try:
        # Allow both ISO date strings and full datetime strings.
        parsed = datetime.fromisoformat(args.date).date()
    except ValueError as exc:
        print(f"Error: '{args.date}' is not a valid ISO date.", file=sys.stderr)
        return 1

    forecast = get_emoji_forecast(parsed)
    print(f"{parsed.isoformat()}: {forecast}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
