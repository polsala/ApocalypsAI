import argparse
import json
import os
from datetime import datetime

LOG_FILE = 'scavenger_log.json'

def load_log():
    """Loads the log data from the JSON file."""
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {LOG_FILE} is corrupted or empty. Starting with an empty log.")
        return []

def save_log(log_data):
    """Saves the log data to the JSON file."""
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)

def add_entry(item, category="Misc", condition="Unknown", location="Unspecified"):
    """Adds a new entry to the log."""
    log_data = load_log()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": timestamp,
        "item": item,
        "category": category,
        "condition": condition,
        "location": location
    }
    log_data.append(entry)
    save_log(log_data)
    print(f"Logged: '{item}' successfully.")

def list_entries():
    """Lists all entries in the log."""
    log_data = load_log()
    if not log_data:
        print("The Scavenger's Scrutiny Log is empty. Go forth and scavenge!")
        return

    print("\n--- Scavenger's Scrutiny Log ---")
    for entry in log_data:
        print(f"[{entry['timestamp']}] Item: {entry['item']}, Category: {entry['category']}, Condition: {entry['condition']}, Location: {entry['location']}")
    print("----------------------------------\n")

def search_entries(query=None, category=None, location=None):
    """Searches entries based on query, category, or location."""
    log_data = load_log()
    if not log_data:
        print("The Scavenger's Scrutiny Log is empty. Nothing to search.")
        return

    results = []
    for entry in log_data:
        match = True
        if query and query.lower() not in entry['item'].lower():
            match = False
        if category and category.lower() != entry['category'].lower():
            match = False
        if location and location.lower() not in entry['location'].lower():
            match = False
        
        if match:
            results.append(entry)
    
    if not results:
        print("No matching entries found.")
        return

    print("\n--- Scavenger's Scrutiny Search Results ---")
    for entry in results:
        print(f"[{entry['timestamp']}] Item: {entry['item']}, Category: {entry['category']}, Condition: {entry['condition']}, Location: {entry['location']}")
    print("-------------------------------------------\n")


def main():
    parser = argparse.ArgumentParser(
        description="A Scavenger's Scrutiny Log for tracking findings.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new finding to the log.')
    add_parser.add_argument('--item', required=True, help='The name of the item found.')
    add_parser.add_argument('--category', default='Misc', help='The category of the item (e.g., Food, Tool, Weapon).')
    add_parser.add_argument('--condition', default='Unknown', help='The condition of the item (e.g., Good, Damaged, Broken).')
    add_parser.add_argument('--location', default='Unspecified', help='Where the item was found or stored.')

    # List command
    list_parser = subparsers.add_parser('list', help='List all logged findings.')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search for specific items.')
    search_parser.add_argument('--query', help='A keyword to search for in item names.')
    search_parser.add_argument('--category', help='Filter by item category.')
    search_parser.add_argument('--location', help='Filter by item location.')

    args = parser.parse_args()

    if args.command == 'add':
        add_entry(args.item, args.category, args.condition, args.location)
    elif args.command == 'list':
        list_entries()
    elif args.command == 'search':
        if not any([args.query, args.category, args.location]):
            print("Error: 'search' command requires at least one of --query, --category, or --location.")
            parser.print_help(search_parser)
        else:
            search_entries(args.query, args.category, args.location)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
