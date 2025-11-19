#!/usr/bin/env python3
"""
Utility to convert datetime strings between IANA time zones.

CLI:
    python -m src.convert "<datetime>" <from_tz> <to_tz>

Example:
    python -m src.convert "2025-11-19 15:30" America/New_York Asia/Tokyo
"""

import sys
from datetime import datetime
from zoneinfo import ZoneInfo


def parse_dt(dt_str: str) -> datetime:
    """Parse a datetime string in '%Y-%m-%d %H:%M' format."""
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")


def convert_time(dt_str: str, from_tz: str, to_tz: str) -> str:
    """Convert a datetime string from one IANA time zone to another.

    Returns an ISO‑8601 string with the target offset.
    """
    naive_dt = parse_dt(dt_str)
    from_zone = ZoneInfo(from_tz)
    to_zone = ZoneInfo(to_tz)
    aware_dt = naive_dt.replace(tzinfo=from_zone)
    target_dt = aware_dt.astimezone(to_zone)
    return target_dt.isoformat()


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 3:
        print("Usage: python -m src.convert \"<datetime>\" <from_tz> <to_tz>")
        return 1
    dt_str, from_tz, to_tz = argv
    try:
        result = convert_time(dt_str, from_tz, to_tz)
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
