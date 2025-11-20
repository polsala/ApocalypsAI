import json
import os
import sys

DATA_FILE = 'resources.json'

def _load_resources():
    """Loads resources from the data file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def _save_resources(resources):
    """Saves resources to the data file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(resources, f, indent=4)

def add_resource(item_name, quantity):
    """Adds or updates a resource."""
    try:
        quantity = int(quantity)
        if quantity <= 0:
            print("Quantity must be a positive integer.", file=sys.stderr)
            return
    except ValueError:
        print("Quantity must be an integer.", file=sys.stderr)
        return

    resources = _load_resources()
    resources[item_name] = resources.get(item_name, 0) + quantity
    _save_resources(resources)
    print(f"Added {quantity} of '{item_name}'. Current total: {resources[item_name]}")

def list_resources():
    """Lists all resources."""
    resources = _load_resources()
    if not resources:
        print("Your stash is currently empty. Time to scavenge!")
        return

    print("\n--- Current Stash ---")
    for item, qty in sorted(resources.items()):
        print(f"- {item}: {qty}")
    print("---------------------\n")

def consume_resource(item_name, quantity):
    """Consumes a resource."""
    try:
        quantity = int(quantity)
        if quantity <= 0:
            print("Quantity to consume must be a positive integer.", file=sys.stderr)
            return
    except ValueError:
        print("Quantity must be an integer.", file=sys.stderr)
        return

    resources = _load_resources()
    if item_name not in resources:
        print(f"'{item_name}' not found in your stash.", file=sys.stderr)
        return

    current_qty = resources[item_name]
    if current_qty < quantity:
        print(f"Not enough '{item_name}' to consume. You only have {current_qty}.", file=sys.stderr)
        return

    resources[item_name] -= quantity
    if resources[item_name] <= 0:
        del resources[item_name]
        print(f"Consumed all {current_qty} of '{item_name}'. Item removed from stash.")
    else:
        print(f"Consumed {quantity} of '{item_name}'. Remaining: {resources[item_name]}")
    _save_resources(resources)

def clear_resources():
    """Clears all resources."""
    _save_resources({})
    print("Stash cleared! Ready for a fresh start.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python tracker.py <command> [args...]", file=sys.stderr)
        print("Commands: add <item> <quantity>, list, consume <item> <quantity>, clear", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) != 4:
            print("Usage: python tracker.py add <item_name> <quantity>", file=sys.stderr)
            sys.exit(1)
        add_resource(sys.argv[2], sys.argv[3])
    elif command == 'list':
        if len(sys.argv) != 2:
            print("Usage: python tracker.py list", file=sys.stderr)
            sys.exit(1)
        list_resources()
    elif command == 'consume':
        if len(sys.argv) != 4:
            print("Usage: python tracker.py consume <item_name> <quantity>", file=sys.stderr)
            sys.exit(1)
        consume_resource(sys.argv[2], sys.argv[3])
    elif command == 'clear':
        if len(sys.argv) != 2:
            print("Usage: python tracker.py clear", file=sys.stderr)
            sys.exit(1)
        clear_resources()
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
