"""human-duration-parser

Utility to parse strings like "2h30m" into total seconds.

Supported units:
- d: days (24 * 60 * 60)
- h: hours (60 * 60)
- m: minutes (60)
- s: seconds

The parser is order‑agnostic and tolerant of whitespace.
"""

import re
import sys
from argparse import ArgumentParser
from typing import Dict

_UNIT_SECONDS: Dict[str, int] = {
    "d": 86400,
    "h": 3600,
    "m": 60,
    "s": 1,
}

_DURATION_RE = re.compile(r"(?P<value>\d+)(?P<unit>[dhms])", re.IGNORECASE)


def parse_duration(duration_str: str) -> int:
    """Parse a human‑readable duration string into total seconds.

    Args:
        duration_str: String like "2h30m" or "1d 4h 5s".

    Returns:
        Total number of seconds as an integer.

    Raises:
        ValueError: If the string contains unknown units or malformed parts.
    """
    if not isinstance(duration_str, str):
        raise ValueError("duration_str must be a string")

    total_seconds = 0
    matches = list(_DURATION_RE.finditer(duration_str.replace(" ", "")))
    if not matches:
        raise ValueError(f"No valid duration components found in '{duration_str}'")

    consumed = 0
    for match in matches:
        value = int(match.group("value"))
        unit = match.group("unit").lower()
        if unit not in _UNIT_SECONDS:
            raise ValueError(f"Unsupported unit '{unit}' in '{duration_str}'")
        total_seconds += value * _UNIT_SECONDS[unit]
        consumed += len(match.group(0))

    # Ensure the whole string was consumed (ignoring whitespace)
    if consumed != len(duration_str.replace(" ", "")):
        raise ValueError(f"Malformed duration string '{duration_str}'")

    return total_seconds


def _cli() -> None:
    parser = ArgumentParser(description="Convert human‑readable duration strings to seconds.")
    parser.add_argument("duration", help="Duration string, e.g., '2h30m'")
    args = parser.parse_args()
    try:
        seconds = parse_duration(args.duration)
        print(seconds)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
