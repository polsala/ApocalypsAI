import sys
import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

def get_current_times_in_timezones(timezone_names: list[str]) -> dict[str, datetime.datetime]:
    """
    Gets the current UTC time and converts it to the specified timezones.
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    times = {"UTC": now_utc}

    for tz_name in timezone_names:
        try:
            tz = ZoneInfo(tz_name)
            times[tz_name] = now_utc.astimezone(tz)
        except ZoneInfoNotFoundError:
            print(f"Warning: Timezone '{tz_name}' not found. Skipping.", file=sys.stderr)
        except Exception as e:
            print(f"Error processing timezone '{tz_name}': {e}", file=sys.stderr)
    return times

def format_time_output(times: dict[str, datetime.datetime]) -> str:
    """
    Formats the dictionary of times into a human-readable string.
    """
    output_lines = ["--- Chronos-Chime Temporal Scan ---"]

    # Always display UTC first
    if "UTC" in times:
        output_lines.append(f"UTC: {times['UTC'].isoformat(timespec='minutes')}")
        del times["UTC"]

    output_lines.append("") # Blank line for spacing

    # Determine max timezone name length for alignment
    # Filter out UTC from this calculation as it's already printed
    max_tz_len = max((len(tz_name) for tz_name in times.keys()), default=0)
    if max_tz_len < 15: # Ensure minimum width for common timezones like 'America/New_York'
        max_tz_len = 15

    for tz_name, dt_obj in sorted(times.items()):
        offset_str = dt_obj.strftime('%z') # e.g., +0100
        offset_str = f"{offset_str[:3]}:{offset_str[3:]}" # e.g., +01:00
        output_lines.append(
            f"{tz_name.ljust(max_tz_len)}: {dt_obj.isoformat(timespec='minutes')} (Offset: {offset_str})"
        )
    return "\n".join(output_lines)

def main():
    default_timezones = [
        "America/New_York",
        "Europe/London",
        "Asia/Tokyo",
        "Australia/Sydney"
    ]
    
    # sys.argv[0] is the script name itself
    if len(sys.argv) > 1:
        requested_timezones = sys.argv[1:]
    else:
        requested_timezones = default_timezones

    current_times = get_current_times_in_timezones(requested_timezones)
    print(format_time_output(current_times))

if __name__ == "__main__":
    main()
