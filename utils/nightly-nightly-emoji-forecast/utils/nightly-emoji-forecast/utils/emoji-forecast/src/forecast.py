"""emoji_forecast – deterministic emoji weather generator.

The algorithm is intentionally simple: it hashes the ISO‑format date string
into an integer and selects an emoji from a fixed list. Because the hash is
based solely on the date, the result is repeatable and requires no network
access – perfect for offline unit tests.
"""

from __future__ import annotations

import argparse
import datetime
from typing import List

# Fixed list of weather‑related emojis (ordered for reproducibility)
EMOJIS: List[str] = [
    "☀️",  # sunny
    "🌤️",  # mostly sunny
    "⛅",   # partly cloudy
    "🌥️",  # mostly cloudy
    "☁️",  # cloudy
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "❄️",  # snow
    "🌪️",  # tornado
]


def _date_to_int(d: datetime.date) -> int:
    """Convert a date to an integer suitable for deterministic indexing.

    The implementation mirrors the one used in the test suite so that the
    mapping stays stable across releases.
    """
    # Use the ISO‑format YYYYMMDD as a plain integer.
    return int(d.strftime("%Y%m%d"))


def get_forecast(d: datetime.date) -> str:
    """Return the emoji forecast for *d*.

    Parameters
    ----------
    d: datetime.date
        The date for which to generate a forecast.

    Returns
    -------
    str
        An emoji representing the deterministic "weather" for the given date.
    """
    index = _date_to_int(d) % len(EMOJIS)
    return EMOJIS[index]


def _parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic emoji weather forecast")
    parser.add_argument(
        "date",
        nargs="?",
        default=datetime.date.today().isoformat(),
        help="Date in YYYY‑MM‑DD format (default: today)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_cli()
    try:
        target_date = datetime.date.fromisoformat(args.date)
    except ValueError as exc:
        raise SystemExit(f"Invalid date format: {args.date}") from exc
    print(get_forecast(target_date))


if __name__ == "__main__":
    main()
