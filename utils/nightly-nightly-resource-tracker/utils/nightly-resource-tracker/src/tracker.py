import argparse
import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'resources.json')

def load_data():
    """Loads resource data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {DATA_FILE} is corrupted. Starting with empty data.")
        return []

def save_data(data):
    """Saves resource data to the JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_entry(resource_name, amount, entry_type):
    """Adds a new resource entry."""
    if not isinstance(amount, (int, float)) or amount <= 0:
        print("Error: Amount must be a positive number.")
        return

    data = load_data()
    timestamp = datetime.now().isoformat()
    
    # Convert amount to negative for consumption, keep positive for production
    effective_amount = -amount if entry_type == 'consumption' else amount

    entry = {
        'timestamp': timestamp,
        'resource': resource_name.lower(),
        'amount': effective_amount,
        'type': entry_type
    }
    data.append(entry)
    save_data(data)
    print(f"Logged {entry_type} of {amount} {resource_name}.")

def get_daily_summary():
    """Calculates the net change for each resource for the current day."""
    data = load_data()
    today_str = datetime.now().date().isoformat()
    
    summary = {}
    for entry in data:
        entry_date_str = datetime.fromisoformat(entry['timestamp']).date().isoformat()
        if entry_date_str == today_str:
            resource = entry['resource']
            summary[resource] = summary.get(resource, 0) + entry['amount']
    return summary

def get_history():
    """Returns all logged entries."""
    return load_data()

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Resource Tracker: Manage your essential supplies."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Log a resource transaction')
    add_parser.add_argument('resource_name', type=str, help='Name of the resource')
    add_parser.add_argument('amount', type=float, help='Amount of the resource')
    add_parser.add_argument('--type', type=str, choices=['consumption', 'production'], 
                            default='consumption', help='Type of transaction')

    # Summary command
    summary_parser = subparsers.add_parser('summary', help='View daily net changes')

    # History command
    history_parser = subparsers.add_parser('history', help='View all logged entries')

    args = parser.parse_args()

    if args.command == 'add':
        add_entry(args.resource_name, args.amount, args.type)
    elif args.command == 'summary':
        summary = get_daily_summary()
        if summary:
            print(f"--- Daily Summary for {datetime.now().date().isoformat()} ---")
            for resource, net_change in summary.items():
                print(f"  {resource.capitalize()}: {net_change:+}")
            print("--------------------------------------")
        else:
            print("No resource activity logged for today.")
    elif args.command == 'history':
        history = get_history()
        if history:
            print("--- Resource History ---")
            for entry in history:
                print(f"[{entry['timestamp']}] {entry['type'].capitalize()} of {abs(entry['amount'])} {entry['resource'].capitalize()} (Net: {entry['amount']:+})")
            print("------------------------")
        else:
            print("No resource history found.")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
