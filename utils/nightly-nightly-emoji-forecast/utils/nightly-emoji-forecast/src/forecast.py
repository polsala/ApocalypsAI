'''Emoji weather forecast utility.

Provides a deterministic emoji forecast based on a given date.
'''  # noqa: D400

import sys
import datetime
import hashlib
from typing import List

# A curated list of weather‑related emojis.
EMOJIS: List[str] = [
    "☀️",  # sunny
    "🌤️",  # sun behind small cloud
    "⛅",   # sun behind cloud
    "🌥️",  # sun behind large cloud
    "☁️",  # cloudy
    "🌦️",  # sun behind rain cloud
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌨️",  # snow
    "❄️",   # snowflake
    "🌪️",  # tornado
    "🌈",   # rainbow
]


def _hash_date(date: datetime.date) -> int:
    """Return a deterministic integer hash for *date*.

    The ISO‑format string is hashed with SHA‑256 and the hex digest is
    interpreted as a base‑16 integer.
    """
    h = hashlib.sha256(date.isoformat().encode()).hexdigest()
    return int(h, 16)


def get_emoji_forecast(date: datetime.date) -> str:
    """Return a single emoji representing the forecast for *date*.

    The selection is deterministic: the same *date* always yields the same
    emoji, and no external resources are required.
    """
    idx = _hash_date(date) % len(EMOJIS)
    return EMOJIS[idx]


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Expected usage: ``python -m forecast <YYYY-MM-DD>``.
    Returns ``0`` on success, ``1`` on error.
    """
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python -m forecast <YYYY-MM-DD>", file=sys.stderr)
        return 1
    try:
        target = datetime.date.fromisoformat(argv[0])
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
        return 1
    print(get_emoji_forecast(target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
