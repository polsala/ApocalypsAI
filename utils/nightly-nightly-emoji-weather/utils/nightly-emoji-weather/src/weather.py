"""weather.py – deterministic emoji weather forecast

Provides a single public function:
    get_weather_emoji(date_str: str) -> str

The function accepts an ISO‑8601 date string (YYYY‑MM‑DD) and returns a weather‑related emoji.
"""

from __future__ import annotations

import datetime
from typing import List

# A short, whimsical list of weather emojis (length = 10)
_EMOJIS: List[str] = [
    "☀️",  # sunny
    "🌤️",  # mostly sunny
    "⛅",   # partly cloudy
    "🌥️",  # mostly cloudy
    "☁️",  # cloudy
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌩️",  # lightning
    "❄️",  # snow
    "🌪️",  # tornado
]


def _parse_date(date_str: str) -> datetime.date:
    """Parse an ISO‑8601 date string into a :class:`datetime.date`.

    Raises:
        ValueError: If the string is not a valid date.
    """
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception as exc:
        raise ValueError(f"Invalid date format '{date_str}'. Expected YYYY-MM-DD.") from exc


def get_weather_emoji(date_str: str) -> str:
    """Return a deterministic weather emoji for *date_str*.

    The algorithm is deliberately simple and offline:
    1. Parse the date.
    2. Compute ``date.toordinal() % len(_EMOJIS)``.
    3. Return the emoji at that index.

    Args:
        date_str: ISO‑8601 date string (e.g. ``"2023-10-31"``).

    Returns:
        A single emoji string.
    """
    date_obj = _parse_date(date_str)
    index = date_obj.toordinal() % len(_EMOJIS)
    return _EMOJIS[index]


def _cli() -> None:
    """Simple command‑line interface.

    Usage:
        python -m utils.nightly-emoji-weather.src.weather <date>
    """
    import argparse
    parser = argparse.ArgumentParser(description="Deterministic emoji weather forecast")
    parser.add_argument("date", help="Date in YYYY‑MM‑DD format (defaults to today)", nargs="?", default=datetime.date.today().isoformat())
    args = parser.parse_args()
    try:
        emoji = get_weather_emoji(args.date)
        print(emoji)
    except ValueError as e:
        print(f"Error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    _cli()
