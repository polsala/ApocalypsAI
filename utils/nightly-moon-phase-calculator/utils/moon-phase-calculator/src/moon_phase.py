import argparse
import datetime
from typing import Tuple

# ---------------------------------------------------------------------------
# Moon phase calculation (simple algorithm)
# ---------------------------------------------------------------------------

# Reference new moon: 2000‑01‑06 (known astronomical new moon)
_REFERENCE_NEW_MOON = datetime.date(2000, 1, 6)
_LUNATION = 29.53058867  # average length of a lunar cycle in days

_PHASES: Tuple[Tuple[float, float, str, str], ...] = (
    (0.0, 0.0625, "New Moon", "🌑"),
    (0.0625, 0.1875, "Waxing Crescent", "🌒"),
    (0.1875, 0.3125, "First Quarter", "🌓"),
    (0.3125, 0.4375, "Waxing Gibbous", "🌔"),
    (0.4375, 0.5625, "Full Moon", "🌕"),
    (0.5625, 0.6875, "Waning Gibbous", "🌖"),
    (0.6875, 0.8125, "Last Quarter", "🌗"),
    (0.8125, 0.9375, "Waning Crescent", "🌘"),
    (0.9375, 1.0, "New Moon", "🌑"),
)


def calculate_moon_phase(target_date: datetime.date) -> Tuple[str, str]:
    """Return the lunar phase name and its emoji for *target_date*.

    The calculation follows a simple lunation‑fraction approach and is
    sufficient for casual, whimsical use.
    """
    days_since_ref = (target_date - _REFERENCE_NEW_MOON).days
    # Normalise to a positive value within one lunation
    lunation_fraction = (days_since_ref % _LUNATION) / _LUNATION
    for low, high, name, emoji in _PHASES:
        if low <= lunation_fraction < high:
            return name, emoji
    # Fallback (should never happen)
    return "New Moon", "🌑"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate the lunar phase for a given date."
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date in YYYY-MM-DD format. Defaults to today.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.date:
        try:
            target = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {args.date}. Use YYYY-MM-DD.") from exc
    else:
        target = datetime.date.today()
    name, emoji = calculate_moon_phase(target)
    if args.date:
        print(f"{target} is a {name} {emoji}")
    else:
        print(f"Today ({target}) is a {name} {emoji}")


if __name__ == "__main__":
    main()
