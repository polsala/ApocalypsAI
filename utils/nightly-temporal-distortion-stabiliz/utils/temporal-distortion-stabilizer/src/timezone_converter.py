import argparse
from datetime import datetime
import sys

try:
    import pytz
except ImportError:
    print("Error: 'pytz' library not found. Please install it using 'pip install pytz'.", file=sys.stderr)
    sys.exit(1)

def convert_timezone(dt_str: str, from_tz_str: str, to_tz_str: str) -> str:
    """Converts a datetime string from one timezone to another."""
    try:
        # Parse the datetime string
        # Try common formats
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d %H:%M",
            "%m-%d-%Y %H:%M:%S",
            "%m/%d/%Y %H:%M:%S",
        ]
        dt_obj = None
        for fmt in formats:
            try:
                dt_obj = datetime.strptime(dt_str, fmt)
                break
            except ValueError:
                continue
        
        if dt_obj is None:
            raise ValueError(f"Could not parse datetime string: {dt_str}. Supported formats: {', '.join(formats)}")

        # Get timezone objects
        from_tz = pytz.timezone(from_tz_str)
        to_tz = pytz.timezone(to_tz_str)

        # Localize the datetime object to the source timezone
        localized_dt = from_tz.localize(dt_obj)

        # Convert to the target timezone
        converted_dt = localized_dt.astimezone(to_tz)

        return converted_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z")

    except pytz.exceptions.UnknownTimeZoneError as e:
        raise ValueError(f"Unknown timezone: {e}")
    except ValueError as e:
        raise ValueError(f"Datetime conversion error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Stabilize temporal distortions by converting datetimes between timezones."
    )
    parser.add_argument(
        "--datetime",
        required=True,
        help="The datetime string to convert (e.g., '2024-10-27 10:00:00')"
    )
    parser.add_argument(
        "--from_tz",
        required=True,
        help="The source IANA timezone (e.g., 'America/New_York')"
    )
    parser.add_argument(
        "--to_tz",
        required=True,
        help="The target IANA timezone (e.g., 'Europe/London')"
    )

    args = parser.parse_args()

    try:
        result = convert_timezone(args.datetime, args.from_tz, args.to_tz)
        print(f"Input: {args.datetime} {args.from_tz}")
        print(f"Output: {result}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
