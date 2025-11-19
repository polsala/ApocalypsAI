"""emoji_forecast/src/forecast.py

Utility that returns a deterministic emoji representing the "weather" for a given date.

The algorithm is deliberately simple and offline‑only:
    1. Convert the date (ISO‑8601 string) to a sum of Unicode code points.
    2. Modulo the sum by the number of available emojis.
    3. Return the emoji at that index.

This guarantees the same output for the same input without any external services.
"""

from __future__ import annotations

import datetime
from typing import List

# A short, whimsical list of weather‑related emojis.
EMOJIS: List[str] = [
    "☀️",  # sunny
    "🌤️",  # sun behind small cloud
    "⛅",   # sun behind cloud
    "🌥️",  # sun behind large cloud
    "☁️",  # cloud
    "🌦️",  # sun behind rain cloud
    "🌧️",  # cloud with rain
    "⛈️",  # cloud with lightning and rain
    "🌩️",  # lightning
    "🌨️",  # cloud with snow
    "❄️",   # snowflake
    "🌈",  # rainbow
    "🌪️",  # tornado
    "🌫️",  # fog
]


def _date_to_string(date: datetime.date | None = None) -> str:
    """Return an ISO‑8601 date string (YYYY‑MM‑DD).

    If *date* is ``None`` the current UTC date is used.
    """
    if date is None:
        date = datetime.date.today()
    return date.isoformat()


def _deterministic_index(date_str: str) -> int:
    """Compute a deterministic index into ``EMOJIS`` based on *date_str*.

    The algorithm sums the Unicode code point of each character and takes the
    modulo of the length of ``EMOJIS``. This is fully deterministic and requires
    no randomness or external state.
    """
    total = sum(ord(ch) for ch in date_str)
    return total % len(EMOJIS)


def get_daily_emoji_forecast(date: str | datetime.date | None = None) -> str:
    """Return the emoji forecast for *date*.

    Parameters
    ----------
    date:
        - ``None`` – use today's date.
        - ``datetime.date`` – a specific date.
        - ``str`` – an ISO‑8601 formatted date (``YYYY‑MM‑DD``).

    Returns
    -------
    str
        The selected emoji.
    """
    if isinstance(date, datetime.date):
        date_str = _date_to_string(date)
    elif isinstance(date, str):
        # Assume the caller passed a correctly formatted ISO‑8601 string.
        date_str = date
    else:
        date_str = _date_to_string()

    idx = _deterministic_index(date_str)
    return EMOJIS[idx]


def main() -> None:
    """CLI entry‑point – prints today's emoji forecast to stdout."""
    forecast = get_daily_emoji_forecast()
    print(f"Today's forecast: {forecast}")


if __name__ == "__main__":
    main()
