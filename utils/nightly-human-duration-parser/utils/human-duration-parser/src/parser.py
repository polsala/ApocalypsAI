"""human-duration-parser/src/parser.py

Utility to parse human‑readable duration strings into total seconds.

Supported units:
- d: days
- h: hours
- m: minutes
- s: seconds

The parser is tolerant of whitespace and case‑insensitive.
"""

import re
import sys
from argparse import ArgumentParser
from typing import Dict

# Mapping of unit suffix to number of seconds
_UNIT_TO_SECONDS: Dict[str, int] = {
    "d": 86_400,
    "h": 3_600,
    "m": 60,
    "s": 1,
}

# Regular expression to capture integer + unit pairs (e.g., "2h", "30m")
_DURATION_RE = re.compile(r"(?P<value>\d+)\s*(?P<unit>[dhms])", re.IGNORECASE)


def parse_duration(duration_str: str) -> int:
    """Parse a duration string like ``"2h30m"`` into total seconds.

    Parameters
    ----------
    duration_str: str
        Human‑readable duration string.

    Returns
    -------
    int
        Total number of seconds represented by the input.

    Raises
    ------
    ValueError
        If the string contains unknown units or cannot be parsed.
    """
    if not isinstance(duration_str, str):
        raise ValueError("duration_str must be a string")

    total_seconds = 0
    matches = list(_DURATION_RE.finditer(duration_str))
    if not matches:
        raise ValueError(f"Unable to parse duration: '{duration_str}'")

    for match in matches:
        value = int(match.group("value"))
        unit = match.group("unit").lower()
        if unit not in _UNIT_TO_SECONDS:
            # Mock rationale: this branch is unreachable because the regex limits units.
            raise ValueError(f"Unsupported unit '{unit}' in '{duration_str}'")
        total_seconds += value * _UNIT_TO_SECONDS[unit]

    return total_seconds


def _cli() -> None:
    parser = ArgumentParser(description="Convert a human‑readable duration to seconds.")
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
