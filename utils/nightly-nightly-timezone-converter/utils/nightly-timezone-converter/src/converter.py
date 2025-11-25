import argparse
import sys
from datetime import datetime
from zoneinfo import ZoneInfo


def convert(datetime_str: str, src_tz: str, tgt_tz: str) -> str:
    """Convert an ISO‑8601 datetime string from src_tz to tgt_tz.

    Args:
        datetime_str: ISO‑8601 datetime without offset, e.g. "2023-10-31T15:00:00".
        src_tz: Source IANA timezone name.
        tgt_tz: Target IANA timezone name.

    Returns:
        ISO‑8601 datetime string with the target offset.
    """
    # Parse naive datetime
    try:
        naive_dt = datetime.fromisoformat(datetime_str)
    except ValueError as e:
        raise ValueError(f"Invalid datetime format: {datetime_str}") from e

    # Attach source timezone
    try:
        src_zone = ZoneInfo(src_tz)
    except Exception as e:
        raise ValueError(f"Invalid source timezone: {src_tz}") from e
    src_dt = naive_dt.replace(tzinfo=src_zone)

    # Convert to target timezone
    try:
        tgt_zone = ZoneInfo(tgt_tz)
    except Exception as e:
        raise ValueError(f"Invalid target timezone: {tgt_tz}") from e
    tgt_dt = src_dt.astimezone(tgt_zone)

    return tgt_dt.isoformat()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="ChronoChameleon – timezone converter")
    parser.add_argument("datetime", help="ISO‑8601 datetime string, e.g., 2023-10-31T15:00:00")
    parser.add_argument("src_tz", help="Source IANA timezone, e.g., America/New_York")
    parser.add_argument("tgt_tz", help="Target IANA timezone, e.g., Europe/London")
    args = parser.parse_args(argv)

    try:
        result = convert(args.datetime, args.src_tz, args.tgt_tz)
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
