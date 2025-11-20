"""emoji_forecast
===================

Provides a deterministic emoji‑based weather forecast.

Public API
----------
- ``get_forecast(date: datetime.date) -> str``
- ``main()`` – CLI entry point that prints today's forecast.
"""

from __future__ import annotations

import argparse
import datetime
import sys
from typing import List

# Mapping order is important for deterministic selection
_EMOJIS: List[str] = ["☀️", "🌤️", "🌧️", "❄️"]


def _deterministic_index(target_date: datetime.date) -> int:
    """Return an index 0‑3 based on the ISO week number and weekday.

    The formula is deliberately simple and fully deterministic:
    ``(iso_week * weekday) % len(_EMOJIS)``.
    """
    iso_week = target_date.isocalendar()[1]
    weekday = target_date.isoweekday()  # 1 (Mon) – 7 (Sun)
    return (iso_week * weekday) % len(_EMOJIS)


def get_forecast(target_date: datetime.date) -> str:
    """Return the weather emoji for *target_date*.

    Parameters
    ----------
    target_date: datetime.date
        The date for which to compute the forecast.

    Returns
    -------
    str
        One of the emojis defined in ``_EMOJIS``.
    """
    idx = _deterministic_index(target_date)
    return _EMOJIS[idx]


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a deterministic emoji weather forecast.")
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Optional date (YYYY-MM-DD). Defaults to today.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    today = args.date or datetime.date.today()
    forecast = get_forecast(today)
    print(f"{today.isoformat()}: {forecast}")


if __name__ == "__main__":
    # Allow execution via ``python -m utils.nightly-emoji-forecast.src.forecast``
    # Adjust sys.path so the relative import works when run as a module.
    # This block mirrors typical ``__main__`` behaviour.
    main()
