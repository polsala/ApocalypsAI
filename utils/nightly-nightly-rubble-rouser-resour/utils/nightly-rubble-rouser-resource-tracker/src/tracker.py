import argparse
import json
import os

DATA_FILE = "resources.json"

def load_resources():
    """Loads resources from the JSON data file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {DATA_FILE} is corrupted. Starting with an empty inventory.")
        return {}

def save_resources(resources):
    """Saves resources to the JSON data file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(resources, f, indent=4)

def add_item(resources, name, quantity, category="misc"):
    """Adds or updates an item in the resources."""
    if not isinstance(quantity, int) or quantity <= 0:
        print("Error: Quantity must be a positive integer.")
        return False

    name = name.lower()
    category = category.lower()

    if name not in resources:
        resources[name] = {'quantity': 0, 'category': category}
    elif resources[name]['category'] != category:
        print(f"Warning: Item '{name}' already exists with category '{resources[name]['category']}'. Keeping existing category.")

    resources[name]['quantity'] += quantity
    print(f"Added {quantity} of '{name}' (Category: {resources[name]['category']}). Total: {resources[name]['quantity']}")
    return True

def remove_item(resources, name, quantity):
    """Removes a specified quantity of an item from resources."""
    if not isinstance(quantity, int) or quantity <= 0:
        print("Error: Quantity must be a positive integer.")
        return False

    name = name.lower()

    if name not in resources:
        print(f"Error: Item '{name}' not found in inventory.")
        return False

    current_quantity = resources[name]['quantity']
    if quantity >= current_quantity:
        print(f"Removed all {current_quantity} of '{name}'. Item depleted.")
        del resources[name]
    else:
        resources[name]['quantity'] -= quantity
        print(f"Removed {quantity} of '{name}'. Remaining: {resources[name]['quantity']}")
    return True

def list_items(resources, category=None):
    """Lists all items, optionally filtered by category."""
    if not resources:
        print("Your inventory is currently empty. Time to scavenge!")
        return

    print("\n--- Current Inventory ---")
    found_items = False
    for name, data in sorted(resources.items()):
        if category is None or data['category'].lower() == category.lower():
            print(f"  - {name.title()}: {data['quantity']} (Category: {data['category'].title()})")
            found_items = True
    if not found_items and category:
        print(f"No items found in category '{category}'.")
    print("-------------------------\n")

def get_summary(resources):
    """Prints a summary of resources by category."""
    if not resources:
        print("Your inventory is empty. No summary to provide.")
        return

    summary = {}
    for item_data in resources.values():
        cat = item_data['category'].lower()
        summary[cat] = summary.get(cat, 0) + item_data['quantity']

    print("\n--- Inventory Summary by Category ---")
    for cat, total_qty in sorted(summary.items()):
        print(f"  - {cat.title()}: {total_qty} items")
    print("-------------------------------------\n")

def main():
    parser = argparse.ArgumentParser(
        description="Rubble-Rouser Resource Tracker: Manage your post-apocalyptic inventory."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a resource to the inventory.')
    add_parser.add_argument('name', type=str, help='Name of the resource.')
    add_parser.add_argument('quantity', type=int, help='Quantity to add.')
    add_parser.add_argument('category', type=str, nargs='?', default='misc', help='Category of the resource (default: misc).')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a resource from the inventory.')
    remove_parser.add_argument('name', type=str, help='Name of the resource.')
    remove_parser.add_argument('quantity', type=int, help='Quantity to remove.')

    # List command
    list_parser = subparsers.add_parser('list', help='List all resources or filter by category.')
    list_parser.add_argument('category', type=str, nargs='?', help='Optional category to filter by.')

    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Show a summary of resources by category.')

    args = parser.parse_args()

    resources = load_resources()
    changed = False

    if args.command == 'add':
        if add_item(resources, args.name, args.quantity, args.category):
            changed = True
    elif args.command == 'remove':
        if remove_item(resources, args.name, args.quantity):
            changed = True
    elif args.command == 'list':
        list_items(resources, args.category)
    elif args.command == 'summary':
        get_summary(resources)
    else:
        parser.print_help()

    if changed:
        save_resources(resources)

if __name__ == '__main__':
    main()
