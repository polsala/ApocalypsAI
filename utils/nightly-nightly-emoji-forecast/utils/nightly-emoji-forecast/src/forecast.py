"""
emoji_forecast.py

Provides a deterministic emoji weather forecast based on a date string.
"""

import hashlib
import sys
from typing import List

_WEATHER_EMOJIS = {
    "sunny": "☀️",
    "cloudy": "☁️",
    "rainy": "🌧️",
    "stormy": "⛈️",
    "snowy": "❄️",
}

_WEATHER_ORDER: List[str] = list(_WEATHER_EMOJIS.keys())


def _hash_date(date_str: str) -> int:
    """Return an integer hash of the date string."""
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    return int(digest, 16)


def get_emoji_forecast(date_str: str) -> str:
    """
    Return an emoji representing the weather forecast for the given ISO‑8601 date.

    Parameters
    ----------
    date_str: str
        Date in ``YYYY-MM-DD`` format.

    Returns
    -------
    str
        Emoji string.
    """
    idx = _hash_date(date_str) % len(_WEATHER_ORDER)
    condition = _WEATHER_ORDER[idx]
    return _WEATHER_EMOJIS[condition]


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.forecast <YYYY-MM-DD>")
        sys.exit(1)
    date = sys.argv[1]
    print(get_emoji_forecast(date))


if __name__ == "__main__":
    main()
