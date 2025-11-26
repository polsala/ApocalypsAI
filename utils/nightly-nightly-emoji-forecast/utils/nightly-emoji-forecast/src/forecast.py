import argparse
import datetime
import random
from typing import List

# A curated list of weather‑related emojis (feel free to extend).
EMOJIS: List[str] = [
    "☀️", "🌤️", "⛅", "🌥️", "☁️", "🌦️", "🌧️", "⛈️", "🌩️", "🌨️",
    "❄️", "🌪️", "🌈", "⚡", "💧", "☔", "🌙", "⭐", "🌟", "🔥",
]


def get_forecast(date: datetime.date) -> str:
    """Return a deterministic three‑emoji forecast for *date*.

    The algorithm:
    1. Convert the date to an integer seed ``YYYYMMDD``.
    2. Initialise ``random.Random`` with that seed.
    3. Choose three emojis (with replacement) from ``EMOJIS``.
    4. Join them with spaces.
    """
    seed = int(date.strftime("%Y%m%d"))
    rng = random.Random(seed)
    chosen = rng.choices(EMOJIS, k=3)
    return " ".join(chosen)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a deterministic emoji weather forecast.")
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Date for the forecast in YYYY-MM-DD format (defaults to today).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    target_date = args.date or datetime.date.today()
    forecast = get_forecast(target_date)
    print(forecast)


if __name__ == "__main__":
    main()
