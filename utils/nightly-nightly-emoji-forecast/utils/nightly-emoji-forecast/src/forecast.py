"""
emoji forecast utility
"""

import datetime
import hashlib
from typing import List

# List of weather emojis ordered for deterministic mapping
WEATHER_EMOJIS: List[str] = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "⛅",   # cloudy
    "🌥️",  # mostly cloudy
    "☁️",  # overcast
    "🌦️",  # light rain
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌨️",  # snow
    "🌩️",  # lightning
    "🌈",  # rainbow
    "🌪️",  # tornado
]


def _hash_date(date: datetime.date) -> int:
    """Return an integer hash for the given date."""
    # Use ISO format, encode, then SHA256, convert to int
    iso = date.isoformat().encode("utf-8")
    digest = hashlib.sha256(iso).hexdigest()
    return int(digest, 16)


def get_emoji_forecast(date: datetime.date) -> str:
    """
    Deterministically map a date to a weather emoji.

    Parameters
    ----------
    date: datetime.date
        The date for which to generate the forecast.

    Returns
    -------
    str
        A single emoji representing the forecast.
    """
    hash_int = _hash_date(date)
    index = hash_int % len(WEATHER_EMOJIS)
    return WEATHER_EMOJIS[index]


def main() -> None:
    """CLI entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="Generate an emoji weather forecast for a given date.")
    parser.add_argument(
        "date",
        nargs="?",
        default=datetime.date.today().isoformat(),
        help="Date in YYYY-MM-DD format (default: today)",
    )
    args = parser.parse_args()
    try:
        target_date = datetime.date.fromisoformat(args.date)
    except ValueError as exc:
        raise SystemExit(f"Invalid date format: {args.date}") from exc
    print(get_emoji_forecast(target_date))


if __name__ == "__main__":
    main()
