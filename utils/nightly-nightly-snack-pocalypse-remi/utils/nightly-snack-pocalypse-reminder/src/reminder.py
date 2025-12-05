import json
import os
import time

# Define file paths relative to the script's execution directory
# This assumes the script is run from the utility's root directory or its parent.
# For robustness, we can derive the absolute path of the script's directory.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, '..', 'config.json')
STATE_FILE = os.path.join(SCRIPT_DIR, '..', 'state.json')

def get_config():
    default_config = {
        'interval_minutes': 60,
        'reminder_message': '🚨 Snack-pocalypse Alert! Time to refuel the resistance! 🍪☕'
    }
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            try:
                user_config = json.load(f)
                return {**default_config, **user_config}
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {CONFIG_FILE}. Using default configuration.")
                return default_config
    return default_config

def get_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {STATE_FILE}. Starting fresh.")
                return {'last_reminded_timestamp': 0}
    return {'last_reminded_timestamp': 0}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def main():
    config = get_config()
    state = get_state()

    interval_seconds = config['interval_minutes'] * 60
    current_time = time.time()
    last_reminded = state.get('last_reminded_timestamp', 0)

    if current_time - last_reminded >= interval_seconds:
        print(config['reminder_message'])
        state['last_reminded_timestamp'] = current_time
        save_state(state)
    else:
        time_until_next_reminder = last_reminded + interval_seconds - current_time
        minutes_until_next = int(time_until_next_reminder / 60)
        seconds_remainder = int(time_until_next_reminder % 60)
        print(f"Next snack-pocalypse reminder in {minutes_until_next}m {seconds_remainder}s.")

if __name__ == '__main__':
    main()
