import argparse
import re
import sys
from typing import Dict

# Regex pattern to capture optional groups for days, hours, minutes, seconds
_DURATION_RE = re.compile(
    r"(?:(?P<days>\d+)\s*d)?\s*"
    r"(?:(?P<hours>\d+)\s*h)?\s*"
    r"(?:(?P<minutes>\d+)\s*m)?\s*"
    r"(?:(?P<seconds>\d+)\s*s)?\s*$",
    re.IGNORECASE,
)

_UNIT_TO_SECONDS: Dict[str, int] = {
    "days": 86400,
    "hours": 3600,
    "minutes": 60,
    "seconds": 1,
}


def parse_duration(duration_str: str) -> int:
    """Parse a human‑friendly duration string into total seconds.

    Supported units are days (d), hours (h), minutes (m), and seconds (s).
    The order of units does not matter and whitespace is ignored.

    Args:
        duration_str: String like "1d 2h30m" or "45m10s".

    Returns:
        Total number of seconds as an integer.

    Raises:
        ValueError: If the string cannot be parsed.
    """
    if not isinstance(duration_str, str):
        raise ValueError("duration_str must be a string")

    # Remove all whitespace for easier matching
    cleaned = duration_str.replace(" ", "")
    match = _DURATION_RE.fullmatch(cleaned)
    if not match:
        raise ValueError(f"Unable to parse duration string: '{duration_str}'")

    total_seconds = 0
    for unit, factor in _UNIT_TO_SECONDS.items():
        value = match.group(unit)
        if value is not None:
            total_seconds += int(value) * factor
    return total_seconds


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a human‑friendly duration string to seconds."
    )
    parser.add_argument(
        "duration",
        type=str,
        help="Duration string (e.g., '2d5h30m').",
    )
    args = parser.parse_args()
    try:
        seconds = parse_duration(args.duration)
        print(seconds)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
