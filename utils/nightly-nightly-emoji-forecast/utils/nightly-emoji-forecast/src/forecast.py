"""Emoji weather forecast utility.

Provides a deterministic emoji forecast based on a given date.
"""

from __future__ import annotations

import datetime
import random
from typing import List

# Mapping of weather conditions to emojis
_WEATHER_EMOJIS: List[str] = [
    "☀️",   # sunny
    "🌤️",  # partly sunny
    "⛅",   # cloudy
    "🌥️",  # overcast
    "🌧️",  # rain
    "⛈️",   # thunderstorm
    "❄️",   # snow
    "🌪️",  # tornado
    "🌈",   # rainbow
    "🌫️",  # fog
]


def _pick_emojis(seed: int, count: int = 3) -> List[str]:
    """Return a list of `count` emojis selected deterministically.

    Args:
        seed: Integer seed for the random generator.
        count: Number of emojis to return.

    Returns:
        List of emojis.
    """
    rnd = random.Random(seed)
    # Mock rationale: using deterministic Random ensures reproducibility without external state.
    return [rnd.choice(_WEATHER_EMOJIS) for _ in range(count)]


def generate_forecast(date: datetime.date | None = None) -> str:
    """Generate an emoji forecast string for the given date.

    If `date` is ``None``, uses today's date.

    Returns:
        A space‑separated string of emojis.
    """
    if date is None:
        date = datetime.date.today()
    seed = date.toordinal()
    emojis = _pick_emojis(seed)
    return " ".join(emojis)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate an emoji weather forecast.")
    parser.add_argument(
        "date",
        nargs="?",
        help="Date in YYYY-MM-DD format (defaults to today).",
    )
    args = parser.parse_args()
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {exc}")
    else:
        target_date = None
    print(generate_forecast(target_date))
