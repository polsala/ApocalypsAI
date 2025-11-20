import sys
import datetime
from typing import List

EMOJI_PALETTE: List[str] = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "⛅",   # partly cloudy
    "🌥️",  # mostly cloudy
    "☁️",  # cloudy
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌩️",  # lightning
    "❄️",  # snow
    "🌪️",  # tornado
    "🌈",  # rainbow
    "🌫️",  # fog
]


def _day_of_year(date: datetime.date) -> int:
    """Return the day of year (1‑based)."""
    return date.timetuple().tm_yday


def get_forecast(date: datetime.date) -> str:
    """Return a three‑emoji forecast string for *date*.

    The algorithm is deliberately simple and deterministic:
    * primary  = palette[day % len]
    * secondary = palette[(day + 3) % len]
    * tertiary  = palette[(day + 7) % len]
    """
    day = _day_of_year(date)
    n = len(EMOJI_PALETTE)
    primary = EMOJI_PALETTE[day % n]
    secondary = EMOJI_PALETTE[(day + 3) % n]
    tertiary = EMOJI_PALETTE[(day + 7) % n]
    return primary + secondary + tertiary


def _parse_date(arg: str) -> datetime.date:
    """Parse a YYYY‑MM‑DD string into a date. Raises ValueError on failure."""
    return datetime.datetime.strptime(arg, "%Y-%m-%d").date()


def main(argv: List[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) == 0:
        target_date = datetime.date.today()
    elif len(argv) == 1:
        try:
            target_date = _parse_date(argv[0])
        except ValueError as exc:
            print(f"Invalid date format: {argv[0]} (expected YYYY-MM-DD)", file=sys.stderr)
            return 1
    else:
        print("Usage: python -m src.forecast [YYYY-MM-DD]", file=sys.stderr)
        return 2

    forecast = get_forecast(target_date)
    print(forecast)
    return 0


if __name__ == "__main__":
    sys.exit(main())
