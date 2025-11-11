import datetime
import sys
from typing import List

# Mapping of each digit to its ASCII representation (5 rows high)
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


def ascii_digit(d: int) -> List[str]:
    """Return the 5‑row ASCII art for a single digit (0‑9)."""
    if 0 <= d <= 9:
        return _DIGIT_ART[d]
    raise ValueError(f"Invalid digit for ASCII art: {d}")


def ascii_time(dt: datetime.datetime) -> str:
    """Convert a datetime to a multi‑line ASCII‑art clock string.

    The format is HH:MM (24‑hour). The colon is represented by two centered dots.
    """
    hour = dt.hour
    minute = dt.minute
    digits = [hour // 10, hour % 10, minute // 10, minute % 10]
    rows: List[str] = ["" for _ in range(5)]
    for idx, d in enumerate(digits):
        art = ascii_digit(d)
        for r in range(5):
            rows[r] += art[r] + "  "  # spacing between digits
        # Insert colon after the hour digits
        if idx == 1:
            colon = ["   ", " • ", "   ", " • ", "   "]
            for r in range(5):
                rows[r] += colon[r] + "  "
    return "\n".join(row.rstrip() for row in rows)


def _main() -> None:
    now = datetime.datetime.now()
    print(ascii_time(now))


if __name__ == "__main__":
    _main()
