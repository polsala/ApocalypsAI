#!/usr/bin/env python3
"""
Daily Whimsical Haiku utility.

Run as a module:
    python -m utils.daily-whimsical-haiku.src.haiku
or directly:
    python utils/daily-whimsical-haiku/src/haiku.py
"""

import datetime
import sys
from pathlib import Path

# Word banks – each list contains five options.
FIRST_LINE = [
    "Morning dew glistens",
    "Silent moon whispers",
    "Autumn leaves tumble",
    "Sunrise paints clouds",
    "Winter winds howl",
]

SECOND_LINE = [
    "over the quiet meadow",
    "through the ancient forest",
    "across the sleepy town",
    "beneath the starry sky",
    "within the hidden garden",
]

THIRD_LINE = [
    "dreams awaken anew.",
    "shadows dance softly.",
    "silence sings loudly.",
    "time folds into light.",
    "hope blooms forever.",
]


def _select_index(seed: int, length: int) -> int:
    """Return a deterministic index based on *seed* and list *length*.

    Simple modulo ensures the result is always in range ``0 <= idx < length``.
    """
    return seed % length


def generate_haiku(date: datetime.date | None = None) -> str:
    """Generate a deterministic haiku for *date*.

    If *date* is ``None`` the current local date is used.  The date is converted
    to an integer ``YYYYMMDD`` which seeds three independent selections from the
    word banks, guaranteeing the same poem for the same calendar day.
    """
    if date is None:
        date = datetime.date.today()
    seed = int(date.strftime("%Y%m%d"))

    idx1 = _select_index(seed, len(FIRST_LINE))
    idx2 = _select_index(seed + 1, len(SECOND_LINE))
    idx3 = _select_index(seed + 2, len(THIRD_LINE))

    line1 = FIRST_LINE[idx1]
    line2 = SECOND_LINE[idx2]
    line3 = THIRD_LINE[idx3]

    return f"{line1}\n{line2}\n{line3}"


def main() -> int:
    """CLI entry point – prints the haiku for today and exits with ``0``."""
    print(generate_haiku())
    return 0


if __name__ == "__main__":
    sys.exit(main())
