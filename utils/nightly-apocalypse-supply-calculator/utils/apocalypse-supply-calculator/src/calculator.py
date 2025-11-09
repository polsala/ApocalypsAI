"""
apocalypse-supply-calculator

Provides a simple function to compute water (liters) and food (kilocalories) needed
for a group of survivors over a number of days.

Assumptions:
- Each person needs 3 liters of water per day.
- Each person needs 2000 kcal of food per day.
"""

import json
import sys
from typing import Dict

WATER_PER_PERSON_PER_DAY = 3  # liters
FOOD_KCAL_PER_PERSON_PER_DAY = 2000  # kcal


def calculate_supplies(survivors: int, days: int) -> Dict[str, int]:
    """Return a dict with total water (liters) and food (kcal) needed.

    Args:
        survivors: Number of people to provision for (must be >= 0).
        days: Number of days to survive (must be >= 0).

    Raises:
        ValueError: If either argument is negative.
    """
    if survivors < 0 or days < 0:
        raise ValueError("survivors and days must be non‑negative integers")
    total_water = survivors * days * WATER_PER_PERSON_PER_DAY
    total_food = survivors * days * FOOD_KCAL_PER_PERSON_PER_DAY
    return {"water_liters": total_water, "food_kcal": total_food}


def main(argv=None):
    """CLI entry point.

    Usage:
        python -m utils.apocalypse-supply-calculator.src.calculator <survivors> <days>
    """
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 2:
        print("Usage: python -m utils.apocalypse-supply-calculator.src.calculator <survivors> <days>")
        sys.exit(1)
    try:
        survivors = int(argv[0])
        days = int(argv[1])
    except ValueError:
        print("Both survivors and days must be integers.")
        sys.exit(1)
    try:
        supplies = calculate_supplies(survivors, days)
    except ValueError as e:
        print(str(e))
        sys.exit(1)
    print(json.dumps(supplies))


if __name__ == "__main__":
    main()
