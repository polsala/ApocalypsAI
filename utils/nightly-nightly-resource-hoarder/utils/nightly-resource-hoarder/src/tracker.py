import json
import os
import sys
import argparse

RESOURCE_FILE = 'resources.json'

def load_resources(file_path=RESOURCE_FILE):
    """Loads resources from a JSON file."""
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {file_path} is corrupted or empty. Starting with an empty inventory.", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Error loading resources from {file_path}: {e}", file=sys.stderr)
        return {}

def save_resources(resources, file_path=RESOURCE_FILE):
    """Saves resources to a JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(resources, f, indent=4)
    except Exception as e:
        print(f"Error saving resources to {file_path}: {e}", file=sys.stderr)

def add_resource(resources, item_name, quantity):
    """Adds or updates a resource item with the given quantity."""
    if not isinstance(quantity, int) or quantity <= 0:
        print(f"Error: Quantity must be a positive integer.", file=sys.stderr)
        return False
    
    item_name = item_name.strip().title() # Normalize name
    resources[item_name] = resources.get(item_name, 0) + quantity
    print(f"Added {quantity}x {item_name}. Total: {resources[item_name]}")
    return True

def remove_resource(resources, item_name, quantity):
    """Removes a given quantity from a resource item. Removes item if quantity drops to 0 or less."""
    if not isinstance(quantity, int) or quantity <= 0:
        print(f"Error: Quantity to remove must be a positive integer.", file=sys.stderr)
        return False

    item_name = item_name.strip().title() # Normalize name
    if item_name not in resources:
        print(f"Error: '{item_name}' not found in resources.", file=sys.stderr)
        return False

    current_quantity = resources[item_name]
    if current_quantity <= quantity:
        del resources[item_name]
        print(f"Removed all {current_quantity}x {item_name}. Item removed from inventory.")
    else:
        resources[item_name] -= quantity
        print(f"Removed {quantity}x {item_name}. Remaining: {resources[item_name]}")
    return True

def list_resources(resources):
    """Lists all resources and their quantities."""
    if not resources:
        print("Your resource inventory is empty. Time to start hoarding!")
        return

    print("\n--- Current Resource Inventory ---")
    for item, quantity in sorted(resources.items()):
        print(f"- {item}: {quantity}")
    print("----------------------------------")

def main():
    parser = argparse.ArgumentParser(
        description="A simple CLI tool for tracking essential resources.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add or update a resource item.')
    add_parser.add_argument('item', type=str, help='Name of the resource item.')
    add_parser.add_argument('quantity', type=int, help='Quantity to add (must be positive integer).')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a quantity from a resource item.')
    remove_parser.add_argument('item', type=str, help='Name of the resource item.')
    remove_parser.add_argument('quantity', type=int, help='Quantity to remove (must be positive integer).')

    # List command
    list_parser = subparsers.add_parser('list', help='List all current resources.')

    args = parser.parse_args()

    resources = load_resources()

    if args.command == 'add':
        if add_resource(resources, args.item, args.quantity):
            save_resources(resources)
    elif args.command == 'remove':
        if remove_resource(resources, args.item, args.quantity):
            save_resources(resources)
    elif args.command == 'list':
        list_resources(resources)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
