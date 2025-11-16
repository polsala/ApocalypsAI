import datetime
import json
import os
import sys

# Path to the config.json file, assuming it's in the parent directory of 'src'
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

def load_config(config_path):
    """Loads snack schedule from a JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, 'r') as f:
        return json.load(f)

def check_snacks(current_time, config):
    """Checks if any snacks are due at the current time."""
    reminders = []
    for snack in config.get('snacks', []):
        try:
            snack_name = snack['name']
            snack_time_str = snack['time'] # e.g., "10:30"
            snack_hour, snack_minute = map(int, snack_time_str.split(':'))

            if current_time.hour == snack_hour and current_time.minute == snack_minute:
                reminders.append(f"It's time for your {snack_name}! Stay strong, survivor!")
        except (KeyError, ValueError) as e:
            print(f"Warning: Malformed snack entry found: {snack}. Error: {e}", file=sys.stderr)
            continue
    return reminders

def main():
    try:
        config = load_config(CONFIG_FILE)
        now = datetime.datetime.now()
        reminders = check_snacks(now, config)

        if reminders:
            for reminder in reminders:
                print(reminder)
            sys.exit(0) # Snacks were due
        else:
            print(f"No snacks due at {now.strftime('%H:%M')}. Keep vigilant!")
            sys.exit(2) # No-op, no snacks due
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing config file '{CONFIG_FILE}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
