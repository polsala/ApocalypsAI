"""moon_phase.py

A lightweight, pure‑Python Moon phase calculator.

Provides:
* ``get_moon_phase(date)`` – returns a human‑readable phase name.
* ``main()`` – CLI entry point.

The algorithm is based on John Conway's method (public domain) and is accurate enough for casual use.
"""

from __future__ import annotations

import argparse
import datetime
from enum import Enum
from typing import Final


class Phase(Enum):
    NEW_MOON = "New Moon"
    WAXING_CRESCENT = "Waxing Crescent"
    FIRST_QUARTER = "First Quarter"
    WAXING_GIBBOUS = "Waxing Gibbous"
    FULL_MOON = "Full Moon"
    WANING_GIBBOUS = "Waning Gibbous"
    LAST_QUARTER = "Last Quarter"
    WANING_CRESCENT = "Waning Crescent"

# Length of a synodic month (new moon to new moon) in days
LUNATION: Final[float] = 29.53058867

# Reference new moon: 2000‑01‑06 (UTC) – known new moon date
REFERENCE_NEW_MOON = datetime.date(2000, 1, 6)


def _moon_age(target: datetime.date) -> float:
    """Return the Moon's age in days for *target*.

    The age is the number of days since the most recent new moon.
    """
    delta_days = (target - REFERENCE_NEW_MOON).days
    # Normalise to a positive value within one lunation
    age = (delta_days % LUNATION)
    return age


def get_moon_phase(target: datetime.date) -> str:
    """Return the Moon phase name for *target*.

    The mapping follows the conventional eight‑phase division:
    * 0‑1.84566   → New Moon
    * 1.84566‑5.53699 → Waxing Crescent
    * 5.53699‑9.22831 → First Quarter
    * 9.22831‑12.91963 → Waxing Gibbous
    * 12.91963‑16.61096 → Full Moon
    * 16.61096‑20.30228 → Waning Gibbous
    * 20.30228‑23.99361 → Last Quarter
    * 23.99361‑27.68493 → Waning Crescent
    * 27.68493‑29.53058 → New Moon (again)
    """
    age = _moon_age(target)
    # Phase thresholds (in days) – derived from dividing the lunation into 8 equal parts
    if age < 1.84566:
        phase = Phase.NEW_MOON
    elif age < 5.53699:
        phase = Phase.WAXING_CRESCENT
    elif age < 9.22831:
        phase = Phase.FIRST_QUARTER
    elif age < 12.91963:
        phase = Phase.WAXING_GIBBOUS
    elif age < 16.61096:
        phase = Phase.FULL_MOON
    elif age < 20.30228:
        phase = Phase.WANING_GIBBOUS
    elif age < 23.99361:
        phase = Phase.LAST_QUARTER
    elif age < 27.68493:
        phase = Phase.WANING_CRESCENT
    else:
        phase = Phase.NEW_MOON
    return phase.value


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate the Moon phase for a given date (ISO format YYYY‑MM‑DD)."
    )
    parser.add_argument(
        "date",
        nargs="?",
        default=None,
        help="Date to evaluate (default: today).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.date:
        try:
            target_date = datetime.date.fromisoformat(args.date)
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {args.date!r}. Use YYYY-MM-DD.") from exc
    else:
        target_date = datetime.date.today()
    phase = get_moon_phase(target_date)
    print(f"{target_date.isoformat()} → {phase}")


if __name__ == "__main__":
    main()
