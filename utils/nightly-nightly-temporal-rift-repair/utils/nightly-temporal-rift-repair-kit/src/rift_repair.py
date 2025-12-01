import argparse
import datetime
import sys

def unix_to_iso(timestamp: int) -> str:
    """Converts a Unix timestamp (seconds) to an ISO 8601 UTC string."""
    dt_object = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    return dt_object.isoformat(timespec='seconds')

def iso_to_unix(iso_string: str) -> int:
    """Converts an ISO 8601 UTC string to a Unix timestamp (seconds)."""
    # datetime.fromisoformat handles various ISO formats, including 'Z' for UTC and offsets.
    # If the string doesn't have timezone info, assume UTC.
    try:
        dt_object = datetime.datetime.fromisoformat(iso_string)
        if dt_object.tzinfo is None:
            dt_object = dt_object.replace(tzinfo=datetime.timezone.utc)
        else:
            dt_object = dt_object.astimezone(datetime.timezone.utc)
        return int(dt_object.timestamp())
    except ValueError:
        raise ValueError(f"Invalid ISO 8601 string: {iso_string}")

def main():
    parser = argparse.ArgumentParser(
        description="Temporal Rift Repair Kit: Convert timestamps between formats.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "timestamp",
        nargs="?",
        type=int,
        help="Unix timestamp (seconds) to convert to ISO 8601 UTC."
    )
    parser.add_argument(
        "--from-iso",
        metavar="ISO_STRING",
        help="ISO 8601 UTC string to convert to Unix timestamp."
    )
    parser.add_argument(
        "--now",
        action="store_true",
        help="Display current UTC time in ISO 8601 and Unix timestamp."
    )

    args = parser.parse_args()

    if args.now:
        current_utc = datetime.datetime.now(datetime.timezone.utc)
        print(f"Current UTC ISO 8601: {current_utc.isoformat(timespec='seconds')}")
        print(f"Current Unix Timestamp: {int(current_utc.timestamp())}")
    elif args.timestamp is not None:
        try:
            iso_output = unix_to_iso(args.timestamp)
            print(f"Unix {args.timestamp} -> ISO 8601 UTC: {iso_output}")
        except Exception as e:
            print(f"Error converting Unix timestamp: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.from_iso:
        try:
            unix_output = iso_to_unix(args.from_iso)
            print(f"ISO 8601 UTC '{args.from_iso}' -> Unix: {unix_output}")
        except ValueError as e:
            print(f"Error converting ISO 8601 string: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
