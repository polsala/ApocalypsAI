import argparse
from datetime import datetime
import sys

def calculate_countdown(target_datetime_str: str) -> str:
    """
    Calculates the time remaining until a target datetime.
    """
    try:
        target_dt = datetime.strptime(target_datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return "Error: Invalid date/time format. Please use YYYY-MM-DD HH:MM:SS."

    now = datetime.now() # Mock rationale: This is the primary point of non-determinism. Mocking allows fixed 'now' for testing.
    time_left = target_dt - now

    if time_left.total_seconds() <= 0:
        # Calculate absolute values for past events
        abs_time_left = abs(time_left)
        days = abs_time_left.days
        hours = abs_time_left.seconds // 3600
        minutes = (abs_time_left.seconds % 3600) // 60
        seconds = abs_time_left.seconds % 60
        return f"The apocalypse was {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds ago. You survived (or missed it)!"
    else:
        days = time_left.days
        hours = time_left.seconds // 3600
        minutes = (time_left.seconds % 3600) // 60
        seconds = time_left.seconds % 60
        return f"Time until apocalypse: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds."

def main():
    parser = argparse.ArgumentParser(
        description="Count down the time until a specified apocalypse event."
    )
    parser.add_argument(
        "target_datetime",
        type=str,
        help="The target date and time in YYYY-MM-DD HH:MM:SS format."
    )
    args = parser.parse_args()

    result = calculate_countdown(args.target_datetime)
    print(result)
    if "Error" in result or "ago" in result:
        sys.exit(1) # Indicate non-success for past events or errors

if __name__ == "__main__":
    main()
