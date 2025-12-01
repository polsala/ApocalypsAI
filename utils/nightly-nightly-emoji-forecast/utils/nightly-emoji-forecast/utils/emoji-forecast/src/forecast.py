'''Emoji Forecast utility.'''

from __future__ import annotations
import sys
import datetime
from typing import List

_EMOJIS: List[str] = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "⛅",   # cloudy
    "🌥️",  # mostly cloudy
    "☁️",  # overcast
    "🌦️",  # rain sun
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌨️",  # snow
    "❄️",  # snowflake
    "🌪️",  # tornado
    "🌈",  # rainbow
]


def get_emoji_for_date(date: datetime.date) -> str:
    """Return deterministic emoji for the given date.

    The calculation is based on the number of days since the Unix epoch (1970‑01‑01).
    """
    days = (date - datetime.date(1970, 1, 1)).days
    index = days % len(_EMOJIS)
    return _EMOJIS[index]


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    * No arguments – prints today's emoji.
    * One argument – ISO date (YYYY‑MM‑DD) to forecast.
    """
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        today = datetime.date.today()
        print(get_emoji_for_date(today))
        return 0
    try:
        target = datetime.date.fromisoformat(argv[0])
    except ValueError:
        print(f"Invalid date format: {argv[0]}. Expected YYYY-MM-DD.", file=sys.stderr)
        return 1
    print(get_emoji_for_date(target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
