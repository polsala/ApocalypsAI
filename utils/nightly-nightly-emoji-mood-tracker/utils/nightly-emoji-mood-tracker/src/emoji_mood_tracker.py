"""emoji_mood_tracker.py

A tiny utility that maps a date to a mood emoji.

Public API:
    get_mood(date_str: str) -> str
        Returns an emoji representing the mood for the supplied ISO‑date string.

CLI usage:
    python -m src.emoji_mood_tracker <date>
"""

from __future__ import annotations

import argparse
import datetime
import sys
from typing import List

# Fixed list of emojis – order matters for deterministic indexing
EMOJIS: List[str] = [
    "😀",  # happy
    "😐",  # neutral
    "😔",  # sad
    "🤔",  # thoughtful
    "🤩",  # excited
    "😎",  # cool
    "🙃",  # playful
    "🥳",  # celebratory
    "😴",  # sleepy
    "🤖",  # robotic
]


def _date_to_int(date_str: str) -> int:
    """Convert an ISO‑date string (YYYY‑MM‑DD) to an integer YYYYMMDD.

    Raises:
        ValueError: If the string is not a valid date.
    """
    # Validate date format using datetime
    try:
        datetime.date.fromisoformat(date_str)
    except Exception as exc:
        raise ValueError(f"Invalid ISO date '{date_str}': {exc}") from exc
    return int(date_str.replace("-", ""))


def get_mood(date_str: str) -> str:
    """Return a deterministic mood emoji for *date_str*.

    The algorithm is deliberately simple and offline‑only:
        1. Convert the date to an integer (YYYYMMDD).
        2. Add the weekday number (Monday=0 … Sunday=6).
        3. Modulo the length of :data:`EMOJIS` to obtain an index.
        4. Return the emoji at that index.
    """
    date_int = _date_to_int(date_str)
    weekday = datetime.date.fromisoformat(date_str).weekday()
    index = (date_int + weekday) % len(EMOJIS)
    return EMOJIS[index]


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Map a date to a mood emoji.")
    parser.add_argument("date", help="Date in ISO format (YYYY-MM-DD)")
    args = parser.parse_args()
    try:
        emoji = get_mood(args.date)
        print(emoji)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
