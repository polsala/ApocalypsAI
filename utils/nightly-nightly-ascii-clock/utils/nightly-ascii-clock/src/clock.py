"""nightly-ascii-clock – print the current time as ASCII art.

This module provides a single public function ``ascii_time`` that converts a
``datetime`` instance into a three‑line string where each digit is rendered using
a simple 3×3 block pattern. The module also offers a ``main`` entry‑point for CLI
usage.
"""

from __future__ import annotations

import datetime
import sys
from typing import List

# 3‑row patterns for digits 0‑9 and colon. Each row is a string of length 3.
_DIGIT_PATTERNS = {
    "0": [" _ ", "| |", "|_|"],
    "1": ["   ", "  |", "  |"],
    "2": [" _ ", " _|", "|_ "],
    "3": [" _ ", " _|", " _|"],
    "4": ["   ", "|_|", "  |"],
    "5": [" _ ", "|_ ", " _|"],
    "6": [" _ ", "|_ ", "|_|"],
    "7": [" _ ", "  |", "  |"],
    "8": [" _ ", "|_|", "|_|"],
    "9": [" _ ", "|_|", " _|"],
    ":": ["   ", " . ", " . "]
}


def _split_time_str(time_str: str) -> List[str]:
    """Return a list of characters (digits or ':') from a HH:MM string.

    Args:
        time_str: A string formatted as ``HH:MM``.
    """
    return list(time_str)


def ascii_time(dt: datetime.datetime) -> str:
    """Convert a ``datetime`` object to a three‑line ASCII‑art representation.

    The function extracts the hour and minute in 24‑hour format, builds the
    corresponding pattern rows for each character, and joins them with a single
    space between characters.

    Args:
        dt: ``datetime.datetime`` instance (timezone‑aware or naive).

    Returns:
        A string containing three lines separated by ``\n``.
    """
    time_str = dt.strftime("%H:%M")
    chars = _split_time_str(time_str)

    # Build each of the three rows.
    rows = ["" for _ in range(3)]
    for ch in chars:
        pattern = _DIGIT_PATTERNS.get(ch)
        if pattern is None:
            raise ValueError(f"Unsupported character in time string: {ch!r}")
        for i in range(3):
            # Add a space separator except before the first character.
            if rows[i]:
                rows[i] += " "
            rows[i] += pattern[i]
    return "\n".join(rows)


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Prints the current local time as ASCII art to ``stdout``.
    Returns ``0`` on success.
    """
    now = datetime.datetime.now()
    print(ascii_time(now))
    return 0


if __name__ == "__main__":
    sys.exit(main())
