'''duration_parser: convert strings like '2h30m' to total seconds.'''

import re
import sys
from argparse import ArgumentParser

_PATTERN = re.compile(r'(?P<value>\d+)(?P<unit>[dhms])')

_UNIT_SECONDS = {
    'd': 86400,
    'h': 3600,
    'm': 60,
    's': 1,
}

def parse_duration(duration: str) -> int:
    """
    Parse a duration string and return total seconds.

    Args:
        duration: String like '2h30m' or '1d 4h'.

    Returns:
        Total seconds as int.

    Raises:
        ValueError: If the string contains unknown units or malformed parts.
    """
    total = 0
    cleaned_input = duration.replace(' ', '')
    for match in _PATTERN.finditer(cleaned_input):
        value = int(match.group('value'))
        unit = match.group('unit')
        if unit not in _UNIT_SECONDS:
            raise ValueError(f'Unsupported unit: {unit}')
        total += value * _UNIT_SECONDS[unit]
    # Verify that the whole string was consumed by the pattern
    leftover = _PATTERN.sub('', cleaned_input)
    if leftover:
        raise ValueError(f'Unrecognized format: {leftover}')
    return total

def _main() -> None:
    parser = ArgumentParser(description='Convert duration strings to seconds.')
    parser.add_argument('duration', help='Duration string, e.g., 2h30m')
    args = parser.parse_args()
    try:
        seconds = parse_duration(args.duration)
        print(seconds)
    except ValueError as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    _main()
