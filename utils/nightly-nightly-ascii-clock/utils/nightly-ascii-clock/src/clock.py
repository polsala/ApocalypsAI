"""ascii‑clock utility

Prints the current local time as large ASCII‑art digits.

Usage:
    python -m src.clock          # prints the time to stdout
    from src.clock import get_ascii_time
    print(get_ascii_time(datetime.datetime(2023, 1, 1, 12, 34)))
"""

import argparse
import datetime
import sys
from typing import Dict, List

# Mapping of each digit to a 3‑line ASCII representation
_DIGIT_ART: Dict[str, List[str]] = {
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
    """Convert a time string like ``"14:35"`` into multi‑line ASCII art.

    The function builds the output line‑by‑line, concatenating the corresponding
    art for each character.
    """
    lines = ["", "", ""]
    for ch in time_str:
        art = _DIGIT_ART.get(ch)
        if not art:
            raise ValueError(f"Unsupported character in time string: {ch!r}")
        for i in range(3):
            lines[i] += art[i] + " "  # space between characters
    return "\n".join(line.rstrip() for line in lines)


def get_ascii_time(dt: datetime.datetime) -> str:
    """Return the ASCII‑art representation of ``dt``'s hour and minute.

    Parameters
    ----------
    dt: datetime.datetime
        The datetime object to render.

    Returns
    -------
    str
        Multi‑line ASCII art of the time in ``HH:MM`` 24‑hour format.
    """
    time_str = dt.strftime("%H:%M")
    return _render_time(time_str)


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print the current time as ASCII art.")
    parser.add_argument(
        "--format",
        choices=["24", "12"],
        default="24",
        help="Display time in 24‑hour (default) or 12‑hour format.",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = _parse_args(argv)
    now = datetime.datetime.now()
    if args.format == "12":
        now = now.strftime("%I:%M %p")  # e.g., "02:35 PM"
        # Strip the AM/PM for ASCII rendering; keep hour/minute only.
        now = datetime.datetime.strptime(now, "%I:%M %p")
    ascii_time = get_ascii_time(now)
    print(ascii_time)
    return 0


if __name__ == "__main__":
    sys.exit(main())
