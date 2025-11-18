import argparse
import datetime
import os

LOG_FILE = 'wayfinder_log.txt'

def _get_log_path():
    """Returns the absolute path to the log file, located next to the script."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), LOG_FILE)

def add_entry(entry_type: str, location: str, description: str):
    """Adds a new entry to the log file."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"{timestamp} | {entry_type.upper()} | {location} | {description}"
    log_path = _get_log_path()
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(entry + '\n')
    print(f"Entry added: {entry}")

def get_entries() -> list[str]:
    """Reads all entries from the log file."""
    log_path = _get_log_path()
    if not os.path.exists(log_path):
        return []
    with open(log_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def list_entries():
    """Prints all entries to the console."""
    entries = get_entries()
    if not entries:
        print("No entries found in the logbook.")
        return
    print("\n--- Wasteland Wayfinder Logbook ---")
    for entry in entries:
        print(entry)
    print("-----------------------------------")

def search_entries(query: str):
    """Searches entries for a given query string and prints matches."""
    entries = get_entries()
    if not entries:
        print("No entries found to search.")
        return

    matches = [entry for entry in entries if query.lower() in entry.lower()]
    if not matches:
        print(f"No entries found matching '{query}'.")
        return

    print(f"\n--- Search Results for '{query}' ---")
    for match in matches:
        print(match)
    print("-----------------------------------")

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Wayfinder Logbook: Track routes, POIs, and hazards."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new log entry.')
    add_parser.add_argument('--type', required=True, choices=['ROUTE', 'POI', 'HAZARD', 'NOTE'],
                            help='Type of entry (ROUTE, POI, HAZARD, NOTE).')
    add_parser.add_argument('--location', required=True,
                            help='Location or context of the entry.')
    add_parser.add_argument('--description', required=True,
                            help='Detailed description of the entry.')

    # List command
    list_parser = subparsers.add_parser('list', help='List all log entries.')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search log entries by keyword.')
    search_parser.add_argument('--query', required=True, help='Keyword to search for.')

    args = parser.parse_args()

    if args.command == 'add':
        add_entry(args.type, args.location, args.description)
    elif args.command == 'list':
        list_entries()
    elif args.command == 'search':
        search_entries(args.query)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
