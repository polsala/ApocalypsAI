import argparse
import csv
import os
from datetime import datetime

LOG_FILE = 'scavenger_log.csv'
HEADERS = ['Timestamp', 'Item', 'Quantity', 'Location']

def ensure_log_file_exists():
    """Ensures the log file exists with headers if it's new."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def add_entry(item: str, quantity: str, location: str):
    """Adds a new resource entry to the log file."""
    ensure_log_file_exists()
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, item, quantity, location])
    print(f"Logged: {item} (x{quantity}) at {location}")

def list_entries():
    """Lists all resource entries from the log file."""
    if not os.path.exists(LOG_FILE):
        print("No scavenger log found. Start logging your finds!")
        return

    with open(LOG_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader) # Read header row
        except StopIteration:
            print("Scavenger log is empty. Time to explore!")
            return

        entries = list(reader)
        if not entries:
            print("Scavenger log is empty. Time to explore!")
            return

        # Determine column widths for pretty printing
        col_widths = [len(h) for h in HEADERS]
        for entry in entries:
            for i, cell in enumerate(entry):
                col_widths[i] = max(col_widths[i], len(cell))

        # Print header
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(HEADERS))
        print(header_line)
        print("-|-".join('-' * width for width in col_widths))

        # Print entries
        for entry in entries:
            print(" | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(entry)))

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Resource Scavenger Log - Track your finds in the wasteland."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new resource entry')
    add_parser.add_argument('item', type=str, help='Name of the resource (e.g., "Canned Beans")')
    add_parser.add_argument('quantity', type=str, help='Amount found (e.g., "5", "1.5L")')
    add_parser.add_argument('location', type=str, help='Where you found it (e.g., "Old Supermart")')

    # List command
    list_parser = subparsers.add_parser('list', help='List all logged resource entries')

    args = parser.parse_args()

    if args.command == 'add':
        add_entry(args.item, args.quantity, args.location)
    elif args.command == 'list':
        list_entries()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
