"""nightly_ascii_clock – Render time as ASCII art.

Provides a CLI entry‑point and a library function `get_ascii_time`.
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import List

# Simple 7‑segment style patterns for digits 0‑9
_DIGIT_PATTERNS: List[List[str]] = [
    [" _ ", "| |", "|_|"],  # 0
    ["   ", "  |", "  |"],  # 1
    [" _ ", " _|", "|_ "],  # 2
    [" _ ", " _|", " _|"],  # 3
    ["   ", "|_|", "  |"],  # 4
    [" _ ", "|_ ", " _|"],  # 5
    [" _ ", "|_ ", "|_|"],  # 6
    [" _ ", "  |", "  |"],  # 7
    [" _ ", "|_|", "|_|"],  # 8
    [" _ ", "|_|", " _|"],  # 9
]

_COLON_PATTERN = ["   ", " . ", " . "]


def _render_char(ch: str) -> List[str]:
    """Return the three‑line ASCII representation for a single character.

    Supports digits 0‑9 and ':' (colon). Raises ValueError for others.
    """
    if ch.isdigit():
        return _DIGIT_PATTERNS[int(ch)]
    if ch == ":":
        return _COLON_PATTERN
    raise ValueError(f"Unsupported character for ASCII clock: {ch!r}")


def get_ascii_time(dt: datetime) -> str:
    """Return a multi‑line string rendering ``dt`` as HH:MM in ASCII art.

    The output consists of three lines, each ending with a newline character.
    """
    time_str = dt.strftime("%H:%M")
    # Build three lines by concatenating the patterns for each character
    lines = ["" for _ in range(3)]
    for ch in time_str:
        pattern = _render_char(ch)
        for i in range(3):
            lines[i] += pattern[i]
    # Join lines with newline characters
    return "\n".join(lines) + "\n"


def _cli() -> None:
    """CLI entry‑point: print the current local time as ASCII art."""
    now = datetime.now()
    ascii_time = get_ascii_time(now)
    sys.stdout.write(ascii_time)


if __name__ == "__main__":
    _cli()
