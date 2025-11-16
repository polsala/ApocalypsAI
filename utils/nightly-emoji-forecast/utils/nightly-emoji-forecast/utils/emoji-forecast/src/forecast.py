from datetime import date
from typing import List

_EMOJIS: List[str] = [
    "☀️",
    "🌤️",
    "⛅",
    "🌥️",
    "☁️",
    "🌧️",
    "⛈️",
    "🌩️",
    "🌨️",
    "❄️",
    "🌪️",
    "🌈",
]


def get_emoji_for_date(target_date: date) -> str:
    """Return an emoji based on the given date.

    The algorithm is deterministic: days since 1970‑01‑01 modulo the emoji list length.
    """
    epoch = date(1970, 1, 1)
    days = (target_date - epoch).days
    index = days % len(_EMOJIS)
    return _EMOJIS[index]


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Get an emoji forecast for a date.")
    parser.add_argument(
        "date",
        nargs="?",
        help="Date in YYYY-MM-DD format (defaults to today).",
    )
    args = parser.parse_args()
    if args.date:
        target = date.fromisoformat(args.date)
    else:
        target = date.today()
    print(get_emoji_for_date(target))


if __name__ == "__main__":
    main()
