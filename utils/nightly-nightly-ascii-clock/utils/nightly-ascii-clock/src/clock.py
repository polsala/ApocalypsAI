"""ascii_clock
================
Utility that prints the current local time as ASCII art.

Running the module directly prints the time, e.g.:

    $ python -m utils.nightly_ascii_clock.src.clock
    12:34
    ┌─┐ ┌─┐ ─ ┌─┐ ┌─┐
    │ │ │ │   │ │ │
    └─┘ └─┘   └─┘ └─┘
"""

from __future__ import annotations

import datetime
import sys
from typing import List

# Simple 3‑row representation for digits 0‑9 and colon.
_DIGITS: dict[str, List[str]] = {
    "0": [" ┌─┐ ", " │ │ ", " └─┘ "],
    "1": ["  ┐  ", "  │  ", " ─┘  "],
    "2": [" ┌─┐ ", " ──┐ ", " └─┘ "],
    "3": [" ┌─┐ ", " ──┐ ", " ──┘ "],
    "4": [" ┐ ┐ ", " └─┘ ", "   │ "],
    "5": [" ┌─┐ ", " └─┐ ", " ──┘ "],
    "6": [" ┌─┐ ", " └─┐ ", " └─┘ "],
    "7": [" ──┐ ", "   │ ", "   │ "],
    "8": [" ┌─┐ ", " ├─┤ ", " └─┘ "],
    "9": [" ┌─┐ ", " └─┤ ", " ──┘ "],
    ":": ["   ", " • ", " • "],
}


def _render_time(dt: datetime.time) -> str:
    """Return a multi‑line string with the time rendered as ASCII art.

    The format is always ``HH:MM`` with leading zeros.
    """
    time_str = dt.strftime("%H:%M")
    rows: List[str] = ["" for _ in range(3)]
    for ch in time_str:
        glyph = _DIGITS.get(ch)
        if glyph is None:
            raise ValueError(f"Unsupported character in time string: {ch!r}")
        for i in range(3):
            rows[i] += glyph[i]
    return "\n".join(rows)


def main() -> None:
    now = datetime.datetime.now().time()
    ascii_time = _render_time(now)
    # Print a simple header with the numeric time for quick glance.
    print(now.strftime("%H:%M"))
    print(ascii_time)


if __name__ == "__main__":
    # When executed as a script, run the CLI.
    try:
        main()
    except Exception as exc:  # pragma: no cover – defensive
        sys.stderr.write(f"Error: {exc}\n")
        sys.exit(1)
