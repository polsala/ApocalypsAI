"""human-duration-parser
=========================

Parse human‑readable duration strings into total seconds.

Supported units:
- weeks:   `w`
- days:    `d`
- hours:   `h`
- minutes: `m`
- seconds: `s`

Both spaced ("1d 2h") and compact ("1d2h") forms are accepted.
"""

from __future__ import annotations

import argparse
import re
from typing import Dict, Tuple

# Mapping of unit suffix to number of seconds per unit
_UNIT_SECONDS: Dict[str, int] = {
    "w": 7 * 24 * 60 * 60,
    "d": 24 * 60 * 60,
    "h": 60 * 60,
    "m": 60,
    "s": 1,
}

# Regex that captures a number (int or float) followed by a unit letter.
# It allows optional whitespace between groups.
_DURATION_RE = re.compile(r"(?P<value>\d+(?:\.\d+)?)(?P<unit>[wdhms])", re.IGNORECASE)


def _normalize(s: str) -> str:
    """Remove whitespace and lower‑case the string for easier parsing."""
    return s.replace(" ", "").lower()


def parse_duration(duration: str) -> int:
    """Convert a duration string to total seconds.

    Parameters
    ----------
    duration: str
        Human‑readable duration, e.g. ``"2h30m"`` or ``"1d 4h"``.

    Returns
    -------
    int
        Total number of seconds represented by the input.

    Raises
    ------
    ValueError
        If the string contains unknown units or cannot be parsed.
    """
    if not isinstance(duration, str):
        raise ValueError("duration must be a string")

    cleaned = _normalize(duration)
    if not cleaned:
        raise ValueError("empty duration string")

    total_seconds = 0
    pos = 0
    while pos < len(cleaned):
        match = _duration_match_at(cleaned, pos)
        if not match:
            raise ValueError(f"unparseable segment at position {pos}: '{cleaned[pos:]}'")
        value_str, unit = match.group("value"), match.group("unit")
        try:
            value = float(value_str)
        except ValueError as exc:
            raise ValueError(f"invalid numeric value '{value_str}'") from exc
        if unit not in _UNIT_SECONDS:
            raise ValueError(f"unsupported unit '{unit}'")
        total_seconds += int(value * _UNIT_SECONDS[unit])
        pos = match.end()
    return total_seconds


def _duration_match_at(s: str, pos: int) -> re.Match | None:
    """Attempt to match a duration token at *pos* in *s*.

    Returns the match object or ``None`` if no token starts at *pos*.
    """
    return _DURATION_RE.match(s, pos)


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Convert a human‑readable duration to seconds.")
    parser.add_argument("duration", help="Duration string, e.g. '2h30m' or '1d 4h'.")
    args = parser.parse_args()
    try:
        seconds = parse_duration(args.duration)
        print(seconds)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    _cli()
