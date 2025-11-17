import argparse
import datetime
import random
import sys
from typing import List

WEATHER_EMOJIS: List[str] = [
    "☀️", "🌤️", "⛅", "🌥️", "☁️", "🌦️", "🌧️", "⛈️", "🌩️", "🌨️", "❄️", "🌪️", "🌈", "☔️", "💨"
]


def _seed_random(target_date: datetime.date) -> None:
    """Seed the global random generator with a reproducible value derived from the date.

    The seed is the integer representation of the ISO formatted date string.
    """
    seed_str = target_date.isoformat()
    # Convert the ISO string to an integer hash for seeding.
    seed_int = int.from_bytes(seed_str.encode("utf-8"), "big")
    random.seed(seed_int)


def get_forecast(target_date: datetime.date) -> str:
    """Return a three‑emoji weather forecast for *target_date*.

    The result is deterministic: the same date always yields the same forecast.
    """
    _seed_random(target_date)
    emojis = random.sample(WEATHER_EMOJIS, 3)
    return "".join(emojis)


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a whimsical emoji weather forecast.")
    parser.add_argument(
        "--date",
        type=str,
        help="ISO date (YYYY-MM-DD). Defaults to today.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    if args.date:
        try:
            target_date = datetime.date.fromisoformat(args.date)
        except ValueError as exc:
            print(f"Invalid date format: {args.date}. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = datetime.date.today()

    forecast = get_forecast(target_date)
    print(f"{target_date.isoformat()}: {forecast}")


if __name__ == "__main__":
    main()
