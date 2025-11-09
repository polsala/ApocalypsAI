"""
ASCII Clock utility.
Provides `get_ascii_time(dt)` to convert a datetime to ASCII art.
When executed as a script, prints the current local time.
"""

import datetime
from typing import List

# 5‑line block representation for each digit (width = 5 characters)
DIGITS = {
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
        " █   ",
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
}

SEPARATOR = "  "  # two spaces between digits


def _digit_lines(d: str) -> List[str]:
    """Return the 5‑line block for a single digit character."""
    return DIGITS[d]


def get_ascii_time(dt: datetime.datetime) -> str:
    """Return an ASCII‑art representation of the time ``HH:MM`` (24‑hour).

    The function formats the hour and minute with leading zeros, builds a
    four‑character string (e.g. ``"1305"``) and concatenates the corresponding
    digit blocks.
    """
    hour = dt.hour
    minute = dt.minute
    time_str = f"{hour:02d}{minute:02d}"  # e.g. "1305"

    # Initialise five empty rows
    rows = ["" for _ in range(5)]

    for idx, ch in enumerate(time_str):
        digit_block = _digit_lines(ch)
        for r in range(5):
            rows[r] += digit_block[r]
            # Add separator unless this is the last digit
            if idx != len(time_str) - 1:
                rows[r] += SEPARATOR
    return "\n".join(rows)


def main() -> None:
    now = datetime.datetime.now()
    print(get_ascii_time(now))


if __name__ == "__main__":
    main()
