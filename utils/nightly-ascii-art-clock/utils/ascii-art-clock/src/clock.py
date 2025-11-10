"""ascii-art-clock – Render the current time as ASCII art.

Provides a `render_time` function and a small CLI for convenience.
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import List

# Mapping of each digit to a 5‑line ASCII representation.
_DIGITS: dict[str, List[str]] = {
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
        "█   █",
        "   █ ",
        "  █  ",
        "█████",
    ],
    "3": [
        "████ ",
        "    █",
        " ███ ",
        "    █",
        "████ ",
    ],
    "4": [
        "   ██",
        "  █ █",
        " █  █",
        "█████",
        "    █",
    ],
    "5": [
        "█████",
        "█    ",
        "████ ",
        "    █",
        "████ ",
    ],
    "6": [
        " ███ ",
        "█    ",
        "████ ",
        "█   █",
        " ███ ",
    ],
    "7": [
        "█████",
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
        " ████",
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


def _split_time(dt: datetime) -> str:
    """Return a HH:MM string from a datetime.

    The function always uses a 24‑hour clock and zero‑pads the hour and minute.
    """
    return dt.strftime("%H:%M")


def render_time(dt: datetime) -> str:
    """Render *dt* as multi‑line ASCII art.

    Parameters
    ----------
    dt: datetime
        The datetime to render.

    Returns
    -------
    str
        The ASCII art representation.
    """
    time_str = _split_time(dt)
    # Build each of the 5 lines by concatenating the corresponding slice of each character.
    lines: List[str] = ["" for _ in range(5)]
    for ch in time_str:
        digit_art = _DIGITS.get(ch)
        if digit_art is None:
            raise ValueError(f"Unsupported character in time string: {ch!r}")
        for i, segment in enumerate(digit_art):
            lines[i] += segment + "  "  # two spaces between characters for readability
    return "\n".join(lines)


def _parse_cli_arg(arg: str) -> datetime:
    """Parse a CLI argument into a datetime.

    Accepts ISO‑8601 strings (e.g., ``2025-12-31T23:59``) or ``HH:MM`` for today.
    """
    # Mock rationale: we keep parsing simple and avoid external deps.
    try:
        # Full datetime
        return datetime.fromisoformat(arg)
    except ValueError:
        # Assume HH:MM for today
        today = datetime.now()
        hour, minute = map(int, arg.split(":"))
        return today.replace(hour=hour, minute=minute, second=0, microsecond=0)


def main(argv: List[str] | None = None) -> None:
    """Entry point for the CLI.

    If an argument is supplied, it is interpreted as a datetime (ISO‑8601) or a ``HH:MM``
    string for the current day. Without arguments, the current system time is used.
    """
    argv = argv if argv is not None else sys.argv[1:]
    if argv:
        dt = _parse_cli_arg(argv[0])
    else:
        dt = datetime.now()
    print(render_time(dt))


if __name__ == "__main__":
    main()
