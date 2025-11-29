import re
from typing import Dict

# Mapping of ISO‑8601 designators to seconds (approximate for months/years)
_UNIT_SECONDS: Dict[str, int] = {
    "Y": 365 * 24 * 3600,   # year = 365 days (ignoring leap years)
    "M": 30 * 24 * 3600,    # month = 30 days (approximation)
    "W": 7 * 24 * 3600,
    "D": 24 * 3600,
    "H": 3600,
    "M_TIME": 60,   # minutes – distinguished from months by context
    "S": 1,
}

_DURATION_REGEX = re.compile(
    r"^P"                                   # starts with 'P'
    r"(?:(?P<years>\d+(?:\.\d+)?)Y)?"      # years
    r"(?:(?P<months>\d+(?:\.\d+)?)M)?"    # months (date part)
    r"(?:(?P<weeks>\d+(?:\.\d+)?)W)?"     # weeks
    r"(?:(?P<days>\d+(?:\.\d+)?)D)?"      # days
    r"(?:T"                                 # time part begins with 'T'
    r"(?:(?P<hours>\d+(?:\.\d+)?)H)?"     # hours
    r"(?:(?P<minutes>\d+(?:\.\d+)?)M)?"   # minutes
    r"(?:(?P<seconds>\d+(?:\.\d+)?)S)?"   # seconds
    r")?$"
)

def _to_seconds(value: str, unit: str) -> int:
    """Convert a numeric string + unit designator to seconds.

    Fractional values are truncated toward zero (int()).
    """
    number = float(value)
    # Minutes use a different key to avoid clash with months.
    key = "M_TIME" if unit == "M" and "T" in value else unit
    seconds_per_unit = _UNIT_SECONDS[unit if unit != "M" else ("M_TIME" if "T" in value else "M")]
    return int(number * seconds_per_unit)

def parse_duration(iso_duration: str) -> int:
    """Parse an ISO‑8601 duration string and return total seconds.

    Parameters
    ----------
    iso_duration: str
        ISO‑8601 duration, e.g. "P3Y6M4DT12H30M5S" or "PT1H".

    Returns
    -------
    int
        Total seconds represented by the duration.

    Raises
    ------
    ValueError
        If the string does not conform to the ISO‑8601 duration format.
    """
    match = _DURATION_REGEX.fullmatch(iso_duration)
    if not match:
        raise ValueError(f"Invalid ISO‑8601 duration: {iso_duration!r}")

    total_seconds = 0
    groups = match.groupdict()
    # Date part units
    for unit_key in ["years", "months", "weeks", "days"]:
        value = groups.get(unit_key)
        if value is not None:
            designator = unit_key[0].upper()  # Y, M, W, D
            total_seconds += _to_seconds(value, designator)
    # Time part units (note minutes share 'M' designator)
    for unit_key in ["hours", "minutes", "seconds"]:
        value = groups.get(unit_key)
        if value is not None:
            designator = unit_key[0].upper()
            if unit_key == "minutes":
                designator = "M"  # minutes use 'M' in time context
            total_seconds += _to_seconds(value, designator)
    return total_seconds

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m nightly_iso8601_duration_parser <ISO_DURATION>")
        sys.exit(1)
    try:
        secs = parse_duration(sys.argv[1])
        print(secs)
    except ValueError as e:
        print(e)
        sys.exit(1)
