import argparse
import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from typing import List, Dict, Optional

def _get_timezone(tz_str: str) -> ZoneInfo:
    """Helper to get a ZoneInfo object, raising a custom error for clarity."""
    try:
        return ZoneInfo(tz_str)
    except ZoneInfoNotFoundError:
        raise ValueError(f"Invalid time zone: {tz_str}")

def get_current_times(timezones: List[str]) -> Dict[str, datetime.datetime]:
    """Returns the current time in a list of specified time zones."""
    current_utc = datetime.datetime.now(datetime.timezone.utc)
    results = {}
    for tz_str in timezones:
        tz = _get_timezone(tz_str)
        results[tz_str] = current_utc.astimezone(tz)
    return results

def convert_time(
    dt_str: str,
    from_tz_str: str,
    to_tz_strs: List[str],
    dt_format: str = "%Y-%m-%d %H:%M"
) -> Dict[str, datetime.datetime]:
    """Converts a given datetime string from a source timezone to multiple target timezones."""
    from_tz = _get_timezone(from_tz_str)

    try:
        # Parse the naive datetime string
        naive_dt = datetime.datetime.strptime(dt_str, dt_format)
        # Localize it to the source timezone
        localized_dt = naive_dt.replace(tzinfo=from_tz)
    except ValueError as e:
        raise ValueError(f"Invalid datetime format or value: {dt_str}. Expected format: {dt_format}. Error: {e}")

    results = {"original": localized_dt}
    for to_tz_str in to_tz_strs:
        to_tz = _get_timezone(to_tz_str)
        results[to_tz_str] = localized_dt.astimezone(to_tz)
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Temporal Rift Time-Sync Adjuster: Display and convert times across time zones."
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Subparser for 'current' command
    current_parser = subparsers.add_parser(
        "current", help="Display current time in specified time zones."
    )
    current_parser.add_argument(
        "--zones",
        nargs='+',
        required=True,
        help="List of IANA time zone names (e.g., UTC, Europe/London)."
    )

    # Subparser for 'convert' command
    convert_parser = subparsers.add_parser(
        "convert", help="Convert a specific time from one zone to others."
    )
    convert_parser.add_argument(
        "--time",
        type=str,
        required=True,
        help="Date and time string to convert (e.g., '2024-07-20 10:00')."
    )
    convert_parser.add_argument(
        "--from-zone",
        type=str,
        required=True,
        help="Source IANA time zone name (e.g., UTC)."
    )
    convert_parser.add_argument(
        "--to-zones",
        nargs='+',
        required=True,
        help="List of target IANA time zone names (e.g., Europe/Berlin, Asia/Tokyo)."
    )
    convert_parser.add_argument(
        "--format",
        type=str,
        default="%Y-%m-%d %H:%M",
        help="Format of the input time string (default: '%Y-%m-%d %H:%M')."
    )

    args = parser.parse_args()

    try:
        if args.command == "current":
            print("Current Times:")
            times = get_current_times(args.zones)
            for tz, dt in times.items():
                print(f"{tz}: {dt.isoformat()}")
        elif args.command == "convert":
            times = convert_time(args.time, args.from_zone, args.to_zones, args.format)
            original_dt = times.pop("original")
            print(f"Original Time ({args.from_zone}): {original_dt.isoformat()}")
            print("Converted Times:")
            for tz, dt in times.items():
                print(f"{tz}: {dt.isoformat()}")
    except ValueError as e:
        print(f"Error: {e}")
        parser.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        parser.exit(1)

if __name__ == "__main__":
    main()
