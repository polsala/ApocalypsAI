"""daily_emoji_rotator – deterministic emoji of the day.

Provides:
- ``get_today_emoji()`` – returns the emoji for the current local date.
- ``get_emoji_for_date(date_obj)`` – pure function useful for testing.
- CLI entry‑point when the module is executed as ``__main__``.
"""

from __future__ import annotations

import datetime
import hashlib
from typing import List

# A curated list of emojis – feel free to extend.
EMOJI_LIST: List[str] = [
    "😀", "🚀", "🌟", "🍕", "🐍", "📚", "🎉", "🧩", "⚡", "🌈",
    "🦄", "💡", "🔧", "🗺️", "🎈", "🕶️", "🍀", "☕", "📅", "🧭",
]


def _hash_date(date_str: str) -> int:
    """Return an integer hash for a given ISO‑format date string.

    The hash is stable across Python versions because we use SHA‑256.
    """
    # Mock rationale: Using SHA‑256 ensures deterministic, uniform distribution.
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    return int(digest, 16)


def get_emoji_for_date(date_obj: datetime.date) -> str:
    """Return the emoji associated with *date_obj*.

    The function is pure and deterministic – ideal for unit testing.
    """
    iso = date_obj.isoformat()  # e.g., "2025-11-12"
    hash_int = _hash_date(iso)
    index = hash_int % len(EMOJI_LIST)
    return EMOJI_LIST[index]


def get_today_emoji() -> str:
    """Convenience wrapper that uses ``datetime.date.today()``.
    """
    today = datetime.date.today()
    return get_emoji_for_date(today)


if __name__ == "__main__":
    # Simple CLI: print the emoji for today.
    print(get_today_emoji())
