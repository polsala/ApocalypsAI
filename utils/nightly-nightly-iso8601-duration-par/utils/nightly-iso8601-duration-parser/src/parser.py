"""
ISO8601 Duration Parser

Provides `parse_duration` to convert an ISO 8601 duration string to total seconds.
Supported components: weeks (W), days (D), hours (H), minutes (M), seconds (S).
"""

import re
import sys
from typing import Dict

# Regex for a subset of ISO 8601 durations (no months/years)
_DURATION_RE = re.compile(
    r'^P'                                   # starts with 'P'
    r'(?:(?P<weeks>\d+)W)?'                 # weeks
    r'(?:(?P<days>\d+)D)?'                  # days
    r'(?:T'                                 # time part begins with 'T'
    r'(?:(?P<hours>\d+)H)?'                 # hours
    r'(?:(?P<minutes>\d+)M)?'               # minutes
    r'(?:(?P<seconds>\d+)S)?'               # seconds
    r')?$'
)

def parse_duration(duration: str) -> int:
    """Parse an ISO 8601 duration string and return total seconds.

    Parameters
    ----------
    duration: str
        ISO 8601 duration, e.g., "P3DT4H5M6S" or "PT20M".

    Returns
    -------
    int
        Total number of seconds represented by the duration.

    Raises
    ------
    ValueError
        If the string is not a valid ISO 8601 duration.
    """
    match = _DURATION_RE.fullmatch(duration)
    if not match:
        raise ValueError(f"Invalid ISO 8601 duration: {duration!r}")

    parts: Dict[str, int] = {k: int(v) if v else 0 for k, v in match.groupdict().items()}
    total_seconds = (
        parts['weeks'] * 7 * 24 * 3600 +
        parts['days'] * 24 * 3600 +
        parts['hours'] * 3600 +
        parts['minutes'] * 60 +
        parts['seconds']
    )
    return total_seconds

def _cli():
    if len(sys.argv) != 2:
        print("Usage: python -m src.parser <ISO8601_DURATION>")
        sys.exit(1)
    try:
        secs = parse_duration(sys.argv[1])
        print(secs)
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    _cli()
