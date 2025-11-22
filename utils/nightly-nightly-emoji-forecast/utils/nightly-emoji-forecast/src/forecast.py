"""emoji_forecast
~~~~~~~~~~~~~~~~~~
Utility to generate a deterministic emoji forecast based on a date.
"""

import argparse
import datetime
from typing import List

# A curated list of emojis representing various moods / weather‑like conditions.
EMOJIS: List[str] = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "⛅",   # cloudy
    "🌥️",  # mostly cloudy
    "☁️",  # overcast
    "🌦️",  # light rain
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌨️",  # snow
    "❄️",   # snowflake
    "🌪️",  # tornado
    "🌈",  # rainbow
    "🌙",  # night
    "⭐",   # stars
    "⚡",   # lightning
    "💧",  # droplets
    "🔥",  # fire
    "🌊",  # wave
    "🍀",  # luck
    "🪐",  # space
]

def get_emoji_forecast(target_date: datetime.date) -> str:
    """Return an emoji forecast for *target_date*.

    The forecast is deterministic: we compute the day‑of‑year, take it modulo the
    number of emojis, and return the corresponding emoji.
    """
    day_of_year = target_date.timetuple().tm_yday
    index = (day_of_year - 1) % len(EMOJIS)  # -1 because tm_yday starts at 1
    return EMOJIS[index]

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an emoji forecast for a given date.")
    parser.add_argument(
        "date",
        nargs="?",
        help="Date in ISO format (YYYY-MM-DD). Defaults to today.",
    )
    return parser.parse_args()

def main() -> None:
    args = _parse_args()
    if args.date:
        try:
            target_date = datetime.date.fromisoformat(args.date)
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {args.date}. Use YYYY-MM-DD.") from exc
    else:
        target_date = datetime.date.today()
    forecast = get_emoji_forecast(target_date)
    print(f"{target_date.isoformat()}: {forecast}")

if __name__ == "__main__":
    main()
