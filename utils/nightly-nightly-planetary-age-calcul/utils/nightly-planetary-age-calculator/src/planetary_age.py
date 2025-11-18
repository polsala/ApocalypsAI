'''planetary_age.py
Utility to calculate age on different planets.
'''

from __future__ import annotations
import sys

# Orbital periods relative to Earth years
PLANET_ORBITAL_PERIODS = {
    "mercury": 0.2408467,
    "venus": 0.61519726,
    "earth": 1.0,
    "mars": 1.8808158,
    "jupiter": 11.862615,
    "saturn": 29.447498,
    "uranus": 84.016846,
    "neptune": 164.79132,
    "pluto": 248.00,
}


def age_on_planet(earth_years: float, planet: str) -> float:
    """Return the age on *planet* given *earth_years*.

    The result is rounded to two decimal places.
    Raises:
        ValueError: If *planet* is not in the supported list.
    """
    planet_key = planet.lower()
    if planet_key not in PLANET_ORBITAL_PERIODS:
        raise ValueError(f"Unsupported planet: {planet}")
    period = PLANET_ORBITAL_PERIODS[planet_key]
    age = earth_years / period
    return round(age, 2)


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 2:
        print("Usage: python -m planetary_age <earth_years> <planet>")
        sys.exit(1)
    try:
        earth_years = float(argv[0])
    except ValueError:
        print("Invalid earth_years; must be a number.")
        sys.exit(1)
    planet = argv[1]
    try:
        result = age_on_planet(earth_years, planet)
    except ValueError as e:
        print(e)
        sys.exit(1)
    print(f"{result} years on {planet.lower()}")


if __name__ == "__main__":
    main()
