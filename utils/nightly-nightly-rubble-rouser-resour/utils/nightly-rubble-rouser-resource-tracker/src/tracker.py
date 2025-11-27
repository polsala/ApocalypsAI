import argparse
import json
import os

DATA_FILE = 'resources.json'

def _load_data(data_file=DATA_FILE):
    """Loads resource data from the JSON file."""
    if not os.path.exists(data_file):
        return {}
    with open(data_file, 'r') as f:
        return json.load(f)

def _save_data(data, data_file=DATA_FILE):
    """Saves resource data to the JSON file."""
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

def add_resource(stash_name, item_name, quantity, data_file=DATA_FILE):
    """Adds a specified quantity of an item to a stash."""
    data = _load_data(data_file)
    stash = data.setdefault(stash_name, {})
    stash[item_name] = stash.get(item_name, 0) + quantity
    _save_data(data, data_file)
    print(f"Added {quantity} '{item_name}' to '{stash_name}'. Current: {stash[item_name]}")

def remove_resource(stash_name, item_name, quantity, data_file=DATA_FILE):
    """Removes a specified quantity of an item from a stash."""
    data = _load_data(data_file)
    if stash_name not in data or item_name not in data[stash_name]:
        print(f"Error: '{item_name}' not found in '{stash_name}'.")
        return

    current_quantity = data[stash_name][item_name]
    if current_quantity < quantity:
        print(f"Warning: Trying to remove {quantity} '{item_name}' from '{stash_name}', but only {current_quantity} available. Removing all {current_quantity}.")
        data[stash_name][item_name] = 0
    else:
        data[stash_name][item_name] -= quantity

    if data[stash_name][item_name] <= 0:
        del data[stash_name][item_name]
        if not data[stash_name]: # If stash becomes empty, remove it
            del data[stash_name]

    _save_data(data, data_file)
    print(f"Removed {quantity} '{item_name}' from '{stash_name}'. Remaining: {data.get(stash_name, {}).get(item_name, 0)}")

def list_resources(stash_name=None, data_file=DATA_FILE):
    """Lists resources in a specific stash or all stashes."""
    data = _load_data(data_file)
    if not data:
        print("No resources tracked yet. Start by adding some!")
        return

    if stash_name:
        if stash_name in data:
            print(f"\nResources in '{stash_name}':")
            if not data[stash_name]:
                print("  (Stash is empty)")
            for item, quantity in data[stash_name].items():
                print(f"  - {item}: {quantity}")
        else:
            print(f"Error: Stash '{stash_name}' not found.")
    else:
        print("\nAll Stashes and Resources:")
        for stash, items in data.items():
            print(f"  '{stash}':")
            if not items:
                print("    (Stash is empty)")
            for item, quantity in items.items():
                print(f"    - {item}: {quantity}")

def total_item(item_name, data_file=DATA_FILE):
    """Calculates the total quantity of an item across all stashes."""
    data = _load_data(data_file)
    total = 0
    for stash, items in data.items():
        total += items.get(item_name, 0)
    print(f"\nTotal '{item_name}' across all stashes: {total}")

def main():
    parser = argparse.ArgumentParser(description="Rubble-Rouser Resource Tracker: Manage your scavenged supplies.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add resources to a stash.')
    add_parser.add_argument('stash', type=str, help='Name of the stash.')
    add_parser.add_argument('item', type=str, help='Name of the item.')
    add_parser.add_argument('quantity', type=int, help='Quantity to add.')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove resources from a stash.')
    remove_parser.add_argument('stash', type=str, help='Name of the stash.')
    remove_parser.add_argument('item', type=str, help='Name of the item.')
    remove_parser.add_argument('quantity', type=int, help='Quantity to remove.')

    # List command
    list_parser = subparsers.add_parser('list', help='List resources in a stash or all stashes.')
    list_parser.add_argument('stash', type=str, nargs='?', help='(Optional) Name of the stash to list. If omitted, lists all stashes.')

    # Total command
    total_parser = subparsers.add_parser('total', help='Get the total quantity of an item across all stashes.')
    total_parser.add_argument('item', type=str, help='Name of the item.')

    args = parser.parse_args()

    if args.command == 'add':
        add_resource(args.stash, args.item, args.quantity)
    elif args.command == 'remove':
        remove_resource(args.stash, args.item, args.quantity)
    elif args.command == 'list':
        list_resources(args.stash)
    elif args.command == 'total':
        total_item(args.item)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
