"""Emoji Weather Forecast Utility.

Provides a deterministic, whimsical weather forecast based on the given date.
"""

from __future__ import annotations

import argparse
import datetime
from typing import List

# List of possible forecasts
FORECASTS: List[str] = [
    "☀️ Sunny",
    "🌧️ Rainy",
    "⛈️ Stormy",
    "❄️ Snowy",
    "🌈 Rainbow",
]

def get_forecast(date: datetime.date) -> str:
    """Return an emoji forecast for *date*.

    The forecast is deterministic: it uses the date's ordinal value modulo the
    number of available forecasts.
    """
    index = date.toordinal() % len(FORECASTS)
    return FORECASTS[index]

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deterministic emoji weather forecast."
    )
    parser.add_argument(
        "date",
        nargs="?",
        help="Date in YYYY-MM-DD format. Defaults to today.",
    )
    return parser.parse_args()

def main() -> None:
    args = _parse_args()
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {exc}") from exc
    else:
        target_date = datetime.date.today()
    forecast = get_forecast(target_date)
    print(forecast)

if __name__ == "__main__":
    main()
