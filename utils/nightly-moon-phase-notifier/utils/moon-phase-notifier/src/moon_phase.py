"""
moon_phase.py – Compute the lunar phase for a given date.

Algorithm based on John Conway's method, which yields an integer 0‑7
representing the eight principal phases.
"""

import argparse
import datetime
from typing import Tuple

PHASES = [
    "New Moon",
    "Waxing Crescent",
    "First Quarter",
    "Waxing Gibbous",
    "Full Moon",
    "Waning Gibbous",
    "Last Quarter",
    "Waning Crescent",
]


def _conway_phase(date: datetime.date) -> int:
    """Return an integer 0‑7 representing the moon phase for *date*.

    Reference: https://en.wikipedia.org/wiki/Conway%27s_Astronomical_Algorithm
    """
    y = date.year
    m = date.month
    d = date.day

    if m < 3:
        y -= 1
        m += 12

    k = y // 100
    t = k // 4
    e = 2 - k + t
    jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + e - 1524.5
    # Days since known new moon (2000‑01‑06)
    days = jd - 2451550.1
    new_moons = days / 29.53058867
    phase = (new_moons - int(new_moons)) * 8
    return int(round(phase)) % 8


def moon_phase(date: datetime.date) -> str:
    """Return the human‑readable moon phase for *date*."""
    idx = _conway_phase(date)
    return PHASES[idx]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print the moon phase for a given date (YYYY‑MM‑DD)."
    )
    parser.add_argument(
        "date",
        nargs="?",
        help="Date in ISO format (default: today).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.date:
        try:
            target = datetime.date.fromisoformat(args.date)
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {exc}")
    else:
        target = datetime.date.today()
    phase = moon_phase(target)
    print(f"Moon phase on {target}: {phase}")


if __name__ == "__main__":
    main()
