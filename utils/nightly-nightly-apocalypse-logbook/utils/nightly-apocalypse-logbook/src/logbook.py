import os
import argparse
from datetime import datetime

LOG_DIR_NAME = "logbook_data"
DEFAULT_CATEGORIES = ["scavenge", "build", "observe", "reflect", "report"]

def _get_log_path(date: datetime) -> str:
    """Constructs the full path for a daily log file."""
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")
    return os.path.join(LOG_DIR_NAME, year, month, f"{day}.md")

def _ensure_log_dir(log_file_path: str):
    """Ensures the directory structure for a log file exists."""
    dir_path = os.path.dirname(log_file_path)
    os.makedirs(dir_path, exist_ok=True)

def init_logbook():
    """Initializes the base logbook directory."""
    if not os.path.exists(LOG_DIR_NAME):
        os.makedirs(LOG_DIR_NAME)
        print(f"Logbook initialized! Created directory: {LOG_DIR_NAME}/")
    else:
        print(f"Logbook directory '{LOG_DIR_NAME}/' already exists.")

def new_entry(category: str, message: str):
    """Adds a new entry to today's log."""
    if category.lower() not in DEFAULT_CATEGORIES:
        print(f"Error: Invalid category '{category}'. Available categories: {', '.join(DEFAULT_CATEGORIES)}")
        return

    now = datetime.now()
    log_file_path = _get_log_path(now)
    _ensure_log_dir(log_file_path)

    timestamp = now.strftime("%H:%M:%S")
    entry_line = f"### [{timestamp}] {category.upper()} - {message}\n"

    # Check if it's a new file for the day to add the header
    is_new_file = not os.path.exists(log_file_path)

    with open(log_file_path, "a", encoding="utf-8") as f:
        if is_new_file:
            f.write(f"# Logbook Entry for {now.strftime('%Y-%m-%d')}\n\n")
        f.write(entry_line)
    print(f"Entry added to {log_file_path}")

def view_entries(date_str: str = None):
    """Views entries for a specific date or today."""
    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD.")
            return
    else:
        target_date = datetime.now()

    log_file_path = _get_log_path(target_date)

    if os.path.exists(log_file_path):
        with open(log_file_path, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print(f"No log entries found for {target_date.strftime('%Y-%m-%d')}.")

def list_categories():
    """Lists all available categories."""
    print("Available categories:")
    for cat in DEFAULT_CATEGORIES:
        print(f"- {cat}")

def main():
    parser = argparse.ArgumentParser(
        description="Apocalypse Logbook: A CLI tool for daily journaling."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize the logbook directory.")

    # New command
    new_parser = subparsers.add_parser("new", help="Add a new entry to today's log.")
    new_parser.add_argument("category", type=str, help="Category for the entry.")
    new_parser.add_argument("message", type=str, help="The log entry message.")

    # View command
    view_parser = subparsers.add_parser("view", help="View entries for a specific date.")
    view_parser.add_argument(
        "date",
        type=str,
        nargs="?",
        help="Date in YYYY-MM-DD format (defaults to today).",
    )

    # Categories command
    categories_parser = subparsers.add_parser("categories", help="List available categories.")

    args = parser.parse_args()

    if args.command == "init":
        init_logbook()
    elif args.command == "new":
        new_entry(args.category, args.message)
    elif args.command == "view":
        view_entries(args.date)
    elif args.command == "categories":
        list_categories()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
