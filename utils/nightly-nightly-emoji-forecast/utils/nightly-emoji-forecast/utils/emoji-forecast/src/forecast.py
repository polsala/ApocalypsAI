'''emoji forecast utility'''

import argparse
import datetime
import random
from typing import List

WEATHER_EMOJIS = ["☀️", "🌤️", "⛅", "🌥️", "☁️", "🌦️", "🌧️", "⛈️", "🌩️", "🌨️", "❄️", "🌪️"]
EVENT_EMOJIS = ["🚀", "🎉", "🛠️", "📚", "🍕", "🧩", "💡", "🐛", "⚡", "🧪"]


def _pick_emojis(seed: int, pool: List[str], count: int) -> List[str]:
    rnd = random.Random(seed)
    return [rnd.choice(pool) for _ in range(count)]


def get_forecast(date: datetime.date) -> str:
    """Return a short emoji forecast for the given date."""
    seed = date.toordinal()
    weather = _pick_emojis(seed, WEATHER_EMOJIS, 2)
    event = _pick_emojis(seed + 1, EVENT_EMOJIS, 1)[0]
    return f"{''.join(weather)} {event}"


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an emoji forecast.")
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Date for the forecast (YYYY-MM-DD). Defaults to today.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()
    target_date = args.date or datetime.date.today()
    print(get_forecast(target_date))


if __name__ == "__main__":
    main()
