import json
import os
import sys
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'sentry_log.json')

def _load_logs():
    """Loads log entries from the JSON file."""
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Handle corrupted or empty JSON file
        return []

def _save_logs(logs):
    """Saves log entries to the JSON file."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True) # Ensure directory exists
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4)

def add_log(sentry_name, observation):
    """Adds a new sentry log entry."""
    logs = _load_logs()
    timestamp = datetime.now().isoformat()
    new_entry = {
        "timestamp": timestamp,
        "sentry_name": sentry_name,
        "observation": observation
    }
    logs.append(new_entry)
    _save_logs(logs)
    print(f"Log added for {sentry_name} at {timestamp}.")

def view_logs(sentry_name=None):
    """Views log entries, optionally filtered by sentry name."""
    logs = _load_logs()
    if not logs:
        print("No sentry logs found.")
        return

    filtered_logs = [log for log in logs if sentry_name is None or log["sentry_name"] == sentry_name]

    if not filtered_logs:
        if sentry_name:
            print(f"No logs found for sentry: {sentry_name}")
        else:
            print("No sentry logs found.")
        return

    print("\n--- Sentry Logs ---")
    for log in filtered_logs:
        print(f"Timestamp: {log['timestamp']}")
        print(f"Sentry:    {log['sentry_name']}")
        print(f"Observed:  {log['observation']}")
        print("-------------------")

def clear_logs():
    """Clears all log entries."""
    _save_logs([])
    print("All sentry logs cleared.")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python src/sentry_log.py add <sentry_name> <observation_text>")
        print("  python src/sentry_log.py view [--sentry <sentry_name>]")
        print("  python src/sentry_log.py clear")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 4:
            print("Usage: python src/sentry_log.py add <sentry_name> <observation_text>")
            sys.exit(1)
        sentry_name = sys.argv[2]
        observation = " ".join(sys.argv[3:])
        add_log(sentry_name, observation)
    elif command == "view":
        sentry_name = None
        if "--sentry" in sys.argv:
            try:
                sentry_index = sys.argv.index("--sentry")
                sentry_name = sys.argv[sentry_index + 1]
            except (ValueError, IndexError):
                print("Error: --sentry requires a sentry name.")
                sys.exit(1)
        view_logs(sentry_name)
    elif command == "clear":
        clear_logs()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
