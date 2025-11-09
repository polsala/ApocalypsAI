"""ascii_clock
================
Utility that renders the current local time as ASCII art.

The implementation is deliberately simple and self‑contained – it only
relies on the Python standard library.
"""

from __future__ import annotations

import datetime
from typing import List

# Mapping of each digit to a 3‑line ASCII representation.
_DIGIT_ART: dict[str, List[str]] = {
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


def _render_digit(d: str) -> List[str]:
    """Return the 3‑line ASCII art for a single character.

    Parameters
    ----------
    d: str
        A single character – one of ``0‑9`` or ``:``.
    """
    return _DIGIT_ART.get(d, ["   ", "   ", "   "])


def get_ascii_time(dt: datetime.time | datetime.datetime) -> str:
    """Return the time formatted as ASCII art.

    The function accepts either a ``datetime.time`` or ``datetime.datetime``
    instance.  Seconds are omitted for brevity.
    """
    if isinstance(dt, datetime.datetime):
        t = dt.time()
    else:
        t = dt
    # Format as HH:MM using zero‑padding.
    time_str = f"{t.hour:02d}:{t.minute:02d}"
    # Build three output lines.
    lines = ["" for _ in range(3)]
    for ch in time_str:
        art = _render_digit(ch)
        for i in range(3):
            lines[i] += art[i] + " "
    # Trim trailing space.
    return "\n".join(line.rstrip() for line in lines)


def main() -> None:
    """CLI entry point – prints the current local time as ASCII art."""
    now = datetime.datetime.now()
    print(get_ascii_time(now))


if __name__ == "__main__":
    main()
