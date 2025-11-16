"""emoji forecast utility

Provides a deterministic emoji "weather" forecast based on the calendar date.

The algorithm is deliberately simple and offline:
- A static list of ten emojis representing various weather moods.
- The index is derived from the date's ordinal value, ensuring the same
  result for the same date across any environment.
"""

from __future__ import annotations

import datetime
import sys
from typing import Optional

_EMOJIS = [
    "☀️",  # sunny
    "🌧️",  # rain
    "⛅",   # partly cloudy
    "🌩️",  # thunderstorm
    "❄️",  # snow
    "🌪️",  # tornado
    "🌈",  # rainbow
    "☁️",  # cloudy
    "🌤️",  # sun behind small cloud
    "🌦️",  # sun behind rain cloud
]


def _emoji_index_for(date: datetime.date) -> int:
    """Return a deterministic index into ``_EMOJIS`` for *date*.

    The calculation is deliberately straightforward: ``(ordinal + 7) % len(_EMOJIS)``.
    Adding a small constant (7) avoids a trivial ``ordinal % len`` pattern and
    provides a bit more visual variety.
    """
    return (date.toordinal() + 7) % len(_EMOJIS)


def get_emoji_forecast(date: Optional[datetime.date] = None) -> str:
    """Return the emoji forecast for *date* (or today if ``None``)."""
    if date is None:
        date = datetime.date.today()
    idx = _emoji_index_for(date)
    return _EMOJIS[idx]


def _parse_cli_arg(arg: str) -> datetime.date:
    """Parse a ``YYYY-MM-DD`` string into a ``datetime.date``.

    Raises ``ValueError`` on malformed input.
    """
    return datetime.datetime.strptime(arg, "%Y-%m-%d").date()


def main(argv: list[str] | None = None) -> None:
    """CLI entry point.

    ``python -m src.forecast`` prints today's forecast.
    ``python -m src.forecast 2025-12-31`` prints the forecast for the supplied date.
    """
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) > 1:
        print("Usage: python -m src.forecast [YYYY-MM-DD]", file=sys.stderr)
        sys.exit(1)
    date = _parse_cli_arg(argv[0]) if argv else None
    print(get_emoji_forecast(date))


if __name__ == "__main__":
    main()
