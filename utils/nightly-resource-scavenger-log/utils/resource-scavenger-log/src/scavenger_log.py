import argparse
import json
import os
from datetime import datetime
from collections import defaultdict

DATA_FILE = 'resources.json'

def _get_data_path():
    """Returns the absolute path to the data file."""
    return os.path.join(os.path.dirname(__file__), DATA_FILE)

def _load_resources():
    """Loads resources from the JSON data file."""
    data_path = _get_data_path()
    if not os.path.exists(data_path):
        return []
    with open(data_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {DATA_FILE} is corrupted. Starting with an empty log.")
            return []

def _save_resources(resources):
    """Saves resources to the JSON data file."""
    data_path = _get_data_path()
    with open(data_path, 'w') as f:
        json.dump(resources, f, indent=2)

def add_resource(resource_name, quantity, unit, location, date=None):
    """Adds a new resource entry to the log."""
    resources = _load_resources()
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    new_entry = {
        'resource': resource_name,
        'quantity': quantity,
        'unit': unit,
        'location': location,
        'date': date
    }
    resources.append(new_entry)
    _save_resources(resources)
    print(f"Added: {quantity} {unit} of {resource_name} at {location} on {date}")

def list_resources():
    """Lists all logged resources."""
    resources = _load_resources()
    if not resources:
        print("No resources logged yet. Go scavenge!")
        return

    print("\n--- Logged Resources ---")
    for i, entry in enumerate(resources):
        print(f"[{i+1}] Resource: {entry['resource']}")
        print(f"    Quantity: {entry['quantity']} {entry['unit']}")
        print(f"    Location: {entry['location']}")
        print(f"    Date:     {entry['date']}")
        print("------------------------")

def generate_report():
    """Generates a summary report of resources."""
    resources = _load_resources()
    if not resources:
        print("No resources logged yet to generate a report.")
        return

    summary = defaultdict(lambda: defaultdict(int))
    for entry in resources:
        resource_name = entry['resource']
        unit = entry['unit']
        quantity = entry['quantity']
        summary[resource_name][unit] += quantity

    print("\n--- Resource Summary Report ---")
    for resource_name, units_data in summary.items():
        print(f"Resource: {resource_name}")
        for unit, total_quantity in units_data.items():
            print(f"    Total: {total_quantity} {unit}")
    print("-------------------------------")

def main():
    parser = argparse.ArgumentParser(
        description="A post-apocalyptic resource scavenger log utility."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new resource entry')
    add_parser.add_argument('--resource', required=True, help='Name of the resource')
    add_parser.add_argument('--quantity', type=int, required=True, help='Quantity of the resource')
    add_parser.add_argument('--unit', required=True, help='Unit of measurement (e.g., cans, kg)')
    add_parser.add_argument('--location', required=True, help='Location where the resource was found')
    add_parser.add_argument('--date', help='Date of discovery (YYYY-MM-DD). Defaults to today.')
    add_parser.set_defaults(func=lambda args: add_resource(args.resource, args.quantity, args.unit, args.location, args.date))

    # List command
    list_parser = subparsers.add_parser('list', help='List all logged resources')
    list_parser.set_defaults(func=lambda args: list_resources())

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate a summary report of resources')
    report_parser.set_defaults(func=lambda args: generate_report())

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
