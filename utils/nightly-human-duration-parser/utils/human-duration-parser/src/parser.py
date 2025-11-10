import re
import argparse


def parse_duration(duration_str: str) -> int:
    """Parse a human‑readable duration string into total seconds.

    Supported units:
    - days (`d`)
    - hours (`h`)
    - minutes (`m`)
    - seconds (`s`)

    Units may appear in any order, optionally separated by whitespace.
    Invalid fragments are ignored.
    """
    pattern = re.compile(r"(?P<value>\d+)\s*(?P<unit>[dhms])", re.IGNORECASE)
    total_seconds = 0
    for match in pattern.finditer(duration_str):
        value = int(match.group('value'))
        unit = match.group('unit').lower()
        if unit == 'd':
            total_seconds += value * 86400
        elif unit == 'h':
            total_seconds += value * 3600
        elif unit == 'm':
            total_seconds += value * 60
        elif unit == 's':
            total_seconds += value
    return total_seconds


def _cli():
    parser = argparse.ArgumentParser(
        description='Parse human‑readable duration strings into total seconds.'
    )
    parser.add_argument('duration', help='Duration string, e.g., "2h30m"')
    args = parser.parse_args()
    seconds = parse_duration(args.duration)
    print(seconds)


if __name__ == '__main__':
    _cli()
