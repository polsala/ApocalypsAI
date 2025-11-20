"""Emoji weather forecast utility.

Provides a deterministic, whimsical weather forecast expressed in emojis.
"""

import sys
import argparse
import datetime
import random
from typing import List

EMOJIS: List[str] = [
    "☀️",   # sunny
    "🌤️",  # mostly sunny
    "🌥️",  # partly cloudy
    "🌦️",  # rain showers
    "🌧️",  # heavy rain
    "⛈️",   # thunderstorm
    "🌩️",   # lightning
    "🌨️",  # snow
    "❄️",   # snowflake
    "🌪️",  # tornado
    "🌈",   # rainbow
]

DESCRIPTIONS = {
    "☀️": "Sunny",
    "🌤️": "Partly sunny",
    "🌥️": "Partly cloudy",
    "🌦️": "Rain showers",
    "🌧️": "Heavy rain",
    "⛈️": "Thunderstorm",
    "🌩️": "Lightning",
    "🌨️": "Snow",
    "❄️": "Snowflake",
    "🌪️": "Tornado",
    "🌈": "Rainbow",
}

def get_forecast(date: datetime.date) -> str:
    """Return an emoji forecast string for the given date.

    The selection is deterministic: the same date always yields the same emoji.
    """
    # Seed random with the date's ordinal to get reproducible choice
    random.seed(date.toordinal())
    emoji = random.choice(EMOJIS)
    description = DESCRIPTIONS.get(emoji, "Mystery")
    return f"{emoji}  {description}"

def parse_args(argv: List[str] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a whimsical emoji weather forecast."
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date for the forecast in YYYY-MM-DD format (default: today).",
    )
    return parser.parse_args(argv)

def main() -> None:
    args = parse_args()
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            print(f"Invalid date format: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = datetime.date.today()
    forecast = get_forecast(target_date)
    print(forecast)

if __name__ == "__main__":
    main()
