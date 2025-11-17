import sys
import hashlib
from datetime import datetime
from typing import List

EMOJIS: List[str] = [
    "☀️", "🌧️", "⛈️", "❄️", "🌪️", "🌈", "☁️", "🌤️", "🌙", "⭐️",
    "🔥", "💧", "🍀", "🍂", "🎉", "🎃", "🎄", "🚀", "🧩", "🤖"
]


def _hash_date(date_str: str) -> int:
    """Return an integer hash for a given ISO date string."""
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    return int(digest, 16)


def get_emoji_for_date(date_str: str) -> str:
    """Return a deterministic emoji for the supplied ISO date string (YYYY-MM-DD).

    Raises:
        ValueError: If the date string is not a valid ISO date.
    """
    # Validate date format – will raise ValueError if invalid
    datetime.strptime(date_str, "%Y-%m-%d")
    hash_int = _hash_date(date_str)
    index = hash_int % len(EMOJIS)
    return EMOJIS[index]


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m forecast <YYYY-MM-DD>")
        sys.exit(1)
    date_input = sys.argv[1]
    try:
        emoji = get_emoji_for_date(date_input)
        print(emoji)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    _cli()
