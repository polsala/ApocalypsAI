import argparse
import datetime
from typing import Tuple

# ---------------------------------------------------------------------------
# Moon phase calculation (based on Conway's algorithm)
# ---------------------------------------------------------------------------

def _julian_day(date: datetime.date) -> int:
    """Return the Julian Day Number for a Gregorian date.
    This implementation follows the algorithm from the US Naval Observatory.
    """
    a = (14 - date.month) // 12
    y = date.year + 4800 - a
    m = date.month + 12 * a - 3
    jd = date.day + ((153 * m + 2) // 5) + 365 * y
    jd += y // 4 - y // 100 + y // 400 - 32045
    return jd


def _moon_age(jd: int) -> float:
    """Calculate the moon's age in days for a given Julian Day.
    The synodic month is approximated as 29.53058867 days.
    """
    # Known new moon on 2000‑01‑06 (Julian Day 2451549.5)
    known_new_moon_jd = 2451550  # integer part for simplicity
    days_since_new = jd - known_new_moon_jd
    # Normalize to [0, 29.53058867)
    age = (days_since_new % 29.53058867)
    return age


def _phase_from_age(age: float) -> Tuple[str, str]:
    """Map moon age to a phase name and emoji.
    The boundaries are chosen to split the lunation into eight equal parts.
    """
    if age < 1.84566:
        return "New Moon", "🌑"
    elif age < 5.53699:
        return "Waxing Crescent", "🌒"
    elif age < 9.22831:
        return "First Quarter", "🌓"
    elif age < 12.91963:
        return "Waxing Gibbous", "🌔"
    elif age < 16.61096:
        return "Full Moon", "🌕"
    elif age < 20.30228:
        return "Waning Gibbous", "🌖"
    elif age < 23.99361:
        return "Last Quarter", "🌗"
    elif age < 27.68493:
        return "Waning Crescent", "🌘"
    else:
        return "New Moon", "🌑"


def get_moon_phase(date: datetime.date) -> Tuple[str, str]:
    """Return the lunar phase name and emoji for *date*.

    Parameters
    ----------
    date: datetime.date
        The Gregorian calendar date.

    Returns
    -------
    (phase_name, emoji): Tuple[str, str]
    """
    jd = _julian_day(date)
    age = _moon_age(jd)
    return _phase_from_age(age)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report the moon phase for a given date.")
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Date in YYYY-MM-DD format (defaults to today).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            raise SystemExit("Invalid date format. Use YYYY-MM-DD.")
    else:
        target_date = datetime.date.today()

    phase, emoji = get_moon_phase(target_date)
    print(f"{target_date}: {phase} {emoji}")


if __name__ == "__main__":
    main()
