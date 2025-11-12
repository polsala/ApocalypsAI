#!/usr/bin/env python3
"""
timezone_converter CLI

Converts a datetime string from a source timezone to a target timezone.

Usage:
    python utils/timezone-converter-cli/src/convert.py "<datetime>" <source_tz> <target_tz>
Example:
    python utils/timezone-converter-cli/src/convert.py "2025-01-01 15:30" America/New_York Asia/Tokyo
"""

import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
import sys


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Convert datetime between time zones.")
    parser.add_argument("datetime", help='Datetime string in "%Y-%m-%d %H:%M" format')
    parser.add_argument("source_tz", help="Source IANA time zone")
    parser.add_argument("target_tz", help="Target IANA time zone")
    return parser.parse_args(argv)


def convert(dt_str: str, source_tz: str, target_tz: str) -> str:
    """Convert datetime string from source_tz to target_tz.

    Returns an ISO‑8601 formatted string with the target timezone offset.
    """
    try:
        naive_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError as e:
        raise ValueError(f"Invalid datetime format: {e}")

    try:
        src_zone = ZoneInfo(source_tz)
        tgt_zone = ZoneInfo(target_tz)
    except Exception as e:
        raise ValueError(f"Invalid time zone: {e}")

    src_dt = naive_dt.replace(tzinfo=src_zone)
    tgt_dt = src_dt.astimezone(tgt_zone)
    return tgt_dt.isoformat()


def main():
    args = parse_args()
    try:
        result = convert(args.datetime, args.source_tz, args.target_tz)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
