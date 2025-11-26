'''Emoji Mood Generator utility.

Provides a deterministic mapping from a date to a mood emoji.
''' 

import sys
import hashlib
from datetime import datetime, date
from typing import List

EMOJIS: List[str] = [
    "😀", "😐", "😔", "🤔", "😎", "🤩", "😴", "😡", "🤯", "🥳"
]


def _hash_date(d: date) -> int:
    """Return an integer hash for the given date."""
    h = hashlib.sha256(d.isoformat().encode()).hexdigest()
    return int(h, 16)


def get_mood(d: date) -> str:
    """Return a deterministic mood emoji for the given date."""
    idx = _hash_date(d) % len(EMOJIS)
    return EMOJIS[idx]


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Optional list of arguments (excluding script name).

    Returns:
        Exit code (0 on success, 1 on error).
    """
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) == 0:
        target_date = date.today()
    else:
        try:
            target_date = datetime.strptime(argv[0], "%Y-%m-%d").date()
        except ValueError:
            print("Error: date must be in YYYY-MM-DD format", file=sys.stderr)
            return 1

    emoji = get_mood(target_date)
    print(emoji)
    return 0


if __name__ == "__main__":
    sys.exit(main())
