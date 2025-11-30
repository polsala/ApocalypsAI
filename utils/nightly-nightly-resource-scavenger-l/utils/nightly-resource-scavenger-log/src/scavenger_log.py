import argparse
import os
from datetime import datetime

# Configuration
LOG_FILE = 'scavenger_log.md'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def _get_log_path():
    """Determines the absolute path for the log file."""
    # For simplicity, log file is in the current working directory.
    # Users can modify this to, e.g., os.path.expanduser('~/.apocalypsai/scavenger_log.md')
    return os.path.abspath(LOG_FILE)

def add_entry(category: str, description: str):
    """Adds a new entry to the scavenger log."""
    timestamp = datetime.now().strftime(DATE_FORMAT)
    entry = f"- [{timestamp}] [{category}] {description}\n"

    log_path = _get_log_path()
    with open(log_path, 'a') as f:
        f.write(entry)
    print(f"Entry added to {log_path}")

def list_entries(filter_date: str = None):
    """Lists all entries, optionally filtered by date."""
    log_path = _get_log_path()
    if not os.path.exists(log_path):
        print(f"No scavenger log found at {log_path}.")
        return

    print(f"\n--- Scavenger Log ({log_path}) ---")
    found_entries = False
    with open(log_path, 'r') as f:
        for line in f:
            if line.startswith('- ['):
                if filter_date:
                    # Extract date part from timestamp, e.g., '2023-10-27'
                    entry_date_str = line[3:13] # '- [YYYY-MM-DD'
                    if entry_date_str == filter_date:
                        print(line.strip())
                        found_entries = True
                else:
                    print(line.strip())
                    found_entries = True
    if not found_entries and filter_date:
        print(f"No entries found for date: {filter_date}")
    elif not found_entries:
        print("No entries found.")
    print("---------------------------\n")

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Resource Scavenger Log utility."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new log entry')
    add_parser.add_argument('category', type=str, help='Category for the resource (e.g., code, docs, idea)')
    add_parser.add_argument('description', type=str, help='Description of the scavenged resource')

    # List command
    list_parser = subparsers.add_parser('list', help='List log entries')
    list_parser.add_argument('--date', type=str, help='Filter entries by date (YYYY-MM-DD)')

    args = parser.parse_args()

    if args.command == 'add':
        add_entry(args.category, args.description)
    elif args.command == 'list':
        list_entries(args.date)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
