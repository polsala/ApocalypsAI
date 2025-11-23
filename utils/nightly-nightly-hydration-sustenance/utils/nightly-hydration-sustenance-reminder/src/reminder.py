import os
import random
from datetime import datetime, timedelta
import sys

# Configuration
REMINDER_INTERVAL_HOURS = 2
TIMESTAMP_FILE = "last_reminded.txt"

MESSAGES = [
    "[ApocalypsAI Wellness Protocol] Warning: Your organic processing unit requires hydration! Seek water before your code turns to dust.",
    "[ApocalypsAI Wellness Protocol] Alert: Sustenance levels critical! Forage for snacks to maintain peak survival efficiency.",
    "[ApocalypsAI Wellness Protocol] Directive: Take a brief tactical retreat. Hydrate and recalibrate your neural network.",
    "[ApocalypsAI Wellness Protocol] Urgent: Your internal power core is depleting! Recharge with a quick snack.",
    "[ApocalypsAI Wellness Protocol] Observation: Prolonged screen exposure detected. Initiate hydration sequence immediately.",
    "[ApocalypsAI Wellness Protocol] Recommendation: A moment of respite is crucial for survival. Grab a drink and stretch those post-apocalyptic muscles.",
]

def get_timestamp_file_path():
    """Returns the absolute path to the timestamp file, relative to the script's directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, TIMESTAMP_FILE)

def get_last_reminded_time():
    """Reads the last reminded timestamp from the file."""
    timestamp_file_path = get_timestamp_file_path()
    if os.path.exists(timestamp_file_path):
        try:
            with open(timestamp_file_path, 'r') as f:
                timestamp_str = f.read().strip()
                return datetime.fromisoformat(timestamp_str)
        except (ValueError, IOError):
            # File corrupted or unreadable, treat as if no timestamp exists
            pass
    return None

def update_last_reminded_time():
    """Writes the current time as the last reminded timestamp to the file."""
    timestamp_file_path = get_timestamp_file_path()
    with open(timestamp_file_path, 'w') as f:
        f.write(datetime.now().isoformat())

def main():
    last_reminded = get_last_reminded_time()
    current_time = datetime.now()

    if last_reminded is None or (current_time - last_reminded) > timedelta(hours=REMINDER_INTERVAL_HOURS):
        print(random.choice(MESSAGES))
        update_last_reminded_time()
        sys.exit(0)  # Success: reminder was given
    else:
        sys.exit(2)  # No-op: not enough time has passed

if __name__ == "__main__":
    main()
