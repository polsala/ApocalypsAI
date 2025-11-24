import argparse
import datetime
import os

DEFAULT_LOG_FILE = "wasteland_log.md"
LOG_HEADER = "# Wasteland Logbook\n\n"

def _ensure_log_header(log_file: str):
    """Ensures the log file exists and has the correct header."""
    if not os.path.exists(log_file) or os.path.getsize(log_file) == 0:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(LOG_HEADER)

def add_entry(log_file: str, entry_text: str):
    """
    Appends a new timestamped entry to the log file.
    """
    _ensure_log_header(log_file)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"## {timestamp}\n{entry_text}\n\n"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(entry)
    print(f"Entry added to {log_file}")

def view_log(log_file: str):
    """
    Prints the entire content of the log file to stdout.
    """
    if not os.path.exists(log_file):
        print(f"Log file '{log_file}' not found. Start by adding an entry.")
        return

    with open(log_file, 'r', encoding='utf-8') as f:
        print(f.read())

def main():
    parser = argparse.ArgumentParser(
        description="A simple logbook for your wasteland adventures.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--file",
        "-f",
        default=DEFAULT_LOG_FILE,
        help=f"Specify the log file to use (default: {DEFAULT_LOG_FILE})"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new entry to the logbook")
    add_parser.add_argument(
        "entry_text",
        type=str,
        help="The text of the log entry to add."
    )

    # View command
    view_parser = subparsers.add_parser("view", help="View the entire logbook")

    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.file, args.entry_text)
    elif args.command == "view":
        view_log(args.file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
