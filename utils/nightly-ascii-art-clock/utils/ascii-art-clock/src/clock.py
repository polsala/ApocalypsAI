"""ascii_art_clock – render the current time as 7‑segment ASCII art.

Public API
-----------
- ``render_time(dt: datetime.datetime) -> str`` – Return the ASCII art for the
  hour and minute of ``dt`` (format HH:MM).
- ``main()`` – CLI entry point that prints ``render_time(datetime.now())``.
"""

from __future__ import annotations

import datetime
import sys
from typing import List

# Mapping of each digit to its 3‑row 7‑segment representation.
_DIGIT_MAP: dict[str, List[str]] = {
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
    ":": ["   ", " . ", " . "],
}


def _split_time(dt: datetime.datetime) -> List[str]:
    """Return a list of characters representing HH:MM (24‑hour clock)."""
    return list(dt.strftime("%H:%M"))


def render_time(dt: datetime.datetime) -> str:
    """Render ``dt`` as three rows of ASCII‑art 7‑segment digits.

    Parameters
    ----------
    dt: datetime.datetime
        The datetime to render. Only hour and minute are used.

    Returns
    -------
    str
        Multi‑line string containing the ASCII art.
    """
    chars = _split_time(dt)
    rows = ["" for _ in range(3)]
    for ch in chars:
        seg = _DIGIT_MAP.get(ch)
        if seg is None:
            raise ValueError(f"Unsupported character for ASCII art: {ch!r}")
        for i in range(3):
            rows[i] += seg[i] + " "  # space between digits
    return "\n".join(row.rstrip() for row in rows)


def main(argv: List[str] | None = None) -> None:
    """CLI entry point.

    Prints the current local time in ASCII art to stdout.
    """
    now = datetime.datetime.now()
    ascii_time = render_time(now)
    print(ascii_time)


if __name__ == "__main__":
    main()
