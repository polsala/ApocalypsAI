"""duration_parser.py

Parse human‑readable duration strings into total seconds.

Supported units (case‑insensitive):
- d – days
- h – hours
- m – minutes
- s – seconds

The parser tolerates whitespace and any order of units.
"""

import re
import sys
from argparse import ArgumentParser
from typing import Dict

_UNIT_SECONDS: Dict[str, int] = {
    "d": 86_400,
    "h": 3_600,
    "m": 60,
    "s": 1,
}

_PATTERN = re.compile(r"(?P<value>\d+)\s*(?P<unit>[dhms])", re.IGNORECASE)


def parse_duration(duration_str: str) -> int:
    """Convert a duration string like ``"2h30m"`` to total seconds.

    Args:
        duration_str: Human‑readable duration.

    Returns:
        Total seconds as an ``int``.

    Raises:
        ValueError: If the string contains no recognizable units.
    """
    total = 0
    matches = list(_PATTERN.finditer(duration_str))
    if not matches:
        raise ValueError(f"No valid duration components found in '{duration_str}'.")
    for match in matches:
        value = int(match.group("value"))
        unit = match.group("unit").lower()
        total += value * _UNIT_SECONDS[unit]
    return total


def _cli() -> None:
    parser = ArgumentParser(description="Convert human‑readable duration strings to seconds.")
    parser.add_argument("duration", help="Duration string, e.g., '2h30m' or '1d 4h'.")
    args = parser.parse_args()
    try:
        seconds = parse_duration(args.duration)
        print(seconds)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
