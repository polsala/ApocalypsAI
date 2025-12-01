"""emoji_forecast – deterministic emoji weather forecast.

Provides a single public function :func:`forecast` and a tiny CLI.
"""

import sys
import hashlib
from datetime import datetime
from typing import Literal

# Mapping index -> emoji
_EMOJIS = [
    "🌞",  # sunny
    "🌤️",  # partly sunny
    "🌥️",  # cloudy
    "🌧️",  # rainy
    "❄️",   # snowy
]

def _hash_date(date_str: str) -> int:
    """Return a stable integer hash for *date_str*.

    Uses SHA‑256 to guarantee deterministic results across Python versions.
    """
    h = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    return int(h, 16)

def forecast(date: str | datetime) -> Literal["🌞", "🌤️", "🌥️", "🌧️", "❄️"]:
    """Return an emoji representing the weather for *date*.

    Parameters
    ----------
    date: str or datetime
        ISO‑format date string (``YYYY-MM-DD``) or a ``datetime`` object.

    Returns
    -------
    str
        One of the five weather emojis.
    """
    if isinstance(date, datetime):
        date_str = date.date().isoformat()
    else:
        date_str = date
    # Validate format (basic)
    try:
        datetime.fromisoformat(date_str)
    except ValueError as exc:
        raise ValueError(f"Invalid date format: {date_str!r}. Expected YYYY-MM-DD") from exc
    idx = _hash_date(date_str) % len(_EMOJIS)
    return _EMOJIS[idx]

def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m forecast <YYYY-MM-DD>")
        sys.exit(1)
    try:
        emoji = forecast(sys.argv[1])
        print(emoji)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    _cli()
