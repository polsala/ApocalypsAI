import sys
import hashlib
from datetime import datetime, date
from typing import List

# Fixed palette of whimsical weather emojis
EMOJI_PALETTE: List[str] = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "⛅",   # cloudy
    "🌥️",  # overcast
    "☁️",  # cloudy
    "🌦️",  # rain showers
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌨️",  # snow
    "❄️",   # snowflake
    "🌈",  # rainbow
    "🌪️",  # tornado
]


def _seed_from_date(target_date: date) -> int:
    """Create a deterministic integer seed from an ISO‑format date string.

    The function hashes the date string using SHA‑256 and converts the first
    eight hex characters to an integer. This provides a stable, reproducible
    seed without relying on the built‑in ``hash`` (which is salted per process).
    """
    iso = target_date.isoformat()
    digest = hashlib.sha256(iso.encode("utf-8")).hexdigest()
    # Use first 8 characters (~32 bits) for the seed
    return int(digest[:8], 16)


def get_emoji_forecast(target_date: date) -> str:
    """Return a two‑emoji forecast for *target_date*.

    The first emoji is the primary condition, the second is a complementary
    accent (e.g., a rainbow after rain). The selection is deterministic based
    on the date.
    """
    seed = _seed_from_date(target_date)
    primary_idx = seed % len(EMOJI_PALETTE)
    secondary_idx = (seed // len(EMOJI_PALETTE)) % len(EMOJI_PALETTE)
    return f"{EMOJI_PALETTE[primary_idx]} {EMOJI_PALETTE[secondary_idx]}"


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m nightly_emoji_forecast <YYYY-MM-DD>")
        sys.exit(1)
    try:
        user_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    except ValueError:
        print("Error: date must be in YYYY-MM-DD format")
        sys.exit(1)
    print(get_emoji_forecast(user_date))


if __name__ == "__main__":
    _cli()
