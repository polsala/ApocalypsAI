"""emoji_forecast.py

A tiny deterministic emoji‑weather generator.

Public API:
    get_forecast(date: datetime.date) -> str
        Returns a space‑separated string of 1‑3 emojis representing the "weather" for the given date.

CLI usage:
    python -m utils.nightly-emoji-forecast src/forecast.py [YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import datetime
import random
from typing import List

# A curated list of weather‑related emojis (feel free to extend).
EMOJIS: List[str] = [
    "☀️",  # sunny
    "🌤️",  # sun behind small cloud
    "⛅",   # sun behind cloud
    "🌥️",  # cloud with sun
    "☁️",  # cloudy
    "🌦️",  # sun behind rain cloud
    "🌧️",  # cloud with rain
    "⛈️",  # cloud with lightning
    "🌩️",  # lightning
    "🌨️",  # cloud with snow
    "❄️",   # snowflake
    "🌈",  # rainbow
    "🌪️",  # tornado
    "🌫️",  # fog
    "⚡",   # high voltage
]


def _seed_from_date(date: datetime.date) -> int:
    """Create an integer seed from a date.

    The format YYYYMMDD guarantees a unique, sortable integer.
    """
    return int(date.strftime("%Y%m%d"))


def get_forecast(date: datetime.date) -> str:
    """Return a deterministic emoji forecast for *date*.

    The function seeds a local ``random.Random`` instance with a value derived
    from the supplied date, then picks a random number of emojis (1‑3) from the
    ``EMOJIS`` list.
    """
    rng = random.Random(_seed_from_date(date))
    count = rng.randint(1, 3)
    chosen = [rng.choice(EMOJIS) for _ in range(count)]
    return " ".join(chosen)


def _parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a deterministic emoji weather forecast.")
    parser.add_argument(
        "date",
        nargs="?",
        default=None,
        help="Date in YYYY-MM-DD format. Defaults to today.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_cli()
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {args.date}. Use YYYY-MM-DD.") from exc
    else:
        target_date = datetime.date.today()
    forecast = get_forecast(target_date)
    print(forecast)


if __name__ == "__main__":
    main()
