"""Emoji weather forecast utility."""

import argparse
import datetime
import hashlib
from typing import List

EMOJIS: List[str] = ["☀️", "🌤️", "⛅", "🌥️", "☁️", "🌧️", "⛈️", "❄️", "🌪️", "🌈"]


def get_forecast(date: datetime.date) -> str:
    """Return a deterministic emoji forecast for the given date.

    The algorithm hashes the ISO‑formatted date with SHA‑256, converts the
    hexadecimal digest to an integer, and selects an emoji by taking the
    remainder modulo the number of available emojis.
    """
    digest = hashlib.sha256(date.isoformat().encode()).hexdigest()
    idx = int(digest, 16) % len(EMOJIS)
    return EMOJIS[idx]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emoji weather forecast")
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Date for the forecast (YYYY-MM-DD). Defaults to today.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    target_date = args.date or datetime.date.today()
    print(get_forecast(target_date))


if __name__ == "__main__":
    main()
