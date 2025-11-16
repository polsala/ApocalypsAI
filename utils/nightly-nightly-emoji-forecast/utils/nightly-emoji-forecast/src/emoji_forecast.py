"""Emoji Weather Forecast utility.

Generates a deterministic sequence of weather emojis for a given date.
"""

import sys
import datetime
import random
from typing import List

WEATHER_EMOJIS = [
    "☀️",
    "🌤️",
    "⛅",
    "🌥️",
    "☁️",
    "🌦️",
    "🌧️",
    "⛈️",
    "🌩️",
    "🌨️",
    "❄️",
    "🌈",
    "🌪️",
]


def _seed_for_date(date: datetime.date) -> int:
    """Create an integer seed from a date.

    Mock rationale: deterministic seed ensures offline test reproducibility.
    """
    # Use ISO format without dashes, e.g., 20251116 -> int
    return int(date.isoformat().replace("-", ""))


def get_forecast(date: datetime.date, count: int = 3) -> List[str]:
    """Return a list of `count` weather emojis for `date`.

    The selection is deterministic based on the date.
    """
    rnd = random.Random(_seed_for_date(date))
    return [rnd.choice(WEATHER_EMOJIS) for _ in range(count)]


def format_forecast(emojis: List[str]) -> str:
    """Join emojis into a human‑readable string."""
    return " ".join(emojis)


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Usage: python -m utils.nightly-emoji-forecast.src.emoji_forecast [YYYY-MM-DD]

    Returns exit code 0 on success, 1 on error.
    """
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Error: date argument required (YYYY-MM-DD)", file=sys.stderr)
        return 1

    try:
        date = datetime.date.fromisoformat(argv[0])
    except ValueError:
        print(f"Error: invalid date format '{argv[0]}'", file=sys.stderr)
        return 1

    emojis = get_forecast(date)
    print(format_forecast(emojis))
    return 0


if __name__ == "__main__":
    sys.exit(main())
