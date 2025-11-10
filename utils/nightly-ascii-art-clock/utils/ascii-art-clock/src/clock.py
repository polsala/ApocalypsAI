"""ascii_art_clock – Render a time as compact ASCII art.

Provides:
- `DIGITS`: mapping of characters to 3‑row bitmap strings.
- `render_time(dt: datetime) -> str`: returns a three‑line string.
- CLI entry point that prints the current local time.
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import List, Mapping

# 3×3 patterns for digits and colon (using a centered dot for the colon)
DIGITS: Mapping[str, List[str]] = {
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
    ":": ["   ", " · ", "   "],
}


def _split_time(dt: datetime) -> List[str]:
    """Return a list of characters representing HH:MM:SS.

    Each component is zero‑padded to two digits.
    """
    return [
        f"{dt.hour:02d}"[0],
        f"{dt.hour:02d}"[1],
        ":",
        f"{dt.minute:02d}"[0],
        f"{dt.minute:02d}"[1],
        ":",
        f"{dt.second:02d}"[0],
        f"{dt.second:02d}"[1],
    ]


def render_time(dt: datetime) -> str:
    """Render *dt* as three lines of ASCII art.

    The function is pure and deterministic – perfect for unit testing.
    """
    chars = _split_time(dt)
    rows: List[str] = ["" for _ in range(3)]
    for idx, ch in enumerate(chars):
        pattern = DIGITS.get(ch)
        if pattern is None:
            raise ValueError(f"Unsupported character for ASCII clock: {ch!r}")
        for r in range(3):
            # Add a space separator between symbols (except before the first one)
            if idx > 0:
                rows[r] += " "
            rows[r] += pattern[r]
    return "\n".join(rows)


def _cli() -> None:
    now = datetime.now()
    print(render_time(now))


if __name__ == "__main__":
    _cli()
