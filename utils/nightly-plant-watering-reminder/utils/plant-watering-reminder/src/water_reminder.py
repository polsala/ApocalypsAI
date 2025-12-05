"""plant_watering_reminder – determine which plants need watering today.

This module is deliberately self‑contained: it only uses the Python standard library.
"""

from __future__ import annotations

import argparse
import datetime as dt
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Plant:
    """Simple representation of a houseplant.

    Attributes
    ----------
    name: str
        Human‑readable name of the plant.
    interval_days: int
        How often the plant should be watered (in days).
    last_watered: dt.date
        The date the plant was last watered.
    """

    name: str
    interval_days: int
    last_watered: dt.date


def days_since(date: dt.date, today: dt.date) -> int:
    """Return the number of full days between *date* and *today*.

    The function is pure and easy to mock in tests.
    """
    return (today - date).days


def plants_to_water(plants: List[Plant], today: dt.date) -> List[str]:
    """Return a list of plant names that need watering on *today*.

    A plant needs watering when the number of days since it was last watered
    is greater than or equal to its watering interval.
    """
    due: List[str] = []
    for plant in plants:
        if days_since(plant.last_watered, today) >= plant.interval_days:
            due.append(plant.name)
    return due


# Example configuration – users can edit this list or import the module.
DEFAULT_PLANTS: List[Plant] = [
    Plant(name="Spider Plant", interval_days=7, last_watered=dt.date(2025, 11, 20)),
    Plant(name="Aloe Vera", interval_days=14, last_watered=dt.date(2025, 11, 10)),
    Plant(name="Peace Lily", interval_days=3, last_watered=dt.date(2025, 11, 25)),
]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tell you which houseplants need watering today.")
    parser.add_argument(
        "--date",
        type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d").date(),
        default=dt.date.today(),
        help="Override today's date (YYYY‑MM‑DD). Useful for testing.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    due = plants_to_water(DEFAULT_PLANTS, args.date)
    if due:
        print("Plants that need watering today:")
        for name in due:
            print(f"- {name}")
    else:
        print("All plants are happy – no watering needed today!")


if __name__ == "__main__":
    main()
