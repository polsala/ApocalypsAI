import sys
import datetime
from typing import List

# Mapping of each digit to a 3‑line ASCII representation
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


def _split_time(dt: datetime.datetime) -> str:
    """Return a HH:MM:SS string from a datetime object."""
    return dt.strftime("%H:%M:%S")


def render_time(dt: datetime.datetime) -> str:
    """Render *dt* as multi‑line ASCII art.

    The function builds three output lines by concatenating the corresponding
    slice of each character's art representation.
    """
    time_str = _split_time(dt)
    # Prepare three empty lines
    lines = ["" for _ in range(3)]
    for ch in time_str:
        art = _DIGIT_ART.get(ch)
        if art is None:
            raise ValueError(f"Unsupported character in time string: {ch}")
        for i in range(3):
            lines[i] += art[i] + " "  # add a space between characters
    return "\n".join(line.rstrip() for line in lines)


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Prints the current local time as ASCII art to stdout.
    Returns exit code 0 on success.
    """
    now = datetime.datetime.now()
    ascii_time = render_time(now)
    print(ascii_time)
    return 0


if __name__ == "__main__":
    sys.exit(main())
