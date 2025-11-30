import argparse
import json
import os
from typing import Dict

DATA_FILE = os.path.join(os.path.dirname(__file__), 'resources.json')

def load_resources() -> Dict[str, int]:
    """Loads resources from the data file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode {DATA_FILE}. Starting with empty inventory.")
        return {}
    except Exception as e:
        print(f"Error loading resources: {e}. Starting with empty inventory.")
        return {}

def save_resources(resources: Dict[str, int]):
    """Saves resources to the data file."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(resources, f, indent=4)
    except Exception as e:
        print(f"Error saving resources: {e}")

def add_resource(item_name: str, quantity: int):
    """Adds or updates a resource."""
    if quantity <= 0:
        print("Quantity must be a positive number, survivor!")
        return

    resources = load_resources()
    resources[item_name] = resources.get(item_name, 0) + quantity
    save_resources(resources)
    print(f"Added {quantity}x {item_name}. Total: {resources[item_name]}x.")

def remove_resource(item_name: str, quantity: int):
    """Removes a quantity of a resource."""
    if quantity <= 0:
        print("Quantity to remove must be a positive number, survivor!")
        return

    resources = load_resources()
    if item_name not in resources:
        print(f"Can't remove {item_name}. You don't seem to have any, survivor!")
        return

    current_quantity = resources[item_name]
    if current_quantity <= quantity:
        del resources[item_name]
        print(f"Used up all {item_name}. It's gone, survivor!")
    else:
        resources[item_name] -= quantity
        print(f"Removed {quantity}x {item_name}. Remaining: {resources[item_name]}x.")
    save_resources(resources)

def list_resources():
    """Lists all tracked resources."""
    resources = load_resources()
    if not resources:
        print("Your inventory is empty, survivor. Time to scavenge!")
        return

    print("\n--- Current Inventory ---")
    for item, quantity in sorted(resources.items()):
        print(f"- {item}: {quantity}x")
    print("-------------------------\n")

def main():
    parser = argparse.ArgumentParser(
        description="Rubble-Rouser Resource Tracker: Manage your scavenged supplies."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a resource to your inventory.')
    add_parser.add_argument('item_name', type=str, help='Name of the resource (e.g., "Canned Beans")')
    add_parser.add_argument('quantity', type=int, help='Quantity to add')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a resource from your inventory.')
    remove_parser.add_argument('item_name', type=str, help='Name of the resource')
    remove_parser.add_argument('quantity', type=int, help='Quantity to remove')

    # List command
    list_parser = subparsers.add_parser('list', help='List all resources in your inventory.')

    args = parser.parse_args()

    if args.command == 'add':
        add_resource(args.item_name, args.quantity)
    elif args.command == 'remove':
        remove_resource(args.item_name, args.quantity)
    elif args.command == 'list':
        list_resources()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
