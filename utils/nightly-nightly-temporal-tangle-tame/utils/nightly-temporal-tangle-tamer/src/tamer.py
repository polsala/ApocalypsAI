import argparse
import datetime
import sys
import pytz

def parse_timestamp(timestamp_str, input_format, input_tz_name):
    """
    Parses a timestamp string into a timezone-aware datetime object.
    Handles Unix epoch, ISO 8601, and custom formats.
    """
    input_tz = pytz.timezone(input_tz_name)

    try:
        # Try Unix epoch
        epoch = int(timestamp_str)
        dt_utc = datetime.datetime.fromtimestamp(epoch, tz=pytz.utc)
        return dt_utc.astimezone(input_tz)
    except ValueError:
        pass # Not an epoch, try other formats

    try:
        # Try ISO 8601 (with or without timezone info)
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00' # Convert Z to explicit UTC offset
        dt = datetime.datetime.fromisoformat(timestamp_str)
        if dt.tzinfo is None:
            # If no timezone info in ISO string, assume input_tz
            return input_tz.localize(dt)
        return dt.astimezone(input_tz)
    except ValueError:
        pass # Not ISO 8601, try custom format

    if input_format:
        try:
            dt = datetime.datetime.strptime(timestamp_str, input_format)
            return input_tz.localize(dt)
        except ValueError:
            pass # Custom format failed

    raise ValueError(f"Could not parse timestamp '{timestamp_str}' with given format '{input_format}' or as epoch/ISO 8601.")

def main():
    parser = argparse.ArgumentParser(
        description="Tame temporal tangles: convert timestamps between formats and timezones."
    )
    parser.add_argument(
        "--timestamp",
        required=True,
        help="The timestamp to convert (Unix epoch, ISO 8601, or custom string)."
    )
    parser.add_argument(
        "--input-format",
        help="The strftime format string if --timestamp is a custom string. Not needed for epoch or ISO 8601."
    )
    parser.add_argument(
        "--input-tz",
        default="UTC",
        help="The IANA timezone name for the input timestamp (e.g., 'UTC', 'America/New_York'). Defaults to UTC."
    )
    parser.add_argument(
        "--output-format",
        default="%Y-%m-%dT%H:%M:%S%z",
        help="The strftime format string for the output. Defaults to ISO 8601 (%%Y-%%m-%%dT%%H:%%M:%%S%%z)."
    )
    parser.add_argument(
        "--output-tz",
        default="UTC",
        help="The IANA timezone name for the output. Defaults to UTC."
    )

    args = parser.parse_args()

    try:
        # Parse the input timestamp
        dt_aware = parse_timestamp(args.timestamp, args.input_format, args.input_tz)

        # Convert to the output timezone
        output_tz = pytz.timezone(args.output_tz)
        dt_output = dt_aware.astimezone(output_tz)

        # Format the output
        print(dt_output.strftime(args.output_format))

    except pytz.exceptions.UnknownTimeZoneError as e:
        print(f"Error: Unknown timezone specified: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
