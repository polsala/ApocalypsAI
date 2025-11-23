import sys
import hashlib
from datetime import datetime, date
from typing import List

# Fixed palette of emojis representing daily moods
EMOJIS: List[str] = [
    "😀",  # Happy
    "😐",  # Neutral
    "😢",  # Sad
    "🤔",  # Thoughtful
    "🔥",  # Fiery
    "🌧️",  # Rainy
    "🌟",  # Starry
    "🌀",  # Whirlwind
    "🦄",  # Magical
    "🚀",  # Rocket
]


def _hash_date(d: date) -> int:
    """Return a deterministic integer hash for *d*.

    The hash is based on SHA‑256 of the ISO‑format string, converted to an int.
    """
    iso = d.isoformat()
    digest = hashlib.sha256(iso.encode("utf-8")).hexdigest()
    return int(digest, 16)


def get_mood(d: date) -> str:
    """Return an emoji representing the mood for the given *date*.

    The function is pure and deterministic – the same *date* always yields the same emoji.
    """
    idx = _hash_date(d) % len(EMOJIS)
    return EMOJIS[idx]


def _parse_cli_arg(arg: str) -> date:
    """Parse a CLI argument into a :class:`datetime.date`.

    Accepts ISO‑format ``YYYY-MM-DD`` strings. Raises ``ValueError`` on failure.
    """
    return datetime.strptime(arg, "%Y-%m-%d").date()


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m utils.nightly-emoji-mood-meter.src.mood_meter <YYYY-MM-DD>")
        sys.exit(1)
    try:
        target_date = _parse_cli_arg(sys.argv[1])
    except ValueError as e:
        print(f"Invalid date format: {e}")
        sys.exit(1)
    print(get_mood(target_date))


if __name__ == "__main__":
    main()
