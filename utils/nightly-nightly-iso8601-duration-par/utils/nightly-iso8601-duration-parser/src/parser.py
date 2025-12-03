import re
from typing import Dict

__all__ = ["parse_iso8601_duration"]

# Regex pattern for a subset of ISO 8601 durations.
# Supports days, hours, minutes, seconds (e.g., P3DT4H5M6S or PT4H5M).
_DURATION_RE = re.compile(
    r"^P"
    r"(?:(?P<days>\d+)D)?"
    r"(?:T"
    r"(?:(?P<hours>\d+)H)?"
    r"(?:(?P<minutes>\d+)M)?"
    r"(?:(?P<seconds>\d+)S)?"
    r")?$"
)

def _to_int(value: str | None) -> int:
    """Convert optional numeric string to int, defaulting to 0."""
    return int(value) if value is not None else 0

def parse_iso8601_duration(duration: str) -> int:
    """Parse an ISO 8601 duration string and return total seconds.

    Parameters
    ----------
    duration: str
        ISO 8601 duration (e.g., ``"PT1H30M"``).

    Returns
    -------
    int
        Total number of seconds represented by the duration.

    Raises
    ------
    ValueError
        If the string does not match the supported ISO 8601 subset.
    """
    match = _DURATION_RE.fullmatch(duration)
    if not match:
        raise ValueError(f"Invalid ISO8601 duration: {duration!r}")

    parts: Dict[str, int] = {
        "days": _to_int(match.group("days")),
        "hours": _to_int(match.group("hours")),
        "minutes": _to_int(match.group("minutes")),
        "seconds": _to_int(match.group("seconds")),
    }

    total_seconds = (
        parts["days"] * 86400 +
        parts["hours"] * 3600 +
        parts["minutes"] * 60 +
        parts["seconds"]
    )
    return total_seconds
