import argparse
import datetime
import os

DEFAULT_LOG_FILE = "chronicle.log"

def add_entry(message: str, log_file: str):
    """Appends a timestamped message to the specified log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    try:
        with open(log_file, "a") as f:
            f.write(entry)
        print(f"Entry added to {log_file}")
    except IOError as e:
        print(f"Error writing to log file {log_file}: {e}")

def view_log(log_file: str):
    """Prints the contents of the specified log file."""
    if not os.path.exists(log_file):
        print(f"Log file '{log_file}' not found.")
        return

    try:
        with open(log_file, "r") as f:
            content = f.read()
            if content:
                print(f"\n--- Contents of {log_file} ---\n")
                print(content.strip())
                print(f"\n--- End of {log_file} ---")
            else:
                print(f"Log file '{log_file}' is empty.")
    except IOError as e:
        print(f"Error reading log file {log_file}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chronicle Keeper Logbook: Log timestamped entries."
    )
    parser.add_argument(
        "-m", "--message",
        type=str,
        help="The message to add to the chronicle log."
    )
    parser.add_argument(
        "-f", "--log-file",
        type=str,
        default=DEFAULT_LOG_FILE,
        help=f"Path to the log file (default: {DEFAULT_LOG_FILE})."
    )
    parser.add_argument(
        "-v", "--view",
        action="store_true",
        help="View the contents of the chronicle log."
    )

    args = parser.parse_args()

    if args.message:
        add_entry(args.message, args.log_file)
    elif args.view:
        view_log(args.log_file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
