import argparse
import datetime
import os

LOG_DIR = "logs"

def get_log_filepath(date_obj):
    """Generates the log file path for a given date."""
    return os.path.join(LOG_DIR, f"{date_obj.strftime('%Y-%m-%d')}.log")

def add_entry(message: str):
    """Adds a timestamped entry to the current day's log file."""
    current_time = datetime.datetime.now()
    log_filepath = get_log_filepath(current_time)
    timestamp = current_time.strftime("%H:%M:%S")

    os.makedirs(LOG_DIR, exist_ok=True) # Ensure log directory exists

    with open(log_filepath, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"Entry added to {log_filepath}")

def view_entries(date_str: str = None, last_n: int = None):
    """
    Views entries from a specific date's log file or the last N entries from today.
    """
    if date_str:
        try:
            target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return
        log_filepath = get_log_filepath(target_date)
    else:
        target_date = datetime.datetime.now().date()
        log_filepath = get_log_filepath(target_date)

    if not os.path.exists(log_filepath):
        print(f"No log entries found for {target_date.strftime('%Y-%m-%d')}.")
        return

    with open(log_filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if last_n:
        lines = lines[-last_n:]

    if not lines:
        print(f"No log entries found for {target_date.strftime('%Y-%m-%d')}.")
        return

    print(f"--- Log for {target_date.strftime('%Y-%m-%d')} ---")
    for line in lines:
        print(line.strip())
    print("-----------------------------------")


def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Chronicle Keeper Logbook: Record your daily observations."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new entry to today's log.")
    add_parser.add_argument("message", type=str, help="The message to log.")

    # View command
    view_parser = subparsers.add_parser("view", help="View log entries.")
    view_parser.add_argument(
        "--date",
        type=str,
        help="View entries for a specific date (YYYY-MM-DD). Defaults to today.",
    )
    view_parser.add_argument(
        "--last",
        type=int,
        metavar="N",
        help="View the last N entries from the specified date (or today).",
    )

    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.message)
    elif args.command == "view":
        view_entries(args.date, args.last)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
