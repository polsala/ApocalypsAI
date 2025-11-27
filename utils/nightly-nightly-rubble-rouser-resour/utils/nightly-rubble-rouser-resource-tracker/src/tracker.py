import argparse
import json
import os

RESOURCE_FILE = 'resources.json'

def load_resources(filepath=RESOURCE_FILE):
    """Loads resources from a JSON file."""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {filepath} is corrupted. Starting with an empty inventory.")
        return {}
    except Exception as e:
        print(f"Error loading resources from {filepath}: {e}")
        return {}

def save_resources(resources, filepath=RESOURCE_FILE):
    """Saves resources to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(resources, f, indent=4)
    except Exception as e:
        print(f"Error saving resources to {filepath}: {e}")

def add_resource(resources, location, item, quantity):
    """Adds a new resource or updates an existing one at a location."""
    if location not in resources:
        resources[location] = {}
    resources[location][item] = resources[location].get(item, 0) + quantity
    print(f"Added {quantity}x {item} to {location}. New total: {resources[location][item]}")
    return resources

def update_resource(resources, location, item, quantity):
    """Sets the quantity of an existing resource at a location."""
    if location not in resources or item not in resources[location]:
        print(f"Error: Item '{item}' not found at location '{location}'. Use 'add' to create it.")
        return resources
    resources[location][item] = quantity
    print(f"Updated {item} at {location} to {quantity}.")
    return resources

def list_resources(resources, location=None, item=None):
    """Lists resources, optionally filtered by location or item."""
    if not resources:
        print("No resources tracked yet. Use 'add' to start.")
        return

    if location and item:
        if location in resources and item in resources[location]:
            print(f"  {location}: {item} x{resources[location][item]}")
        else:
            print(f"Item '{item}' not found at location '{location}'.")
    elif location:
        if location in resources:
            print(f"Resources at {location}:")
            for res_item, qty in resources[location].items():
                print(f"  - {res_item} x{qty}")
        else:
            print(f"Location '{location}' not found.")
    elif item:
        found = False
        print(f"'{item}' found across locations:")
        for loc, items in resources.items():
            if item in items:
                print(f"  - {loc}: x{items[item]}")
                found = True
        if not found:
            print(f"  No '{item}' found anywhere.")
    else:
        print("All Tracked Resources:")
        for loc, items in resources.items():
            print(f"  {loc}:")
            if not items:
                print("    (empty)")
            for res_item, qty in items.items():
                print(f"    - {res_item} x{qty}")

def main():
    parser = argparse.ArgumentParser(
        description="Track scavenged resources across locations."
    )
    parser.add_argument(
        '--file', default=RESOURCE_FILE,
        help=f"Path to the resource JSON file (default: {RESOURCE_FILE})"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add or increment a resource at a location.')
    add_parser.add_argument('--location', required=True, help='The location of the resource.')
    add_parser.add_argument('--item', required=True, help='The name of the resource item.')
    add_parser.add_argument('--quantity', type=int, default=1, help='Quantity to add (default: 1).')

    # Update command
    update_parser = subparsers.add_parser('update', help='Set the quantity of a resource at a location.')
    update_parser.add_argument('--location', required=True, help='The location of the resource.')
    update_parser.add_argument('--item', required=True, help='The name of the resource item.')
    update_parser.add_argument('--quantity', type=int, required=True, help='The new quantity for the resource.')

    # List command
    list_parser = subparsers.add_parser('list', help='List resources.')
    list_parser.add_argument('--location', help='Filter by location.')
    list_parser.add_argument('--item', help='Filter by item name.')

    args = parser.parse_args()

    resources = load_resources(args.file)

    if args.command == 'add':
        resources = add_resource(resources, args.location, args.item, args.quantity)
        save_resources(resources, args.file)
    elif args.command == 'update':
        resources = update_resource(resources, args.location, args.item, args.quantity)
        save_resources(resources, args.file)
    elif args.command == 'list':
        list_resources(resources, args.location, args.item)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
