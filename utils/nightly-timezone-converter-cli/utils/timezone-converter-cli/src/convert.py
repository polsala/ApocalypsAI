#!/usr/bin/env python3
"""timezone-converter-cli

A tiny CLI that converts an ISO‑8601 timestamp from one IANA time zone to another.

Usage:
    python convert.py --timestamp "2025-01-01T12:00:00" \
                       --from-tz "America/New_York" \
                       --to-tz "Europe/London"
"""

import argparse
import sys
from datetime import datetime
from zoneinfo import ZoneInfo


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert timestamps between IANA time zones.")
    parser.add_argument(
        "--timestamp",
        required=True,
        help="ISO‑8601 timestamp without offset (e.g., 2025-01-01T12:00:00)",
    )
    parser.add_argument(
        "--from-tz",
        required=True,
        help="Source IANA time zone (e.g., America/New_York)",
    )
    parser.add_argument(
        "--to-tz",
        required=True,
        help="Target IANA time zone (e.g., Europe/London)",
    )
    return parser.parse_args(argv)


def convert(timestamp_str: str, from_tz: str, to_tz: str) -> str:
    """Convert *timestamp_str* from *from_tz* to *to_tz*.

    Parameters
    ----------
    timestamp_str: str
        ISO‑8601 datetime without offset (e.g., "2025-01-01T12:00:00").
    from_tz: str
        Source IANA time zone name.
    to_tz: str
        Target IANA time zone name.

    Returns
    -------
    str
        ISO‑8601 representation of the converted datetime, including the target offset.
    """
    # Parse naive datetime
    try:
        naive_dt = datetime.fromisoformat(timestamp_str)
    except ValueError as exc:
        raise ValueError(f"Invalid timestamp format: {timestamp_str}") from exc

    # Attach source tz
    try:
        source_zone = ZoneInfo(from_tz)
    except Exception as exc:
        raise ValueError(f"Invalid source time zone: {from_tz}") from exc
    aware_dt = naive_dt.replace(tzinfo=source_zone)

    # Convert to target tz
    try:
        target_zone = ZoneInfo(to_tz)
    except Exception as exc:
        raise ValueError(f"Invalid target time zone: {to_tz}") from exc
    target_dt = aware_dt.astimezone(target_zone)

    # Return ISO string with offset
    return target_dt.isoformat()


def main() -> int:
    args = parse_args()
    try:
        result = convert(args.timestamp, args.from_tz, args.to_tz)
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
