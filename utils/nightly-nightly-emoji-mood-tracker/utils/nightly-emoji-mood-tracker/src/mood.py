"""emoji_mood_tracker
=====================

Provides a deterministic mapping from a date to an emoji representing the day's mood.

The algorithm:
1. Convert the date to its ISO string (YYYY‑MM‑DD).
2. Compute a simple stable hash using `hashlib.sha256`.
3. Use the hash to index into a fixed list of emojis.

The function is pure and side‑effect free, making it trivial to test.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
from typing import List

# A curated list of emojis covering a range of moods.
EMOJI_PALETTE: List[str] = [
    "😀",  # happy
    "😐",  # neutral
    "😔",  # sad
    "🤖",  # robotic (techy day)
    "🚀",  # launch day
    "🌧️",  # rainy mood
    "☀️",  # sunny optimism
    "🧩",  # puzzling day
    "🔥",  # fiery energy
    "🛠️",  # productive / fixing
]


def _stable_hash(value: str) -> int:
    """Return a deterministic integer hash for *value*.

    Uses SHA‑256 and converts the first 8 bytes to an int.
    """
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    # Take first 8 bytes for a 64‑bit integer.
    return int.from_bytes(digest[:8], "big")


def mood_for_date(date: datetime.date) -> str:
    """Return an emoji representing the mood for *date*.

    The mapping is deterministic: the same date always yields the same emoji.
    """
    iso = date.isoformat()
    h = _stable_hash(iso)
    index = h % len(EMOJI_PALETTE)
    return EMOJI_PALETTE[index]


def main() -> None:
    parser = argparse.ArgumentParser(description="Get an emoji mood for a given date.")
    parser.add_argument(
        "date",
        nargs="?",
        default=None,
        help="Date in YYYY-MM-DD format. Defaults to today.",
    )
    args = parser.parse_args()

    if args.date:
        try:
            target_date = datetime.date.fromisoformat(args.date)
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {args.date}") from exc
    else:
        target_date = datetime.date.today()

    print(mood_for_date(target_date))


if __name__ == "__main__":
    main()
