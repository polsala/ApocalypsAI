"""nightly_emoji_forecast – deterministic emoji mapping for dates.

Provides a simple CLI and a library function `get_emoji_for_date`.
"""

import argparse
import hashlib
from datetime import datetime
from typing import List

# A curated list of emojis representing a whimsical "forecast".
EMOJI_PALETTE: List[str] = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "⛅",   # cloudy
    "🌥️",  # overcast
    "☁️",  # cloudy
    "🌦️",  # rain showers
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌨️",  # snow
    "❄️",   # snowflake
    "🌪️",  # tornado
    "🌈",  # rainbow
    "🌙",  # night
    "⭐",   # starry
    "🎄",  # festive
    "🪐",  # cosmic
    "🦄",  # magical
    "🤖",  # robotic
    "💥",  # explosive
    "🪁",  # kite
]

def _hash_date(date_str: str) -> int:
    """Return a deterministic integer hash for *date_str*.

    The function uses SHA‑256 to avoid collisions and to produce a uniform
    distribution across the emoji palette.
    """
    # Ensure the string is normalized (ISO format) – callers should validate.
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    return int(digest, 16)

def get_emoji_for_date(date_str: str) -> str:
    """Return an emoji representing the *date_str*.

    Parameters
    ----------
    date_str: str
        Date in ISO format ``YYYY-MM-DD``.

    Returns
    -------
    str
        An emoji from ``EMOJI_PALETTE``.
    """
    # Basic validation – raise ValueError for malformed dates.
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"Invalid date format: {date_str!r}. Expected YYYY-MM-DD.") from exc

    hash_int = _hash_date(date_str)
    index = hash_int % len(EMOJI_PALETTE)
    return EMOJI_PALETTE[index]

def _cli() -> None:
    parser = argparse.ArgumentParser(description="Deterministic emoji forecast for a given date.")
    parser.add_argument("date", help="Date in ISO format (YYYY-MM-DD)")
    args = parser.parse_args()
    try:
        emoji = get_emoji_for_date(args.date)
        print(emoji)
    except ValueError as e:
        parser.error(str(e))

if __name__ == "__main__":
    _cli()
