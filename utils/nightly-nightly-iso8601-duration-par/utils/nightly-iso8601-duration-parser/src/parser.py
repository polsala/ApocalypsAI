"""ISO 8601 Duration Parser
================================

Provides a single public function :func:`parse_iso8601_duration` that converts an
ISO 8601 duration string (e.g. ``"PT1H30M"``) into the total number of seconds.

The implementation deliberately supports only the most common subset of the
standard:

- ``P`` – period designator (required)
- ``nD`` – days
- ``T`` – time designator (optional, introduces hour/minute/second components)
- ``nH`` – hours
- ``nM`` – minutes
- ``nS`` – seconds

All components are optional, but at least one must be present.  The parser raises
a :class:`ValueError` for malformed inputs.
"""

import re
from typing import Optional

# Regular expression that captures days, hours, minutes, and seconds.
_DURATION_RE = re.compile(
    r"^P"
    r"(?:(?P<days>\d+)D)?"
    r"(?:T"
    r"(?:(?P<hours>\d+)H)?"
    r"(?:(?P<minutes>\d+)M)?"
    r"(?:(?P<seconds>\d+)S)?"
    r")?"
    r"$"
)

def _to_int(value: Optional[str]) -> int:
    """Convert a captured regex group to ``int`` (defaults to ``0``)."""
    return int(value) if value is not None else 0

def parse_iso8601_duration(duration: str) -> int:
    """Parse an ISO 8601 duration string and return the total seconds.

    Parameters
    ----------
    duration: str
        ISO 8601 duration (e.g. ``"PT1H30M"`` or ``"P2DT3H"``).

    Returns
    -------
    int
        Total number of seconds represented by the duration.

    Raises
    ------
    ValueError
        If the string does not conform to the supported subset of ISO 8601.
    """
    match = _DURATION_RE.fullmatch(duration)
    if not match:
        raise ValueError(f"Invalid ISO 8601 duration: {duration!r}")

    days = _to_int(match.group("days"))
    hours = _to_int(match.group("hours"))
    minutes = _to_int(match.group("minutes"))
    seconds = _to_int(match.group("seconds"))

    total_seconds = (
        days * 86_400 +
        hours * 3_600 +
        minutes * 60 +
        seconds
    )
    return total_seconds

# ---------------------------------------------------------------------------
# Simple CLI for quick manual checks
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Convert ISO 8601 duration to seconds")
    parser.add_argument("duration", help="ISO 8601 duration string, e.g. PT1H30M")
    args = parser.parse_args()

    try:
        secs = parse_iso8601_duration(args.duration)
        print(secs)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
