"""
ASCII Clock Utility
"""

from datetime import datetime
from typing import List, Optional

# Simple 3x3 ASCII patterns for digits 0-9 and colon
_DIGIT_PATTERNS = {
    "0": [" _ ", "| |", "|_|"],
    "1": ["  |", "  |", "  |"],
    "2": [" _ ", " _|", "|_ "],
    "3": [" _ ", " _|", " _|"],
    "4": ["   ", "|_|", "  |"],
    "5": [" _ ", "|_ ", " _|"],
    "6": [" _ ", "|_ ", "|_|"],
    "7": [" _ ", "  |", "  |"],
    "8": [" _ ", "|_|", "|_|"],
    "9": [" _ ", "|_|", " _|"],
    ":": [" ", ".", " "]
}


def _render_time(dt: datetime) -> str:
    """Render a datetime as ASCII art HH:MM."""
    time_str = dt.strftime("%H:%M")
    rows: List[str] = ["", "", ""]
    for ch in time_str:
        pattern = _DIGIT_PATTERNS.get(ch)
        if pattern is None:
            raise ValueError(f"Unsupported character {ch!r} for ASCII clock")
        for i in range(3):
            rows[i] += pattern[i] + " "
    return "\n".join(row.rstrip() for row in rows)


def get_ascii_time(dt: Optional[datetime] = None) -> str:
    """Return the current (or supplied) time as ASCII art."""
    if dt is None:
        dt = datetime.now()
    return _render_time(dt)


if __name__ == "__main__":
    print(get_ascii_time())
