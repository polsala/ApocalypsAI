"""ascii_art_clock – Render the current time as ASCII art.

Provides:
- `render_time(dt: datetime) -> str` – Convert a datetime to ASCII digits.
- CLI entry point that prints the current local time.
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import List

# Mapping of each digit to a 5‑line ASCII representation.
_DIGIT_ART: List[List[str]] = [
    [" ███ ", "█   █", "█   █", "█   █", " ███ "],  # 0
    ["  █  ", " ██  ", "  █  ", "  █  ", " ███ "],  # 1
    [" ███ ", "    █", " ███ ", "█    ", " ███ "],  # 2
    [" ███ ", "    █", " ███ ", "    █", " ███ "],  # 3
    ["█   █", "█   █", " ███ ", "    █", "    █"],  # 4
    [" ███ ", "█    ", " ███ ", "    █", " ███ "],  # 5
    [" ███ ", "█    ", " ███ ", "█   █", " ███ "],  # 6
    [" ███ ", "    █", "   █ ", "  █  ", " █   "],  # 7
    [" ███ ", "█   █", " ███ ", "█   █", " ███ "],  # 8
    [" ███ ", "█   █", " ███ ", "    █", " ███ "],  # 9
]

_COLON_ART: List[str] = ["   ", " • ", "   ", " • ", "   "]


def _split_digits(time_str: str) -> List[str]:
    """Return a list of characters (digits or ':') from a HH:MM string."""
    return list(time_str)


def render_time(dt: datetime) -> str:
    """Render ``dt`` as a multi‑line ASCII clock.

    The output consists of 5 lines, each line containing the ASCII art for
    the hour and minute digits separated by a colon.
    """
    time_str = dt.strftime("%H:%M")  # e.g. "14:05"
    chars = _split_digits(time_str)

    # Build each of the 5 lines.
    lines: List[str] = ["" for _ in range(5)]
    for ch in chars:
        if ch == ":":
            art = _COLON_ART
        else:
            art = _DIGIT_ART[int(ch)]
        for i in range(5):
            # Add a space between symbols for readability.
            lines[i] += art[i] + "  "
    return "\n".join(line.rstrip() for line in lines)


def _cli() -> None:
    now = datetime.now()
    print(render_time(now))


if __name__ == "__main__":
    _cli()
