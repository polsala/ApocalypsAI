"""utils/nightly-duration-parser/src/parser.py

Utility functions for parsing and formatting human‑friendly duration strings.
Supported units (case‑insensitive):
- d : days
- h : hours
- m : minutes
- s : seconds

Examples
--------
>>> parse_duration("2h 30m")
9000
>>> format_duration(9000)
'2h 30m'
"""

import re
from typing import Dict

# Mapping of unit suffix to number of seconds
_UNIT_SECONDS: Dict[str, int] = {
    "d": 86_400,
    "h": 3_600,
    "m": 60,
    "s": 1,
}

_DURATION_RE = re.compile(r"(?P<value>\d+)(?P<unit>[dhms])", re.IGNORECASE)


def parse_duration(duration_str: str) -> int:
    """Parse a duration string into total seconds.

    Parameters
    ----------
    duration_str: str
        Human‑readable duration, e.g. "2h30m", "1d 4h", "45m".

    Returns
    -------
    int
        Total number of seconds represented by the string.

    Raises
    ------
    ValueError
        If the string contains unknown units or malformed parts.
    """
    if not isinstance(duration_str, str):
        raise ValueError("duration_str must be a string")

    total_seconds = 0
    # Remove whitespace for easier matching
    cleaned = duration_str.replace(" ", "")
    if not cleaned:
        raise ValueError("Empty duration string")

    pos = 0
    while pos < len(cleaned):
        match = _DURATION_RE.match(cleaned, pos)
        if not match:
            raise ValueError(f"Invalid duration segment at position {pos}: '{cleaned[pos:]}'")
        value = int(match.group("value"))
        unit = match.group("unit").lower()
        if unit not in _UNIT_SECONDS:
            raise ValueError(f"Unsupported time unit: '{unit}'")
        total_seconds += value * _UNIT_SECONDS[unit]
        pos = match.end()
    return total_seconds


def format_duration(seconds: int) -> str:
    """Format a number of seconds into a compact duration string.

    The output includes only the largest non‑zero units in descending order
    (days, hours, minutes, seconds). Units with a value of zero are omitted.

    Parameters
    ----------
    seconds: int
        Number of seconds to format. Must be non‑negative.

    Returns
    -------
    str
        Human‑readable duration, e.g. "1d 2h 3m 4s".
    """
    if not isinstance(seconds, int) or seconds < 0:
        raise ValueError("seconds must be a non‑negative integer")

    parts = []
    remainder = seconds
    for unit, unit_sec in [("d", 86_400), ("h", 3_600), ("m", 60), ("s", 1)]:
        if remainder >= unit_sec:
            value, remainder = divmod(remainder, unit_sec)
            parts.append(f"{value}{unit}")
    return " ".join(parts) if parts else "0s"
