"""
emoji forecast utility

Generates a deterministic, whimsical weather forecast composed of emojis.
"""

import argparse
import datetime
import hashlib
from typing import List

# A small, deterministic palette of weather‑related emojis.
EMOJIS = [
    "☀️",  # sunny
    "🌤️",  # sun behind small cloud
    "⛅",   # sun behind cloud
    "🌥️",  # sun behind large cloud
    "☁️",  # cloud
    "🌦️",  # sun behind rain cloud
    "🌧️",  # cloud with rain
    "⛈️",  # cloud with lightning
    "🌩️",  # high voltage
    "🌨️",  # cloud with snow
    "❄️",   # snowflake
    "🌪️",  # tornado
]


def _hash_date(date_str: str) -> int:
    """Return a deterministic integer hash for a date string.

    The hash is derived from the SHA‑256 digest of the ISO‑formatted date.
    """
    return int(hashlib.sha256(date_str.encode()).hexdigest(), 16)


def get_emoji_forecast(date: datetime.date, length: int = 3) -> List[str]:
    """Return a list of `length` emojis representing the forecast.

    The selection is deterministic: the same `date` and `length` always produce the same list.
    """
    base = _hash_date(date.isoformat())
    forecast = []
    for i in range(length):
        idx = (base + i) % len(EMOJIS)
        forecast.append(EMOJIS[idx])
    return forecast


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a deterministic emoji weather forecast."
    )
    parser.add_argument(
        "date",
        nargs="?",
        default=datetime.date.today().isoformat(),
        help="Date in YYYY‑MM‑DD format (default: today)",
    )
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        default=3,
        help="Number of emojis to generate (default: 3)",
    )
    args = parser.parse_args()

    try:
        date_obj = datetime.date.fromisoformat(args.date)
    except ValueError as exc:
        raise SystemExit(f"Invalid date format: {args.date}") from exc

    forecast = get_emoji_forecast(date_obj, length=args.num)
    print("".join(forecast))


if __name__ == "__main__":
    main()
