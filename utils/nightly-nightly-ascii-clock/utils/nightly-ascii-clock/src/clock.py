"""ascii_clock
================
Utility that prints the current local time as ASCII‑art digits.

The implementation is deliberately simple and has **no third‑party
dependencies** – only the Python standard library.
"""

import datetime
import sys
from typing import List

# Mapping of each digit to its 3‑line ASCII representation.
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


def _render_time(time_str: str) -> str:
    """Convert a time string like ``"12:34"`` into stacked ASCII art.

    Returns a single string with newline characters separating the three rows.
    """
    rows = ["", "", ""]
    for ch in time_str:
        art = _DIGIT_ART.get(ch, ["   ", "   ", "   "])
        for i in range(3):
            rows[i] += art[i] + " "
    return "\n".join(row.rstrip() for row in rows)


def get_current_time_ascii() -> str:
    """Return the current local time formatted as ``HH:MM`` ASCII art.

    The function is isolated for easy testing – it can be monkey‑patched
    to return a deterministic value.
    """
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M")
    return _render_time(time_str)


def main(argv: List[str] | None = None) -> int:
    """Entry‑point for the ``python -m src.clock`` command.

    Prints the ASCII clock to ``stdout`` and returns an exit code.
    """
    ascii_time = get_current_time_ascii()
    print(ascii_time)
    return 0


if __name__ == "__main__":
    sys.exit(main())
