import argparse
import re
from typing import Dict

# Mapping of unit suffix to number of seconds
_UNIT_SECONDS: Dict[str, int] = {
    "w": 7 * 24 * 60 * 60,
    "d": 24 * 60 * 60,
    "h": 60 * 60,
    "m": 60,
    "s": 1,
}

_DURATION_RE = re.compile(r"(?P<value>\d+)(?P<unit>[wdhms])", re.IGNORECASE)


def _tokenize(duration: str) -> Dict[str, int]:
    """Extract numeric values per unit from *duration*.

    Returns a dict like ``{"h": 2, "m": 30}``. Unknown units are ignored.
    """
    tokens: Dict[str, int] = {}
    for match in _DURATION_RE.finditer(duration.replace(" ", "")):
        value = int(match.group("value"))
        unit = match.group("unit").lower()
        tokens[unit] = tokens.get(unit, 0) + value
    return tokens


def parse_duration(duration: str) -> int:
    """Convert a human‑readable *duration* string to total seconds.

    Supported units:
        - ``w`` – weeks
        - ``d`` – days
        - ``h`` – hours
        - ``m`` – minutes
        - ``s`` – seconds

    Example:
        >>> parse_duration("1d 2h30m")
        93600
    """
    if not isinstance(duration, str):
        raise TypeError("duration must be a string")
    tokens = _tokenize(duration)
    total = sum(tokens.get(unit, 0) * _UNIT_SECONDS[unit] for unit in _UNIT_SECONDS)
    return total


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a human‑readable duration string to seconds."
    )
    parser.add_argument(
        "duration",
        type=str,
        help="Duration string, e.g., '2h30m' or '1d 4h'.",
    )
    args = parser.parse_args()
    try:
        seconds = parse_duration(args.duration)
        print(seconds)
    except Exception as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    _cli()
