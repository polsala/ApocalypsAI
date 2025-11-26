"""
emoji_forecast utility
Provides deterministic emoji weather forecasts based on a date string.
"""

import hashlib
from datetime import datetime
from typing import List

# Define possible weather emojis
WEATHER_EMOJIS = ["☀️", "🌤️", "⛅️", "🌥️", "☁️", "🌧️", "⛈️", "🌩️", "🌨️", "❄️", "🌈", "☔️"]


def _hash_date(date_str: str) -> int:
    """Create a stable integer hash from a date string.
    
    Mock rationale: using SHA256 ensures deterministic output without external randomness.
    """
    return int(hashlib.sha256(date_str.encode()).hexdigest(), 16)


def get_emoji_forecast(date_str: str) -> str:
    """Return a deterministic sequence of 3 weather emojis for the given ISO date string.

    Parameters
    ----------
    date_str: str
        Date in ISO format (YYYY-MM-DD).

    Returns
    -------
    str
        Concatenated emojis representing the forecast.
    """
    # Validate date format
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("date_str must be in YYYY-MM-DD format") from exc

    seed = _hash_date(date_str)
    emojis: List[str] = []
    for i in range(3):
        idx = (seed >> (i * 8)) % len(WEATHER_EMOJIS)
        emojis.append(WEATHER_EMOJIS[idx])
    return "".join(emojis)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m src.forecast <YYYY-MM-DD>")
        sys.exit(1)
    print(get_emoji_forecast(sys.argv[1]))
