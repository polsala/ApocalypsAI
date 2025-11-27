import hashlib
from datetime import datetime
from typing import Optional

# A small palette of weather‑related emojis.
EMOJI_MAP = [
    "☀️",  # sunny
    "🌤️",  # mostly sunny
    "⛅",   # partly cloudy
    "🌥️",  # mostly cloudy
    "☁️",  # cloudy
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "❄️",  # snow
    "🌪️",  # tornado
    "🌈",  # rainbow
]


def _seed_from_date(date_str: str) -> int:
    """Create a deterministic integer seed from an ISO‑date string.

    The function hashes the string with SHA‑256 and interprets the hex digest as an integer.
    """
    # Mock rationale: using a cryptographic hash guarantees the same output for the same input
    # without relying on external randomness sources.
    return int(hashlib.sha256(date_str.encode("utf-8")).hexdigest(), 16)


def get_forecast(date_str: Optional[str] = None) -> str:
    """Return a three‑emoji weather forecast for *date_str*.

    If *date_str* is ``None`` the current UTC date (``YYYY‑MM‑DD``) is used.
    The algorithm is deterministic: it derives a seed from the date and selects three emojis
    based on successive byte windows of that seed.
    """
    if date_str is None:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
    seed = _seed_from_date(date_str)
    emojis = []
    for i in range(3):
        # Shift by 8 bits per step to get a new byte window, then modulo the emoji list length.
        idx = (seed >> (i * 8)) % len(EMOJI_MAP)
        emojis.append(EMOJI_MAP[idx])
    return "".join(emojis)


if __name__ == "__main__":
    # Simple CLI for quick manual checks.
    print(get_forecast())
