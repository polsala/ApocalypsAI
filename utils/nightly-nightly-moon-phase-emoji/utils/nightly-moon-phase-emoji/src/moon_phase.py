"""moon_phase.py

Utility to calculate the lunar phase for a given date and return a matching emoji.

The algorithm is based on the simple lunation calculation using a known reference new moon.
It is deterministic, offline, and requires only the Python standard library.
"""

from __future__ import annotations

import argparse
import datetime
from typing import Tuple

# Known new moon reference: 2000‑01‑06 18:14 UTC (Julian Day 2451549.26)
# For our purposes we use the date part only.
_REFERENCE_NEW_MOON = datetime.date(2000, 1, 6)
# Length of a synodic month in days (average)
_SYNODIC_MONTH = 29.53058867

_PHASES = [
    ("New Moon", "🌑"),
    ("Waxing Crescent", "🌒"),
    ("First Quarter", "🌓"),
    ("Waxing Gibbous", "🌔"),
    ("Full Moon", "🌕"),
    ("Waning Gibbous", "🌖"),
    ("Last Quarter", "🌗"),
    ("Waning Crescent", "🌘"),
]

# Thresholds are fractions of the lunation cycle.
_THRESHOLDS = [
    0.0,
    0.0625,
    0.1875,
    0.3125,
    0.4375,
    0.5625,
    0.6875,
    0.8125,
    0.9375,
    1.0,
]


def _lunation_fraction(target: datetime.date) -> float:
    """Return the fraction of the current lunation (0‑1) for *target*.

    The calculation is:
        days_since_reference % SYNODIC_MONTH / SYNODIC_MONTH
    """
    delta = (target - _REFERENCE_NEW_MOON).days
    # Mock rationale: using integer days ensures deterministic, timezone‑free result.
    lunation = (delta % _SYNODIC_MONTH) / _SYNODIC_MONTH
    return lunation


def get_moon_phase(target: datetime.date) -> Tuple[str, str]:
    """Return a tuple ``(phase_name, emoji)`` for *target* date.

    Parameters
    ----------
    target: datetime.date
        The date for which to compute the lunar phase.
    """
    fraction = _lunation_fraction(target)
    # Find the appropriate phase based on thresholds.
    for i in range(len(_THRESHOLDS) - 1):
        if _THRESHOLDS[i] <= fraction < _THRESHOLDS[i + 1]:
            return _PHASES[i]
    # Fallback – should never happen because thresholds cover [0,1).
    return _PHASES[-1]


def _parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print the moon phase and emoji for a given date.")
    parser.add_argument(
        "date",
        nargs="?",
        default=datetime.date.today().isoformat(),
        help="Date in ISO format (YYYY-MM-DD). Defaults to today.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_cli()
    try:
        target_date = datetime.date.fromisoformat(args.date)
    except ValueError as exc:
        raise SystemExit(f"Invalid date format: {args.date}") from exc
    phase, emoji = get_moon_phase(target_date)
    print(f"{phase} {emoji}")


if __name__ == "__main__":
    main()
