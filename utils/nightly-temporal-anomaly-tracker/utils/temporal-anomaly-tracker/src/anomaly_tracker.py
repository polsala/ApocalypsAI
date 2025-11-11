import datetime
import os
import json
import time

# Configuration
THRESHOLD_SECONDS = 60  # Seconds. If time jumps more than this, it's an anomaly.
STATE_FILE = os.path.join(os.path.dirname(__file__), 'last_known_time.json')

def get_current_timestamp():
    """Returns the current UTC timestamp as a float."""
    return time.time()

def load_last_known_time(state_file_path):
    """Loads the last known timestamp from the state file."""
    if os.path.exists(state_file_path):
        try:
            with open(state_file_path, 'r') as f:
                data = json.load(f)
                return data.get('timestamp')
        except (json.JSONDecodeError, KeyError):
            # File corrupted or malformed, treat as no previous time
            print(f"Warning: Could not read or parse state file '{state_file_path}'. Starting fresh.")
            return None
    return None

def save_current_time(state_file_path, timestamp):
    """Saves the current timestamp to the state file."""
    with open(state_file_path, 'w') as f:
        json.dump({'timestamp': timestamp}, f)

def check_for_anomalies():
    """
    Checks for temporal anomalies by comparing current time to the last known time.
    Returns True if an anomaly is detected, False otherwise.
    """
    current_timestamp = get_current_timestamp()
    last_known_timestamp = load_last_known_time(STATE_FILE)

    if last_known_timestamp is None:
        print(f"First run or state file missing/corrupted. Initializing with current time: {datetime.datetime.fromtimestamp(current_timestamp, tz=datetime.timezone.utc)}")
        save_current_time(STATE_FILE, current_timestamp)
        return False

    time_difference = current_timestamp - last_known_timestamp

    if abs(time_difference) > THRESHOLD_SECONDS:
        print("--------------------------------------------------")
        print("🚨 Temporal Anomaly Detected! 🚨")
        print(f"  Last known time: {datetime.datetime.fromtimestamp(last_known_timestamp, tz=datetime.timezone.utc)}")
        print(f"  Current time:    {datetime.datetime.fromtimestamp(current_timestamp, tz=datetime.timezone.utc)}")
        print(f"  Difference:      {time_difference:.2f} seconds")
        print(f"  Threshold:       {THRESHOLD_SECONDS} seconds")
        print("  Investigate your system clock, NTP, or potential time-traveling squirrels!")
        print("--------------------------------------------------")
        # Update state file even on anomaly to track from this new point
        save_current_time(STATE_FILE, current_timestamp)
        return True
    else:
        print(f"System time stable. Difference: {time_difference:.2f} seconds (within {THRESHOLD_SECONDS}s threshold).")
        save_current_time(STATE_FILE, current_timestamp)
        return False

if __name__ == "__main__":
    check_for_anomalies()
