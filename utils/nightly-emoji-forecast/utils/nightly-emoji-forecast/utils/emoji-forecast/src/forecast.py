import sys
import datetime
from typing import List

# A small palette of weather‑related emojis
EMOJIS = [
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
    "🌈",
    "🌪️",
    "🌫️",
]


def get_forecast(date: datetime.date) -> str:
    """Return a deterministic three‑emoji forecast for *date*.

    The algorithm is simple and offline:
    1. Convert the date to its ordinal (days since 0001‑01‑01).
    2. Use the ordinal modulo the emoji list length as a starting index.
    3. Return three consecutive emojis, wrapping around the list.
    """
    base = date.toordinal() % len(EMOJIS)
    forecast_emojis: List[str] = [
        EMOJIS[(base + i) % len(EMOJIS)] for i in range(3)
    ]
    return "".join(forecast_emojis)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m emoji_forecast <YYYY-MM-DD>")
        sys.exit(1)
    try:
        target_date = datetime.date.fromisoformat(sys.argv[1])
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)
    print(get_forecast(target_date))


if __name__ == "__main__":
    main()
