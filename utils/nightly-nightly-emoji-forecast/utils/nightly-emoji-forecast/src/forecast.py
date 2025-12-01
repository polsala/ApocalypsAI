#!/usr/bin/env python3
"""emoji forecast utility

Provides a deterministic three‑emoji forecast for any date.
"""

import sys
import datetime
import hashlib

# List of emojis representing whimsical weather conditions
EMOJIS = [
    "☀️",  # sunny
    "🌤️",  # sun behind small cloud
    "⛅",   # sun behind cloud
    "🌥️",  # sun behind large cloud
    "☁️",  # cloudy
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌩️",  # lightning
    "❄️",  # snow
    "🌪️",  # tornado
    "🌈",  # rainbow
    "🌫️",  # fog
]


def _seed_from_date(date_str: str) -> int:
    """Create an integer seed from a date string (YYYY‑MM‑DD).

    # Mock rationale: deterministic hashing, no external randomness.
    """
    # MD5 provides a stable 128‑bit hash; we interpret it as an integer.
    return int(hashlib.md5(date_str.encode()).hexdigest(), 16)


def get_forecast(date: datetime.date) -> str:
    """Return a three‑emoji forecast for the given date.

    The same date always yields the same forecast.
    """
    seed = _seed_from_date(date.isoformat())
    # Derive three 4‑bit indices from the seed (bits 0‑3, 4‑7, 8‑11)
    indices = [(seed >> (i * 4)) & 0xF for i in range(3)]
    return "".join(EMOJIS[idx % len(EMOJIS)] for idx in indices)


def main() -> None:
    """CLI entry point: prints forecast for today or a supplied YYYY‑MM‑DD date."""
    if len(sys.argv) > 1:
        try:
            date = datetime.date.fromisoformat(sys.argv[1])
        except ValueError:
            print("Invalid date format, use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
    else:
        date = datetime.date.today()
    print(get_forecast(date))


if __name__ == "__main__":
    main()
