import argparse
import datetime
import os

DEFAULT_LOG_FILE = "chronicle.log"

def add_entry(message: str, log_file: str):
    """Appends a timestamped message to the log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"Entry added to {log_file}")
    except IOError as e:
        print(f"Error writing to log file {log_file}: {e}")

def view_entries(num_entries: int | None, log_file: str):
    """Displays the last N entries from the log file, or all if N is None."""
    if not os.path.exists(log_file):
        print(f"Log file '{log_file}' not found. No entries to display.")
        return

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines:
            print(f"Log file '{log_file}' is empty.")
            return

        if num_entries is None:
            for line in lines:
                print(line.strip())
        else:
            for line in lines[-num_entries:]:
                print(line.strip())

    except IOError as e:
        print(f"Error reading log file {log_file}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="A command-line utility for keeping a timestamped logbook."
    )
    parser.add_argument(
        "--log-file",
        default=DEFAULT_LOG_FILE,
        help=f"Path to the log file (default: {DEFAULT_LOG_FILE})",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new entry to the logbook.")
    add_parser.add_argument("message", type=str, help="The message for the log entry.")

    # View command
    view_parser = subparsers.add_parser("view", help="View entries from the logbook.")
    view_parser.add_argument(
        "num_entries",
        type=int,
        nargs="?",  # Optional argument
        help="Number of last entries to display. If omitted, all entries are shown.",
    )

    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.message, args.log_file)
    elif args.command == "view":
        view_entries(args.num_entries, args.log_file)

if __name__ == "__main__":
    main()
