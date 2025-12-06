import argparse
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

def display_current_time(timezones: list[str]):
    """Displays the current time in a list of specified timezones."""
    print("Current Time Across Zones:")
    for tz_name in timezones:
        try:
            tz = ZoneInfo(tz_name)
            now_in_tz = datetime.now(tz)
            print(f"{tz_name}: {now_in_tz.isoformat(timespec='minutes')}")
        except ZoneInfoNotFoundError:
            print(f"Error: Timezone '{tz_name}' not found. Please use a valid IANA timezone name.")
        except Exception as e:
            print(f"An unexpected error occurred for timezone '{tz_name}': {e}")

def convert_time(time_str: str, from_tz_name: str, to_tz_name: str):
    """Converts a specific time from a source timezone to a target timezone."""
    try:
        from_tz = ZoneInfo(from_tz_name)
        to_tz = ZoneInfo(to_tz_name)

        # Parse the input time string without timezone info first
        # Assuming format "YYYY-MM-DD HH:MM"
        dt_naive = datetime.strptime(time_str, "%Y-%m-%d %H:%M")

        # Localize the naive datetime to the source timezone
        dt_from_tz = dt_naive.replace(tzinfo=from_tz)

        # Convert to the target timezone
        dt_to_tz = dt_from_tz.astimezone(to_tz)

        print("Conversion:")
        print(f"{time_str} {from_tz_name}  ->  {dt_to_tz.isoformat(timespec='minutes')} {to_tz_name}")

    except ZoneInfoNotFoundError as e:
        print(f"Error: {e}. Please use valid IANA timezone names.")
    except ValueError:
        print(f"Error: Invalid time format '{time_str}'. Expected 'YYYY-MM-DD HH:MM'.")
    except Exception as e:
        print(f"An unexpected error occurred during conversion: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Chronos's Compass: Navigate the temporal currents.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Group for display mode
    display_group = parser.add_argument_group("Display Current Time")
    display_group.add_argument(
        "--display",
        nargs='+',
        metavar='TIMEZONE',
        help="Display current time in one or more specified IANA timezones (e.g., 'UTC', 'America/New_York')."
    )

    # Group for conversion mode
    convert_group = parser.add_argument_group("Convert Specific Time")
    convert_group.add_argument(
        "--convert",
        metavar='DATETIME',
        help="The datetime string to convert (e.g., '2023-10-27 14:00'). Requires --from-tz and --to-tz."
    )
    convert_group.add_argument(
        "--from-tz",
        metavar='FROM_TIMEZONE',
        help="The source IANA timezone for conversion (e.g., 'Europe/London')."
    )
    convert_group.add_argument(
        "--to-tz",
        metavar='TO_TIMEZONE',
        help="The target IANA timezone for conversion (e.g., 'America/Los_Angeles')."
    )

    args = parser.parse_args()

    if args.display:
        if args.convert or args.from_tz or args.to_tz:
            parser.error("Cannot use --display with --convert, --from-tz, or --to-tz simultaneously.")
        display_current_time(args.display)
    elif args.convert:
        if not (args.from_tz and args.to_tz):
            parser.error("--convert requires both --from-tz and --to-tz.")
        if args.display:
            parser.error("Cannot use --convert with --display simultaneously.")
        convert_time(args.convert, args.from_tz, args.to_tz)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
