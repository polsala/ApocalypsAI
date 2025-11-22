import json
import os
import sys
from collections import defaultdict

DATA_FILE = "resources.json"

def load_resources(file_path):
    """Loads resources from a JSON file."""
    if not os.path.exists(file_path):
        return defaultdict(int)
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Ensure all values are integers and handle potential non-int values gracefully
            return defaultdict(int, {k: int(v) for k, v in data.items() if isinstance(v, (int, str)) and str(v).isdigit()})
    except (json.JSONDecodeError, ValueError):
        print(f"Warning: Could not read or parse {file_path}. Starting with an empty inventory.", file=sys.stderr)
        return defaultdict(int)

def save_resources(file_path, resources):
    """Saves resources to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(dict(resources), f, indent=4)

def add_resource(resources, name, quantity):
    """Adds a quantity to a resource."""
    if quantity < 0:
        print("Quantity to add cannot be negative.", file=sys.stderr)
        return
    resources[name] += quantity
    print(f"Added {quantity} of '{name}'. New total: {resources[name]}")

def remove_resource(resources, name, quantity):
    """Removes a quantity from a resource."""
    if quantity < 0:
        print("Quantity to remove cannot be negative.", file=sys.stderr)
        return
    if name not in resources or resources[name] == 0:
        print(f"'{name}' not found or quantity is already zero. Cannot remove.", file=sys.stderr)
        return
    
    resources[name] = max(0, resources[name] - quantity)
    print(f"Removed {quantity} of '{name}'. New total: {resources[name]}")

def set_resource(resources, name, quantity):
    """Sets the quantity of a resource."""
    if quantity < 0:
        print("Quantity cannot be negative.", file=sys.stderr)
        return
    resources[name] = quantity
    print(f"Set '{name}' quantity to {resources[name]}")

def list_resources(resources):
    """Lists all resources and their quantities."""
    if not resources:
        print("Your inventory is empty. Time to scavenge!")
        return

    print("\n--- Current Inventory ---")
    for name, quantity in sorted(resources.items()):
        print(f"- {name}: {quantity}")
    print("-------------------------\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python tracker.py <command> [args...]")
        print("Commands: add <name> <quantity>, remove <name> <quantity>, set <name> <quantity>, list")
        sys.exit(1)

    command = sys.argv[1]
    
    # Determine the absolute path for the data file relative to the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, DATA_FILE)

    resources = load_resources(data_file_path)

    if command == "add":
        if len(sys.argv) != 4:
            print("Usage: python tracker.py add <name> <quantity>", file=sys.stderr)
            sys.exit(1)
        name = sys.argv[2]
        try:
            quantity = int(sys.argv[3])
        except ValueError:
            print("Quantity must be an integer.", file=sys.stderr)
            sys.exit(1)
        add_resource(resources, name, quantity)
        save_resources(data_file_path, resources)
    elif command == "remove":
        if len(sys.argv) != 4:
            print("Usage: python tracker.py remove <name> <quantity>", file=sys.stderr)
            sys.exit(1)
        name = sys.argv[2]
        try:
            quantity = int(sys.argv[3])
        except ValueError:
            print("Quantity must be an integer.", file=sys.stderr)
            sys.exit(1)
        remove_resource(resources, name, quantity)
        save_resources(data_file_path, resources)
    elif command == "set":
        if len(sys.argv) != 4:
            print("Usage: python tracker.py set <name> <quantity>", file=sys.stderr)
            sys.exit(1)
        name = sys.argv[2]
        try:
            quantity = int(sys.argv[3])
        except ValueError:
            print("Quantity must be an integer.", file=sys.stderr)
            sys.exit(1)
        set_resource(resources, name, quantity)
        save_resources(data_file_path, resources)
    elif command == "list":
        list_resources(resources)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Commands: add, remove, set, list", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
