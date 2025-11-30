"""
emoji-forecast utility
Provides a deterministic emoji weather forecast based on a date.
"""

import datetime
import hashlib


def _hash_date(date: datetime.date) -> int:
    """Return a deterministic integer hash for *date*.

    # Mock rationale: use SHA‑256 of the ISO‑formatted date string to obtain a stable, reproducible integer.
    """
    return int(hashlib.sha256(date.isoformat().encode()).hexdigest(), 16)


def get_forecast(date: datetime.date) -> str:
    """Return a whimsical emoji forecast string for the given *date*.

    The forecast is deterministic: the same date always yields the same result.
    """
    emojis = [
        "☀️",  # sunny
        "🌤️",  # sun behind small cloud
        "⛅",   # sun behind cloud
        "🌥️",  # sun behind large cloud
        "☁️",  # cloudy
        "🌦️",  # sun behind rain cloud
        "🌧️",  # rain
        "⛈️",  # thunderstorm
        "🌩️",  # lightning
        "🌨️",  # snow
        "❄️",   # snowflake
        "🌪️",  # tornado
    ]
    idx = _hash_date(date) % len(emojis)
    return emojis[idx]


def main() -> None:
    today = datetime.date.today()
    print(f"Today's emoji forecast: {get_forecast(today)}")


if __name__ == "__main__":
    main()
