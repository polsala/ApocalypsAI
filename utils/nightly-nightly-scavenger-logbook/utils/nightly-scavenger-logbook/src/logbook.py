import argparse
import datetime
import os

LOG_FILE = "scavenger_log.txt"

def _get_log_path():
    """Returns the absolute path to the log file, relative to the script's directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, LOG_FILE)

def add_entry(location: str, note: str):
    """Adds a new timestamped entry to the log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] Location: {location} | Note: {note}\n"
    log_path = _get_log_path()
    with open(log_path, "a") as f:
        f.write(entry)
    print(f"Log entry added: {entry.strip()}")

def view_entries():
    """Prints all entries from the log file."""
    log_path = _get_log_path()
    if not os.path.exists(log_path):
        print("No log entries found yet.")
        return

    print("--- Scavenger Log ---")
    with open(log_path, "r") as f:
        for line in f:
            print(line.strip())
    print("---------------------")

def main():
    parser = argparse.ArgumentParser(
        description="A simple logbook for scavenger findings."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new log entry")
    add_parser.add_argument(
        "--location", required=True, help="The location of the finding."
    )
    add_parser.add_argument(
        "--note", required=True, help="A description or note about the finding."
    )

    # View command
    view_parser = subparsers.add_parser("view", help="View all log entries")

    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.location, args.note)
    elif args.command == "view":
        view_entries()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
