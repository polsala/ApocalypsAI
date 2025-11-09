"""ascii_clock
================
Utility that renders the current time (or any ``datetime``) as large ASCII‑art digits.

The module provides two public callables:

* ``get_ascii_time(dt: datetime.datetime) -> str`` – returns the ASCII art string.
* ``main()`` – CLI entry point that prints the current local time.
"""

from __future__ import annotations

import datetime
import sys
from typing import Dict, List

# Mapping of each digit to a 5‑line ASCII representation.
_DIGIT_ART: Dict[str, List[str]] = {
    "0": [
        " ███ ",
        "█   █",
        "█   █",
        "█   █",
        " ███ ",
    ],
    "1": [
        "  █  ",
        " ██  ",
        "  █  ",
        "  █  ",
        " ███ ",
    ],
    "2": [
        " ███ ",
        "    █",
        " ███ ",
        "█    ",
        " ███ ",
    ],
    "3": [
        " ███ ",
        "    █",
        " ███ ",
        "    █",
        " ███ ",
    ],
    "4": [
        "█   █",
        "█   █",
        " ███ ",
        "    █",
        "    █",
    ],
    "5": [
        " ███ ",
        "█    ",
        " ███ ",
        "    █",
        " ███ ",
    ],
    "6": [
        " ███ ",
        "█    ",
        " ███ ",
        "█   █",
        " ███ ",
    ],
    "7": [
        " ███ ",
        "    █",
        "   █ ",
        "  █  ",
        "  █  ",
    ],
    "8": [
        " ███ ",
        "█   █",
        " ███ ",
        "█   █",
        " ███ ",
    ],
    "9": [
        " ███ ",
        "█   █",
        " ███ ",
        "    █",
        " ███ ",
    ],
    ":": [
        "     ",
        "  ░  ",
        "     ",
        "  ░  ",
        "     ",
    ],
}


def _render_time_str(time_str: str) -> str:
    """Convert a string like ``12:34`` into stacked ASCII art.

    Parameters
    ----------
    time_str: str
        The time string consisting of digits and a colon.
    """
    lines: List[str] = ["" for _ in range(5)]
    for ch in time_str:
        art = _DIGIT_ART.get(ch)
        if art is None:
            raise ValueError(f"Unsupported character in time string: {ch!r}")
        for i, line in enumerate(art):
            lines[i] += line + "  "  # two spaces between characters
    return "\n".join(lines)


def get_ascii_time(dt: datetime.datetime) -> str:
    """Return the ASCII‑art representation of ``dt``'s hour and minute.

    The function formats the time as ``HH:MM`` (24‑hour clock) and then
    renders each character using the predefined ``_DIGIT_ART`` mapping.
    """
    time_str = dt.strftime("%H:%M")
    return _render_time_str(time_str)


def main(argv: List[str] | None = None) -> None:
    """CLI entry point.

    Prints the current local time in ASCII art to ``stdout``.
    """
    if argv is None:
        argv = sys.argv[1:]
    # No arguments are currently used; placeholder for future extensions.
    now = datetime.datetime.now()
    ascii_time = get_ascii_time(now)
    print(ascii_time)


if __name__ == "__main__":
    main()
