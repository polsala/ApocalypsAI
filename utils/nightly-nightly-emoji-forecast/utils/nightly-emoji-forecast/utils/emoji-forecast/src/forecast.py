"""
emoji_forecast utility.

Provides a deterministic emoji weather forecast based on a date string.
"""

import hashlib
from typing import List

# List of weather emojis ordered from sunny to stormy
WEATHER_EMOJIS: List[str] = ["🌞", "🌤️", "⛅", "🌥️", "☁️", "🌦️", "🌧️", "⛈️", "🌩️", "❄️"]


def _hash_date(date_str: str) -> int:
    """Return an integer hash of the date string.

    # Mock rationale: using SHA256 to get a stable hash across runs.
    """
    return int(hashlib.sha256(date_str.encode()).hexdigest(), 16)


def get_emoji_forecast(date_str: str) -> str:
    """Return an emoji representing the weather forecast for the given ISO date string.

    Parameters
    ----------
    date_str: str
        Date in ISO format (YYYY-MM-DD).

    Returns
    -------
    str
        A single emoji.
    """
    # Mock rationale: deterministic selection via modulo.
    idx = _hash_date(date_str) % len(WEATHER_EMOJIS)
    return WEATHER_EMOJIS[idx]


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m emoji_forecast <YYYY-MM-DD>")
        sys.exit(1)
    print(get_emoji_forecast(sys.argv[1]))
