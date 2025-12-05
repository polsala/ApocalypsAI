import argparse
import datetime
import os
import sys

LOG_FILE_NAME = "chronicle.log"

def _get_timestamp():
    """Returns the current timestamp in a consistent format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_entry(message: str, log_file_path: str = LOG_FILE_NAME) -> None:
    """Appends a timestamped message to the chronicle log."""
    timestamp = _get_timestamp()
    entry = f"[{timestamp}] - {message}\n"
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(entry)
        print(f"Chronicle updated: '{message}'")
    except IOError as e:
        print(f"Error writing to chronicle log: {e}", file=sys.stderr)
        raise

def view_entries(num_entries: int = 5, log_file_path: str = LOG_FILE_NAME) -> list[str]:
    """Reads and returns the last N entries from the chronicle log."""
    try:
        if not os.path.exists(log_file_path):
            return []
        with open(log_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return [line.strip() for line in lines[-num_entries:]]
    except IOError as e:
        print(f"Error reading from chronicle log: {e}", file=sys.stderr)
        raise

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Chronicle Keeper's Log - Record your daily observations."
    )
    parser.add_argument(
        "-a", "--add", type=str,
        help="Add a new entry to the chronicle log."
    )
    parser.add_argument(
        "-v", "--view", type=int, nargs='?', const=5, default=0,
        help="View the last N entries from the chronicle log. Defaults to 5 if N is not specified."
    )
    parser.add_argument(
        "--log-file", type=str, default=LOG_FILE_NAME,
        help=f"Specify a custom log file name. Defaults to '{LOG_FILE_NAME}'."
    )

    args = parser.parse_args()

    if args.add:
        add_entry(args.add, args.log_file)
    elif args.view > 0:
        entries = view_entries(args.view, args.log_file)
        if entries:
            print("\n--- Chronicle Log (Last {} Entries) ---".format(len(entries)))
            for entry in entries:
                print(entry)
            print("------------------------------------")
        else:
            print(f"No entries found in '{args.log_file}'.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
