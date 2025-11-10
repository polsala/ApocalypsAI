import datetime
import argparse
import sys

# The immutable, universally recognized Cosmic Alignment Time (CAT) in UTC.
# All temporal calculations are relative to this epoch.
COSMIC_ALIGNMENT_TIME_STR = "2025-01-01T00:00:00Z"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_current_utc_time() -> datetime.datetime:
    """Returns the current UTC time."""
    return datetime.datetime.utcnow()

def get_cosmic_alignment_time() -> datetime.datetime:
    """Parses and returns the Cosmic Alignment Time as a datetime object."""
    return datetime.datetime.strptime(COSMIC_ALIGNMENT_TIME_STR, "%Y-%m-%dT%H:%M:%SZ")

def format_timedelta(td: datetime.timedelta) -> str:
    """Formats a timedelta object into a human-readable string (days, H:M:S)."""
    total_seconds = int(td.total_seconds())
    is_negative = total_seconds < 0
    abs_seconds = abs(total_seconds)

    days = abs_seconds // (24 * 3600)
    abs_seconds %= (24 * 3600)
    hours = abs_seconds // 3600
    abs_seconds %= 3600
    minutes = abs_seconds // 60
    seconds = abs_seconds % 60

    return f"{days} days, {hours:02}:{minutes:02}:{seconds:02}"

def main():
    parser = argparse.ArgumentParser(
        description="Chronos-Sync Time Adjuster: Align your clock with the Cosmic Rhythm."
    )
    parser.add_argument(
        "--offset-hours",
        type=int,
        default=0,
        help="Apocalypse Offset in hours. Added to Cosmic Alignment Time to determine target sync time."
    )
    args = parser.parse_args()

    current_utc_time = get_current_utc_time()
    cosmic_alignment_time = get_cosmic_alignment_time()
    apocalypse_offset = datetime.timedelta(hours=args.offset_hours)
    target_sync_time = cosmic_alignment_time + apocalypse_offset

    print(f"Current UTC Time: {current_utc_time.strftime(DATE_FORMAT)}")
    print(f"Cosmic Alignment Time: {cosmic_alignment_time.strftime(DATE_FORMAT)}")
    print(f"Apocalypse Offset: {apocalypse_offset.total_seconds() / 3600:+.0f} hours")
    print(f"Target Sync Time: {target_sync_time.strftime(DATE_FORMAT)}")
    print()

    drift = target_sync_time - current_utc_time

    if drift == datetime.timedelta(0):
        print("Temporal Drift: Your system clock is perfectly aligned with the Target Sync Time. No adjustment needed.")
    else:
        direction = "behind" if drift > datetime.timedelta(0) else "ahead of"
        action = "advance" if drift > datetime.timedelta(0) else "rewind"
        formatted_drift = format_timedelta(drift)

        print(f"Temporal Drift: Your system clock is currently {formatted_drift} {direction} the Target Sync Time.")
        print(f"To synchronize, you need to {action} your clock by {formatted_drift}.")

if __name__ == "__main__":
    main()
