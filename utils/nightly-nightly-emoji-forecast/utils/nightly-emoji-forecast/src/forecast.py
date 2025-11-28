"""Emoji weather forecast utility.

Provides a deterministic emoji forecast based on a given date.
"""

import sys
import datetime
from typing import List

# Fixed list of weather‑related emojis
EMOJIS: List[str] = [
    "☀️",  # sunny
    "🌤️",  # sun behind small cloud
    "⛅️",  # sun behind cloud
    "🌥️",  # sun behind large cloud
    "☁️",  # cloud
    "🌦️",  # sun behind rain cloud
    "🌧️",  # cloud with rain
    "☔️",  # umbrella with rain drops
    "⛈️",  # cloud with lightning
    "🌩️",  # high voltage sign
    "🌨️",  # cloud with snow
    "❄️",  # snowflake
    "🌪️",  # tornado
]


def _seed_from_date(date: datetime.date) -> int:
    """Create a reproducible integer seed from a date.

    The seed is simply the integer representation ``YYYYMMDD``.
    """
    return int(date.strftime("%Y%m%d"))


def get_forecast(date: datetime.date) -> str:
    """Return a three‑emoji forecast for *date*.

    The selection is deterministic: for each of the three positions we
    compute ``(seed + offset) % len(EMOJIS)`` and pick the emoji at that index.
    """
    seed = _seed_from_date(date)
    emojis = []
    for offset in range(3):
        idx = (seed + offset) % len(EMOJIS)
        emojis.append(EMOJIS[idx])
    return "".join(emojis)


def _parse_date(arg: str) -> datetime.date:
    """Parse a ``YYYY-MM-DD`` string into a :class:`datetime.date`.

    Raises ``ValueError`` if the format is invalid.
    """
    try:
        return datetime.datetime.strptime(arg, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("Date must be in YYYY-MM-DD format") from exc


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    * If a date argument is supplied, it must be ``YYYY-MM-DD``.
    * Without arguments the current local date is used.
    """
    argv = argv or sys.argv[1:]
    if not argv:
        target_date = datetime.date.today()
    else:
        target_date = _parse_date(argv[0])
    forecast = get_forecast(target_date)
    print(forecast)
    return 0


if __name__ == "__main__":
    sys.exit(main())
