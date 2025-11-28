"""emoji_weather_forecast/src/forecast.py

Provides a deterministic emoji weather forecast based on a given date.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from typing import Final

# Mapping from deterministic index to emoji
_EMOJI_MAP: Final[list[str]] = ["☀️", "🌤️", "🌧️", "⛈️"]


def _index_for_date(target_date: date) -> int:
    """Return a deterministic index (0‑3) for *target_date*.

    The algorithm is deliberately simple: use the ordinal value of the date
    (days since 0001‑01‑01) modulo the number of emojis.
    """
    return target_date.toordinal() % len(_EMOJI_MAP)


def get_forecast(target_date: date) -> str:
    """Return the weather emoji for *target_date*.

    Parameters
    ----------
    target_date: date
        The date for which to generate the forecast.

    Returns
    -------
    str
        One of the emojis defined in ``_EMOJI_MAP``.
    """
    idx = _index_for_date(target_date)
    return _EMOJI_MAP[idx]


def _parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic emoji weather forecast")
    parser.add_argument(
        "date",
        nargs="?",
        default=None,
        help="Date in ISO format (YYYY-MM-DD). Defaults to today.",
    )
    return parser.parse_args(argv)


def _main(argv: list[str] | None = None) -> int:
    args = _parse_cli_args(argv)
    if args.date:
        try:
            target = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            print(f"Invalid date format: {args.date}. Expected YYYY-MM-DD.", file=sys.stderr)
            return 1
    else:
        target = date.today()
    print(get_forecast(target))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
