"""
Daily Emoji Forecast utility
Provides a deterministic emoji forecast based on a date.
"""

import hashlib
import datetime
from typing import List

EMOJIS: List[str] = [
    "🌞",
    "🌧️",
    "🌪️",
    "🌋",
    "🌈",
    "🌑",
    "🔥",
    "❄️",
    "🌊",
    "🌟",
]


def _hash_date(date: datetime.date) -> int:
    """Return a stable integer hash for the given date.

    Uses SHA‑256 on the ISO‑format string of the date.
    """
    date_str = date.isoformat()
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    return int(digest, 16)


def get_forecast(date: datetime.date) -> str:
    """Return an emoji forecast for the given date."""
    idx = _hash_date(date) % len(EMOJIS)
    return EMOJIS[idx]


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Get a whimsical emoji forecast for a date.")
    parser.add_argument(
        "date",
        nargs="?",
        default=datetime.date.today().isoformat(),
        help="Date in YYYY-MM-DD format (default: today).",
    )
    args = parser.parse_args()
    try:
        target_date = datetime.date.fromisoformat(args.date)
    except ValueError as exc:
        raise SystemExit(f"Invalid date format: {args.date}") from exc
    print(get_forecast(target_date))


if __name__ == "__main__":
    main()
