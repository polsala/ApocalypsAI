"""Utility to parse ISO‑8601 duration strings.

The implementation follows the ISO‑8601 "duration" format:
    P[nY][nM][nW][nD][T[nH][nM][nS]]
where each component is optional and may appear in any order (except that the "T" separator must precede time components).

Only the components listed above are supported; fractional values are not parsed.
"""

import re
import sys
from typing import Dict

# Regex pattern based on the ISO‑8601 duration specification.
_DURATION_REGEX = re.compile(
    r"^P"  # starts with 'P'
    r"(?:(?P<years>\d+)Y)?"
    r"(?:(?P<months>\d+)M)?"
    r"(?:(?P<weeks>\d+)W)?"
    r"(?:(?P<days>\d+)D)?"
    r"(?:T"
    r"(?:(?P<hours>\d+)H)?"
    r"(?:(?P<minutes>\d+)M)?"
    r"(?:(?P<seconds>\d+)S)?"
    r")?"
    r"$"
)

def _to_int(value: str | None) -> int:
    """Convert a captured string to int, defaulting to 0 if None."""
    return int(value) if value is not None else 0

def parse_iso8601_duration(iso_str: str) -> Dict[str, int]:
    """Parse an ISO‑8601 duration string.

    Parameters
    ----------
    iso_str: str
        The duration string, e.g. ``"P1Y2M3DT4H5M6S"``.

    Returns
    -------
    dict
        Mapping with keys ``years, months, weeks, days, hours, minutes, seconds``.
        Missing components are reported as ``0``.

    Raises
    ------
    ValueError
        If the string does not conform to the ISO‑8601 duration format.
    """
    match = _DURATION_REGEX.fullmatch(iso_str)
    if not match:
        raise ValueError(f"Invalid ISO‑8601 duration: {iso_str!r}")

    components = {
        "years": _to_int(match.group('years')),
        "months": _to_int(match.group('months')),
        "weeks": _to_int(match.group('weeks')),
        "days": _to_int(match.group('days')),
        "hours": _to_int(match.group('hours')),
        "minutes": _to_int(match.group('minutes')),
        "seconds": _to_int(match.group('seconds')),
    }
    return components

def _cli() -> None:
    """Simple command‑line interface.

    Usage: ``python -m utils.nightly-iso8601-duration-parser.src.duration_parser <duration>``
    """
    if len(sys.argv) != 2:
        print("Usage: python -m utils.nightly-iso8601-duration-parser.src.duration_parser <ISO‑8601 duration>")
        sys.exit(1)
    iso = sys.argv[1]
    try:
        result = parse_iso8601_duration(iso)
        print(result)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    _cli()
