import sys
import os

RESOURCE_FILE = 'resources.txt'

def _load_resources():
    """Loads resources from the RESOURCE_FILE into a dictionary."""
    resources = {}
    if not os.path.exists(RESOURCE_FILE):
        return resources

    try:
        with open(RESOURCE_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or '=' not in line:
                    continue
                item, quantity_str = line.split('=', 1)
                try:
                    resources[item] = int(quantity_str)
                except ValueError:
                    print(f"Warning: Invalid quantity for '{item}' in {RESOURCE_FILE}. Skipping.", file=sys.stderr)
    except IOError as e:
        print(f"Error reading {RESOURCE_FILE}: {e}", file=sys.stderr)
    return resources

def _save_resources(resources):
    """Saves the resources dictionary back to the RESOURCE_FILE."""
    try:
        with open(RESOURCE_FILE, 'w') as f:
            for item, quantity in resources.items():
                f.write(f"{item}={quantity}\n")
    except IOError as e:
        print(f"Error writing to {RESOURCE_FILE}: {e}", file=sys.stderr)

def add_resource(item: str, quantity: int):
    """Adds or updates a resource's quantity."""
    if not item or quantity <= 0:
        print("Error: Item name cannot be empty and quantity must be positive.", file=sys.stderr)
        return

    resources = _load_resources()
    resources[item] = resources.get(item, 0) + quantity
    _save_resources(resources)
    print(f"Added {quantity} of '{item}'. New total: {resources[item]}")

def remove_resource(item: str, quantity: int):
    """Removes a quantity of a resource. Removes item if quantity <= 0."""
    if not item or quantity <= 0:
        print("Error: Item name cannot be empty and quantity must be positive.", file=sys.stderr)
        return

    resources = _load_resources()
    if item not in resources:
        print(f"Error: '{item}' not found in resources.", file=sys.stderr)
        return

    resources[item] -= quantity
    if resources[item] <= 0:
        del resources[item]
        print(f"Removed '{item}'. Item depleted and removed from list.")
    else:
        print(f"Removed {quantity} of '{item}'. New total: {resources[item]}")
    _save_resources(resources)

def list_resources():
    """Lists all current resources and their quantities."""
    resources = _load_resources()
    if not resources:
        print("No resources tracked yet. Add some with 'add' command.")
        return

    print("\n--- Current Resources ---")
    for item, quantity in sorted(resources.items()):
        print(f"{item}: {quantity}")
    print("-------------------------")

def main():
    if len(sys.argv) < 2:
        print("Usage: python tracker.py <command> [args...]", file=sys.stderr)
        print("Commands: add <item_name> <quantity>, remove <item_name> <quantity>, list", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'add':
        if len(sys.argv) != 4:
            print("Usage: python tracker.py add <item_name> <quantity>", file=sys.stderr)
            sys.exit(1)
        item_name = sys.argv[2]
        try:
            quantity = int(sys.argv[3])
            add_resource(item_name, quantity)
        except ValueError:
            print("Error: Quantity must be an integer.", file=sys.stderr)
            sys.exit(1)
    elif command == 'remove':
        if len(sys.argv) != 4:
            print("Usage: python tracker.py remove <item_name> <quantity>", file=sys.stderr)
            sys.exit(1)
        item_name = sys.argv[2]
        try:
            quantity = int(sys.argv[3])
            remove_resource(item_name, quantity)
        except ValueError:
            print("Error: Quantity must be an integer.", file=sys.stderr)
            sys.exit(1)
    elif command == 'list':
        if len(sys.argv) != 2:
            print("Usage: python tracker.py list", file=sys.stderr)
            sys.exit(1)
        list_resources()
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Commands: add, remove, list", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
