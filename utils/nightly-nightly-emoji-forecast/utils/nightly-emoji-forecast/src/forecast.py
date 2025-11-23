import sys
import datetime
import hashlib
from typing import List

# List of emoji "weather" symbols – whimsical but deterministic.
EMOJI_WEATHER: List[str] = [
    "☀️",  # Sunny
    "🌤️",  # Partly sunny
    "⛅",   # Cloudy
    "🌥️",  # Overcast
    "☁️",  # Foggy
    "🌦️",  # Light rain
    "🌧️",  # Heavy rain
    "⛈️",  # Thunderstorm
    "🌨️",  # Snow
    "❄️",   # Blizzard
    "🌪️",  # Windy
    "🌈",   # Rainbow (good vibes)
]

def _seed_from_date(date: datetime.date) -> int:
    """Create a stable integer seed from a date.

    The ISO‑format string is hashed with SHA‑256 and the first 8 bytes are
    interpreted as a big‑endian integer.
    """
    iso = date.isoformat().encode("utf-8")
    digest = hashlib.sha256(iso).digest()
    return int.from_bytes(digest[:8], "big")

def get_forecast(date: datetime.date) -> str:
    """Return a deterministic emoji forecast for *date*.

    The forecast consists of 3 emojis selected from ``EMOJI_WEATHER`` based on
    a pseudo‑random sequence seeded by the date. Because the seed is derived
    solely from the date, the same input always yields the same output.
    """
    seed = _seed_from_date(date)
    # Simple linear congruential generator (LCG) – lightweight, no external deps.
    a, c, m = 1664525, 1013904223, 2 ** 32
    rng = seed
    emojis = []
    for _ in range(3):
        rng = (a * rng + c) % m
        idx = rng % len(EMOJI_WEATHER)
        emojis.append(EMOJI_WEATHER[idx])
    return " ".join(emojis)

def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m forecast <YYYY-MM-DD>")
        sys.exit(1)
    try:
        input_date = datetime.date.fromisoformat(sys.argv[1])
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)
    print(get_forecast(input_date))

if __name__ == "__main__":
    _cli()
