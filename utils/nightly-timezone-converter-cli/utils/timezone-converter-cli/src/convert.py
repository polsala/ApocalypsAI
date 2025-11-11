import argparse
import sys
from datetime import datetime
from zoneinfo import ZoneInfo


def parse_datetime(dt_str: str) -> datetime:
    """Parse an ISO‑8601 datetime string without timezone info.

    The function expects a string like ``2023-01-01T12:00:00``.
    """
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError as exc:
        raise ValueError(f"Invalid datetime format: {dt_str!r}. Expected ISO‑8601.") from exc


def convert(dt_str: str, from_tz: str, to_tz: str) -> str:
    """Convert *dt_str* from *from_tz* to *to_tz*.

    Returns an ISO‑8601 string with the target offset.
    """
    naive_dt = parse_datetime(dt_str)
    try:
        from_zone = ZoneInfo(from_tz)
        to_zone = ZoneInfo(to_tz)
    except Exception as exc:
        raise ValueError(f"Invalid timezone name: {exc}")

    aware_dt = naive_dt.replace(tzinfo=from_zone)
    target_dt = aware_dt.astimezone(to_zone)
    return target_dt.isoformat()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Convert a datetime from one timezone to another.")
    parser.add_argument("datetime", help="Datetime in ISO‑8601 format, e.g., 2023-01-01T12:00:00")
    parser.add_argument("from_tz", help="Source IANA timezone, e.g., UTC")
    parser.add_argument("to_tz", help="Target IANA timezone, e.g., America/New_York")
    args = parser.parse_args(argv)

    try:
        result = convert(args.datetime, args.from_tz, args.to_tz)
        print(result)
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
