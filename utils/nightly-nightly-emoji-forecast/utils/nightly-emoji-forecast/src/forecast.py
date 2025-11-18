"""emoji_forecast
===================

Provides a deterministic, emoji‑based weather forecast for a given date.

The algorithm is deliberately simple: it hashes the ISO‑formatted date string,
mods it by the number of available emojis, and returns the selected emoji.

This module can be used as a library (`get_emoji_forecast`) or as a tiny CLI.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
from typing import List

# 🌞 ☀️ 🌤️ 🌥️ 🌦️ 🌧️ ⛈️ 🌩️ 🌨️ ❄️ 🌈 🌪️
EMOJI_WEATHER: List[str] = [
    "☀️",  # clear sky
    "🌤️",  # few clouds
    "🌥️",  # scattered clouds
    "🌦️",  # rain showers
    "🌧️",  # steady rain
    "⛈️",  # thunderstorm
    "🌩️",  # lightning
    "🌨️",  # snow
    "❄️",  # snowflake
    "🌈",  # rainbow
    "🌪️",  # tornado
]


def _hash_date(date: datetime.date) -> int:
    """Return a stable integer hash for *date*.

    The hash is derived from the SHA‑256 digest of the ISO‑format string, ensuring
    the same result across Python versions and platforms.
    """
    iso = date.isoformat().encode("utf-8")
    digest = hashlib.sha256(iso).hexdigest()
    # Take the first 8 hex chars → 32‑bit integer
    return int(digest[:8], 16)


def get_emoji_forecast(date: datetime.date) -> str:
    """Return an emoji representing the weather forecast for *date*.

    The function is deterministic: the same *date* always yields the same emoji.
    """
    idx = _hash_date(date) % len(EMOJI_WEATHER)
    return EMOJI_WEATHER[idx]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an emoji weather forecast for a given date.")
    parser.add_argument(
        "date",
        nargs="?",
        default=datetime.date.today().isoformat(),
        help="Date in ISO format (YYYY-MM-DD). Defaults to today.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        target_date = datetime.date.fromisoformat(args.date)
    except ValueError as exc:
        raise SystemExit(f"Invalid date format: {args.date!r}. Expected YYYY-MM-DD.") from exc
    forecast = get_emoji_forecast(target_date)
    print(forecast)


if __name__ == "__main__":
    main()
