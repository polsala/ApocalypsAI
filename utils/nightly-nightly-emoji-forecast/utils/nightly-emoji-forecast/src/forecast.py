import datetime
from typing import List

# A curated list of emojis representing a "forecast". Feel free to extend!
EMOJI_PALETTE: List[str] = [
    "☀️",  # sunny
    "🌧️",  # rainy
    "⛈️",  # stormy
    "❄️",  # snowy
    "🌪️",  # windy
    "🌈",  # colorful
    "🌫️",  # foggy
    "🌞",  # bright
    "🌙",  # night
    "⚡",   # electric
]


def get_emoji_forecast(target_date: datetime.date) -> str:
    """Return a deterministic emoji forecast for *target_date*.

    The algorithm is deliberately simple and offline:
    1. Compute the day‑of‑year (1‑366, accounting for leap years).
    2. Modulo‑reduce it against the length of ``EMOJI_PALETTE``.
    3. Return the emoji at that index.

    Args:
        target_date: The date for which to generate the forecast.

    Returns:
        A single emoji string.
    """
    # ``timetuple().tm_yday`` gives the day of the year (1‑366).
    day_of_year = target_date.timetuple().tm_yday
    index = (day_of_year - 1) % len(EMOJI_PALETTE)
    return EMOJI_PALETTE[index]


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Print an emoji forecast for a given date.")
    parser.add_argument(
        "date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Date in YYYY-MM-DD format",
    )
    args = parser.parse_args()
    print(get_emoji_forecast(args.date))


if __name__ == "__main__":
    main()
