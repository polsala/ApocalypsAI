import argparse
import json
import os
from datetime import datetime

LOG_FILE = 'scavenger_log.json'

def _get_log_path():
    """Returns the absolute path to the log file."""
    # Ensure the log file is in the same directory as the script
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), LOG_FILE)

def _load_log():
    """Loads the scavenger log from the JSON file."""
    log_path = _get_log_path()
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {LOG_FILE} is corrupted or empty. Starting with an empty log.")
        return []

def _save_log(log_data):
    """Saves the scavenger log to the JSON file."""
    log_path = _get_log_path()
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=4)

def add_entry(item, location, quantity, notes):
    """Adds a new entry to the scavenger log."""
    log_data = _load_log()
    timestamp = datetime.now().isoformat()
    entry = {
        "timestamp": timestamp,
        "item": item,
        "location": location,
        "quantity": quantity,
        "notes": notes
    }
    log_data.append(entry)
    _save_log(log_data)
    print(f"Added: {item} (x{quantity}) from {location}")

def view_log():
    """Displays all entries in the scavenger log."""
    log_data = _load_log()
    if not log_data:
        print("The scavenger log is empty. Time to get scavenging!")
        return

    print("\n--- Scavenger Log ---")
    for i, entry in enumerate(log_data):
        print(f"Entry #{i+1}:")
        print(f"  Timestamp: {entry['timestamp']}")
        print(f"  Item: {entry['item']}")
        print(f"  Location: {entry['location']}")
        print(f"  Quantity: {entry['quantity']}")
        print(f"  Notes: {entry['notes']}")
        print("-" * 20)
    print("--- End of Log ---")

def search_log(keyword):
    """Searches the log for entries containing the keyword in item, location, or notes."""
    log_data = _load_log()
    found_entries = []
    keyword_lower = keyword.lower()

    for entry in log_data:
        if (keyword_lower in entry['item'].lower() or
            keyword_lower in entry['location'].lower() or
            keyword_lower in entry['notes'].lower()):
            found_entries.append(entry)

    if not found_entries:
        print(f"No entries found matching '{keyword}'.")
        return

    print(f"\n--- Search Results for '{keyword}' ---")
    for i, entry in enumerate(found_entries):
        print(f"Result #{i+1}:")
        print(f"  Timestamp: {entry['timestamp']}")
        print(f"  Item: {entry['item']}")
        print(f"  Location: {entry['location']}")
        print(f"  Quantity: {entry['quantity']}")
        print(f"  Notes: {entry['notes']}")
        print("-" * 20)
    print("--- End of Search Results ---")

def main():
    parser = argparse.ArgumentParser(
        description="A command-line utility for logging scavenged resources."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new scavenged item entry.')
    add_parser.add_argument('--item', required=True, help='Name of the scavenged item.')
    add_parser.add_argument('--location', required=True, help='Location where the item was found.')
    add_parser.add_argument('--quantity', type=int, default=1, help='Quantity of the item found.')
    add_parser.add_argument('--notes', default='No specific notes.', help='Any additional notes about the item.')

    # View command
    view_parser = subparsers.add_parser('view', help='View all entries in the scavenger log.')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search for entries by keyword.')
    search_parser.add_argument('--keyword', required=True, help='Keyword to search for in item, location, or notes.')

    args = parser.parse_args()

    if args.command == 'add':
        add_entry(args.item, args.location, args.quantity, args.notes)
    elif args.command == 'view':
        view_log()
    elif args.command == 'search':
        search_log(args.keyword)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
