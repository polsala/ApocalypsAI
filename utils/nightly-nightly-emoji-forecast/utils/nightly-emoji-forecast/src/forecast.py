"""emoji forecast utility

Provides a deterministic, emoji‑only weather forecast for any given date.

Public API:
    - ``get_forecast(date: datetime.date) -> str``
    - ``main()`` – CLI entry point
"""

from __future__ import annotations

import argparse
import datetime
import sys
from typing import List

# A curated list of weather‑related emojis. The order is intentional – it will be
# cycled through based on the day‑of‑year.
EMOJI_PALETTE: List[str] = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "⛅",   # partly cloudy
    "🌥️",  # mostly cloudy
    "☁️",  # cloudy
    "🌦️",  # sun behind rain cloud
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌨️",  # snow
    "❄️",   # snowflake
    "🌪️",  # tornado
    "🌈",  # rainbow (good omen)
]


def _deterministic_index(date: datetime.date) -> int:
    """Return an index into ``EMOJI_PALETTE`` based on ``date``.

    The algorithm is deliberately simple and offline:
    1. Compute the day‑of‑year (1‑366).
    2. Modulo the length of the palette.
    """
    day_of_year = date.timetuple().tm_yday
    return (day_of_year - 1) % len(EMOJI_PALETTE)


def get_forecast(date: datetime.date) -> str:
    """Return the emoji forecast for ``date``.

    Parameters
    ----------
    date:
        The date for which to generate the forecast.

    Returns
    -------
    str
        A single emoji representing the forecast.
    """
    idx = _deterministic_index(date)
    return EMOJI_PALETTE[idx]


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="nightly-emoji-forecast",
        description="Print a whimsical emoji weather forecast for a given date.",
    )
    parser.add_argument(
        "date",
        nargs="?",
        default=None,
        help="Date in YYYY-MM-DD format. Defaults to today.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            print(f"Invalid date format: {args.date}. Expected YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = datetime.date.today()

    forecast = get_forecast(target_date)
    print(forecast)


if __name__ == "__main__":
    main()
