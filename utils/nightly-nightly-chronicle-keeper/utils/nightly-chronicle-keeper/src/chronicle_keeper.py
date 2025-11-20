import argparse
import datetime
import os
import sys

DEFAULT_CHRONICLE_FILE = "chronicle.log"

def get_timestamp():
    """Returns a formatted timestamp."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def append_entry(message: str, chronicle_file: str = DEFAULT_CHRONICLE_FILE):
    """Appends a timestamped message to the chronicle file."""
    try:
        # Ensure the directory exists for the chronicle file
        chronicle_dir = os.path.dirname(chronicle_file)
        if chronicle_dir:
            os.makedirs(chronicle_dir, exist_ok=True)

        with open(chronicle_file, 'a', encoding='utf-8') as f:
            f.write(f"[{get_timestamp()}] {message}\n")
        print(f"Entry added to {chronicle_file}")
    except IOError as e:
        print(f"Error writing to chronicle file: {e}", file=sys.stderr)
        sys.exit(1)

def view_entries(num_entries: int, chronicle_file: str = DEFAULT_CHRONICLE_FILE):
    """Displays the last N entries from the chronicle file."""
    try:
        if not os.path.exists(chronicle_file):
            print(f"Chronicle file '{chronicle_file}' does not exist yet.")
            return

        with open(chronicle_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if not lines:
            print(f"Chronicle file '{chronicle_file}' is empty.")
            return

        start_index = max(0, len(lines) - num_entries)
        for line in lines[start_index:]:
            print(line.strip())

    except IOError as e:
        print(f"Error reading chronicle file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Chronicle Keeper: Log timestamped entries to a chronicle file."
    )
    parser.add_argument(
        "-f", "--file",
        default=DEFAULT_CHRONICLE_FILE,
        help=f"Path to the chronicle file (default: {DEFAULT_CHRONICLE_FILE})"
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Append command
    append_parser = subparsers.add_parser("append", help="Append a new entry to the chronicle.")
    append_parser.add_argument(
        "message",
        help="The message to log in the chronicle."
    )

    # View command
    view_parser = subparsers.add_parser("view", help="View the last N entries from the chronicle.")
    view_parser.add_argument(
        "-n", "--num",
        type=int,
        default=10,
        help="Number of last entries to display (default: 10)."
    )

    args = parser.parse_args()

    if args.command == "append":
        append_entry(args.message, args.file)
    elif args.command == "view":
        view_entries(args.num, args.file)

if __name__ == "__main__":
    main()
