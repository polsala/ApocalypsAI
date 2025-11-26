"""emoji_forecast.py

Provides a deterministic emoji "weather" forecast for a given ISO‑format date string.

Functions
---------
get_forecast(date_str: str) -> str
    Returns an emoji representing the forecast for the supplied date.
"""

import hashlib
from datetime import datetime
from typing import List

# List of emojis to choose from – order matters for deterministic mapping
_EMOJIS: List[str] = ["🌞", "🌦️", "🌧️", "❄️", "🌪️"]


def _hash_date(date_str: str) -> int:
    """Return a stable integer hash for the given date string.

    The function uses SHA‑256 to avoid platform‑dependent hash randomization.
    """
    # Ensure the date string is a valid ISO date; raise ValueError otherwise
    datetime.strptime(date_str, "%Y-%m-%d")
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    # Convert a portion of the hex digest to an integer
    return int(digest[:8], 16)


def get_forecast(date_str: str) -> str:
    """Return an emoji forecast for the supplied ISO‑format date string.

    Parameters
    ----------
    date_str: str
        Date in ``YYYY-MM-DD`` format.

    Returns
    -------
    str
        One of the emojis defined in ``_EMOJIS``.
    """
    idx = _hash_date(date_str) % len(_EMOJIS)
    return _EMOJIS[idx]


def _cli() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Deterministic emoji weather forecast")
    parser.add_argument("date", help="Date in YYYY-MM-DD format")
    args = parser.parse_args()
    try:
        print(get_forecast(args.date))
    except ValueError as exc:
        raise SystemExit(f"Invalid date: {exc}")


if __name__ == "__main__":
    _cli()
