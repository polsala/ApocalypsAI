import argparse
from datetime import datetime, time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

def list_timezones():
    """Lists a selection of common time zones."""
    print("Available Time Zones (selection):")
    common_zones = [
        "UTC", "America/New_York", "America/Los_Angeles", "Europe/London",
        "Europe/Berlin", "Asia/Tokyo", "Asia/Shanghai", "Australia/Sydney"
    ]
    for tz_name in sorted(common_zones):
        print(f"- {tz_name}")
    print("\nFor a full list, refer to IANA Time Zone Database names.")

def convert_time(dt_str: str, from_tz_str: str, to_tz_str: str) -> str:
    """
    Converts a datetime string from one time zone to another.
    Assumes dt_str is in 'YYYY-MM-DD HH:MM' format.
    """
    try:
        from_tz = ZoneInfo(from_tz_str)
        to_tz = ZoneInfo(to_tz_str)
    except ZoneInfoNotFoundError as e:
        raise ValueError(f"Invalid time zone specified: {e}")

    try:
        # Parse the datetime string without timezone info first
        dt_naive = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        # Localize it to the 'from' timezone
        dt_from_tz = dt_naive.replace(tzinfo=from_tz)
        # Convert to the 'to' timezone
        dt_to_tz = dt_from_tz.astimezone(to_tz)
        return dt_to_tz.strftime('%Y-%m-%d %H:%M %Z%z')
    except ValueError as e:
        raise ValueError(f"Invalid datetime format or value: {e}. Expected YYYY-MM-DD HH:MM")

def suggest_meeting_times(timezones: list[str], preferred_start_hour_utc: int = 9, preferred_end_hour_utc: int = 17) -> dict:
    """
    Suggests meeting times by showing equivalent times in different zones
    for a few common UTC meeting slots, highlighting if they fall within
    a typical working day (8 AM - 6 PM local time).
    """
    if not timezones:
        raise ValueError("At least one timezone must be provided.")

    meeting_slots_utc = [
        time(9, 0),  # 9 AM UTC
        time(13, 0), # 1 PM UTC
        time(17, 0)  # 5 PM UTC
    ]

    today_utc = datetime.now(ZoneInfo("UTC")).date() # Use a fixed date for consistency in suggestions

    results = {}
    for slot_utc in meeting_slots_utc:
        utc_dt = datetime.combine(today_utc, slot_utc, tzinfo=ZoneInfo("UTC"))
        slot_key = utc_dt.strftime('%H:%M UTC')
        results[slot_key] = {}

        for tz_str in timezones:
            try:
                tz = ZoneInfo(tz_str)
                local_dt = utc_dt.astimezone(tz)
                local_time = local_dt.time()
                is_working_hours = time(8, 0) <= local_time <= time(18, 0) # 8 AM to 6 PM local
                results[slot_key][tz_str] = {
                    "local_time": local_dt.strftime('%H:%M %Z%z'),
                    "is_working_hours": is_working_hours
                }
            except ZoneInfoNotFoundError:
                results[slot_key][tz_str] = {
                    "error": "Invalid timezone",
                    "local_time": "N/A",
                    "is_working_hours": False
                }
    return results

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Chronosync Crystal Calibrator: Time zone conversion and meeting scheduler.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List time zones command
    list_parser = subparsers.add_parser('list', help='List common time zones.')

    # Convert time command
    convert_parser = subparsers.add_parser('convert', help='Convert a datetime between time zones.')
    convert_parser.add_argument('datetime', type=str, help='Datetime to convert (e.g., "2024-07-20 14:30").')
    convert_parser.add_argument('from_tz', type=str, help='Source time zone (e.g., "America/New_York").')
    convert_parser.add_argument('to_tz', type=str, help='Target time zone (e.g., "Europe/London").')

    # Suggest meeting command
    suggest_parser = subparsers.add_parser('suggest', help='Suggest meeting times across multiple time zones.')
    suggest_parser.add_argument('timezones', nargs='+', help='List of time zones to consider (e.g., "America/New_York" "Europe/London").')

    args = parser.parse_args()

    if args.command == 'list':
        list_timezones()
    elif args.command == 'convert':
        try:
            result = convert_time(args.datetime, args.from_tz, args.to_tz)
            print(f"Original: {args.datetime} {args.from_tz}")
            print(f"Converted: {result}")
        except ValueError as e:
            print(f"Error: {e}")
            exit(1)
    elif args.command == 'suggest':
        try:
            suggestions = suggest_meeting_times(args.timezones)
            print("Meeting Time Suggestions (8 AM - 6 PM local considered working hours):")
            for utc_slot, tz_data in suggestions.items():
                print(f"\n--- If meeting starts at {utc_slot} ---")
                for tz_name, data in tz_data.items():
                    status = "✅ Working Hours" if data["is_working_hours"] else "❌ Outside Working Hours"
                    if "error" in data:
                        print(f"  {tz_name}: {data['error']}")
                    else:
                        print(f"  {tz_name}: {data['local_time']} ({status})")
        except ValueError as e:
            print(f"Error: {e}")
            exit(1)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
