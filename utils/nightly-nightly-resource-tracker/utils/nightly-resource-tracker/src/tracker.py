import argparse
import os

RESOURCE_FILE = 'resources.txt'

def _load_resources():
    """Loads resources from the RESOURCE_FILE."""
    resources = {}
    if not os.path.exists(RESOURCE_FILE):
        return resources

    try:
        with open(RESOURCE_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    name, quantity_str = line.split(',', 1)
                    quantity = int(quantity_str)
                    if quantity < 0:
                        print(f"Warning: Negative quantity found for '{name}'. Skipping.")
                        continue
                    resources[name] = quantity
                except ValueError:
                    print(f"Warning: Malformed line in {RESOURCE_FILE}: '{line}'. Skipping.")
    except IOError as e:
        print(f"Error loading resources from {RESOURCE_FILE}: {e}")
    return resources

def _save_resources(resources):
    """Saves resources to the RESOURCE_FILE."""
    try:
        with open(RESOURCE_FILE, 'w') as f:
            for name, quantity in resources.items():
                f.write(f"{name},{quantity}\n")
    except IOError as e:
        print(f"Error saving resources to {RESOURCE_FILE}: {e}")

def add_resource(name, quantity):
    """Adds or updates a resource's quantity."""
    if quantity <= 0:
        print("Error: Quantity must be a positive integer.")
        return

    resources = _load_resources()
    resources[name] = resources.get(name, 0) + quantity
    _save_resources(resources)
    print(f"Added {quantity} of '{name}'. New total: {resources[name]}")

def remove_resource(name, quantity):
    """Removes a resource's quantity."""
    if quantity <= 0:
        print("Error: Quantity must be a positive integer.")
        return

    resources = _load_resources()
    if name not in resources:
        print(f"Error: Resource '{name}' not found.")
        return

    if resources[name] < quantity:
        print(f"Error: Not enough '{name}' to remove. Available: {resources[name]}, trying to remove: {quantity}")
        return

    resources[name] -= quantity
    if resources[name] == 0:
        del resources[name]
    _save_resources(resources)
    print(f"Removed {quantity} of '{name}'. Remaining: {resources.get(name, 0)}")

def list_resources():
    """Lists all tracked resources."""
    resources = _load_resources()
    if not resources:
        print("No resources tracked yet.")
        return

    print("--- Current Resources ---")
    for name, quantity in sorted(resources.items()):
        print(f"{name}: {quantity}")
    print("-------------------------")

def main():
    parser = argparse.ArgumentParser(description="ApocalypsAI Nightly Resource Tracker")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a resource or increase its quantity')
    add_parser.add_argument('name', type=str, help='Name of the resource')
    add_parser.add_argument('quantity', type=int, help='Quantity to add')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a resource or decrease its quantity')
    remove_parser.add_argument('name', type=str, help='Name of the resource')
    remove_parser.add_argument('quantity', type=int, help='Quantity to remove')

    # List command
    list_parser = subparsers.add_parser('list', help='List all tracked resources')

    args = parser.parse_args()

    if args.command == 'add':
        add_resource(args.name, args.quantity)
    elif args.command == 'remove':
        remove_resource(args.name, args.quantity)
    elif args.command == 'list':
        list_resources()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
