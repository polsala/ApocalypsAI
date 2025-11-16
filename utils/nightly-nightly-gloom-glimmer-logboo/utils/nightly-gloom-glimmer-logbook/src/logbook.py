import argparse
import json
import os
from datetime import datetime

LOG_FILE_NAME = "logbook.json"

def _get_log_file_path():
    """Determines the path to the logbook.json file."""
    # The logbook.json will be stored in the same directory as the script.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, LOG_FILE_NAME)

def _load_log(log_file_path):
    """Loads existing log entries from the JSON file."""
    if not os.path.exists(log_file_path):
        return []
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {LOG_FILE_NAME} is corrupted or empty. Starting a new log.")
        return []
    except Exception as e:
        print(f"Error loading log file: {e}")
        return []

def _save_log(log_file_path, log_entries):
    """Saves log entries to the JSON file."""
    try:
        with open(log_file_path, 'w', encoding='utf-8') as f:
            json.dump(log_entries, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving log file: {e}")

def add_entry(entry_text: str, glimmer_text: str):
    """Adds a new log entry with the current date."""
    log_file_path = _get_log_file_path()
    log_entries = _load_log(log_file_path)

    current_date = datetime.now().strftime("%Y-%m-%d")
    new_entry = {
        "date": current_date,
        "gloom": entry_text,
        "glimmer": glimmer_text
    }
    log_entries.append(new_entry)
    _save_log(log_file_path, log_entries)
    print(f"Log entry added for {current_date}.")

def view_entries():
    """Prints all log entries to the console."""
    log_file_path = _get_log_file_path()
    log_entries = _load_log(log_file_path)

    if not log_entries:
        print("No entries in the logbook yet.")
        return

    for entry in log_entries:
        print(f"--- Log Entry: {entry.get('date', 'N/A')} ---")
        print(f"Gloom: {entry.get('gloom', 'N/A')}")
        print(f"Glimmer: {entry.get('glimmer', 'N/A')}")
        print("-----------------------------")

def main():
    parser = argparse.ArgumentParser(
        description="A simple command-line logbook for recording daily events and 'glimmers' of hope."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new log entry.")
    add_parser.add_argument("gloom", type=str, help="The main log entry (gloom/observation).")
    add_parser.add_argument("glimmer", type=str, help="A positive observation or glimmer of hope.")

    # View command
    view_parser = subparsers.add_parser("view", help="View all log entries.")

    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.gloom, args.glimmer)
    elif args.command == "view":
        view_entries()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
