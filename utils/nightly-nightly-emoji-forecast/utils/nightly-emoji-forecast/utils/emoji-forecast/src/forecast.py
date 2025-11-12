#!/usr/bin/env python3
"""emoji-forecast – deterministic emoji weather generator.

The forecast is derived from the ISO‑format date string (YYYY‑MM‑DD).
A SHA‑256 hash of the date is taken, converted to an integer, and then
used to pick emojis from a predefined palette. The result is a short
string of 1‑3 emojis that is *always* the same for a given date.
"""

import hashlib
import datetime
from typing import List

# 🎨 Emoji palette – ordered by typical weather symbolism.
EMOJI_PALETTE: List[str] = [
    "☀️",   # sunny
    "🌤️",   # partly sunny
    "⛅",    # partly cloudy
    "🌥️",   # mostly cloudy
    "☁️",   # cloudy
    "🌦️",   # rain showers
    "🌧️",   # heavy rain
    "⛈️",   # thunderstorm
    "🌨️",   # snow
    "❄️",   # snowflake
    "🌈",   # rainbow (good vibes)
    "🌪️",   # tornado (just for fun)
]


def _hash_date(date: datetime.date) -> int:
    """Return a deterministic integer hash for *date*.

    The hash is based on the SHA‑256 of the ISO‑format string, ensuring
    the same result across Python versions and platforms.
    """
    iso = date.isoformat().encode("utf-8")
    digest = hashlib.sha256(iso).hexdigest()
    return int(digest, 16)


def generate_forecast(date: datetime.date | None = None) -> str:
    """Generate a deterministic emoji forecast for *date*.

    If *date* is ``None`` the current local date is used.
    The function returns a space‑separated string of 1‑3 emojis.
    """
    if date is None:
        date = datetime.date.today()
    # Derive a reproducible integer from the date.
    seed = _hash_date(date)
    # Choose how many emojis (1‑3) – deterministic via modulo.
    count = (seed % 3) + 1
    emojis: List[str] = []
    palette_len = len(EMOJI_PALETTE)
    for i in range(count):
        # Pick an emoji index using the seed and the loop counter.
        idx = (seed // (palette_len ** i)) % palette_len
        emojis.append(EMOJI_PALETTE[idx])
    return " ".join(emojis)


def main() -> None:
    """CLI entry point – prints the forecast for today."""
    forecast = generate_forecast()
    print(forecast)


if __name__ == "__main__":
    main()
