"""emoji_forecast – deterministic emoji weather generator.

Provides:
- ``get_emoji_forecast(date: datetime.date) -> str`` – core library function.
- ``main()`` – CLI entry point.
"""

from __future__ import annotations

import argparse
import datetime
import sys
from typing import List

# Fixed list of weather emojis (ordered for deterministic indexing)
EMOJI_WEATHER: List[str] = [
    "☀️",   # sunny
    "🌤️",   # sun behind small cloud
    "🌥️",   # sun behind large cloud
    "🌦️",   # sun behind rain cloud
    "🌧️",   # cloud with rain
    "⛈️",   # cloud with lightning and rain
    "🌩️",   # cloud with lightning
    "🌨️",   # cloud with snow
    "❄️",   # snowflake
    "🌪️",   # tornado
]


def _deterministic_index(date_str: str) -> int:
    """Return a deterministic index in ``EMOJI_WEATHER`` for *date_str*.

    The algorithm is deliberately simple and offline:
    1. Sum the Unicode code points of the characters in *date_str*.
    2. Take the modulus with the length of ``EMOJI_WEATHER``.

    This yields a reproducible mapping without any external hashing libraries.
    """
    total = sum(ord(ch) for ch in date_str)
    return total % len(EMOJI_WEATHER)


def get_emoji_forecast(date: datetime.date) -> str:
    """Return a single emoji representing the *weather* for *date*.

    The function is pure – given the same ``date`` it always returns the same emoji.
    """
    date_str = date.isoformat()
    idx = _deterministic_index(date_str)
    return EMOJI_WEATHER[idx]


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic emoji weather forecast")
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Date in YYYY-MM-DD format (defaults to today)",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    if args.date:
        try:
            target_date = datetime.date.fromisoformat(args.date)
        except ValueError as exc:
            print(f"Invalid date format: {args.date}", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = datetime.date.today()

    forecast = get_emoji_forecast(target_date)
    print(f"Forecast for {target_date.isoformat()}: {forecast}")


if __name__ == "__main__":
    main()
