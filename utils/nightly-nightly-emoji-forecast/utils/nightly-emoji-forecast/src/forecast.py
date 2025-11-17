import sys
import datetime
import hashlib

# 🌤️ Weather emojis – ordered from sunny to extreme
WEATHER_EMOJIS = [
    "☀️",
    "🌤️",
    "⛅️",
    "🌥️",
    "☁️",
    "🌦️",
    "🌧️",
    "⛈️",
    "🌩️",
    "🌨️",
    "❄️",
    "🌪️",
]

# 😀 Mood emojis – from happy to sleepy
MOOD_EMOJIS = [
    "😀",
    "🙂",
    "😐",
    "🙁",
    "😞",
    "😢",
    "😴",
    "🤔",
    "🤩",
    "🤪",
]


def _deterministic_index(seed: str, length: int) -> int:
    """Return a reproducible index in ``0..length-1`` based on ``seed``.

    The function hashes the seed with SHA‑256, interprets the hex digest as an
    integer, and takes the modulo with ``length``.
    """
    h = hashlib.sha256(seed.encode()).hexdigest()
    return int(h, 16) % length


def get_forecast(date: datetime.date) -> str:
    """Return a two‑emoji forecast for *date*.

    The first emoji is a weather symbol, the second a mood symbol.
    """
    iso = date.isoformat()
    weather_idx = _deterministic_index(f"weather-{iso}", len(WEATHER_EMOJIS))
    mood_idx = _deterministic_index(f"mood-{iso}", len(MOOD_EMOJIS))
    return f"{WEATHER_EMOJIS[weather_idx]}{MOOD_EMOJIS[mood_idx]}"


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.forecast <YYYY-MM-DD>")
        sys.exit(1)
    try:
        target_date = datetime.date.fromisoformat(sys.argv[1])
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)
    print(get_forecast(target_date))


if __name__ == "__main__":
    main()
