import argparse
import json
import os

DATA_FILE = 'resources.json'

def _get_data_path():
    """Returns the absolute path to the data file, relative to the script's directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, DATA_FILE)

def _load_data():
    """Loads resource data from the JSON file."""
    data_path = _get_data_path()
    if not os.path.exists(data_path):
        return {}
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {DATA_FILE} is corrupted. Starting with empty resources.")
        return {}

def _save_data(data):
    """Saves resource data to the JSON file."""
    data_path = _get_data_path()
    with open(data_path, 'w') as f:
        json.dump(data, f, indent=4)

def add_resource(name: str, quantity: int):
    """Adds or updates a resource with the given quantity."""
    if quantity <= 0:
        print("Quantity must be positive.")
        return

    resources = _load_data()
    resources[name] = resources.get(name, 0) + quantity
    _save_data(resources)
    print(f"Added {quantity} of '{name}'. Current total: {resources[name]}")

def consume_resource(name: str, quantity: int):
    """Consumes a resource, reducing its quantity. Prevents over-consumption."""
    if quantity <= 0:
        print("Quantity must be positive.")
        return

    resources = _load_data()
    if name not in resources or resources[name] < quantity:
        current = resources.get(name, 0)
        print(f"Error: Not enough '{name}' to consume {quantity}. Available: {current}")
        return False

    resources[name] -= quantity
    if resources[name] == 0:
        del resources[name] # Remove if quantity drops to zero
    _save_data(resources)
    print(f"Consumed {quantity} of '{name}'. Remaining: {resources.get(name, 0)}")
    return True

def list_resources():
    """Lists all currently tracked resources and their quantities."""
    resources = _load_data()
    if not resources:
        print("No resources currently tracked. Time to scavenge!")
        return

    print("--- Current Resources ---")
    for name, quantity in sorted(resources.items()):
        print(f"- {name}: {quantity}")
    print("-------------------------")

def main():
    parser = argparse.ArgumentParser(
        description="Post-Apocalyptic Resource Tracker: Manage your vital supplies."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a resource or increase its quantity')
    add_parser.add_argument('name', type=str, help='Name of the resource')
    add_parser.add_argument('quantity', type=int, help='Quantity to add')

    # Consume command
    consume_parser = subparsers.add_parser('consume', help='Consume a resource')
    consume_parser.add_argument('name', type=str, help='Name of the resource')
    consume_parser.add_argument('quantity', type=int, help='Quantity to consume')

    # List command
    list_parser = subparsers.add_parser('list', help='List all tracked resources')

    args = parser.parse_args()

    if args.command == 'add':
        add_resource(args.name, args.quantity)
    elif args.command == 'consume':
        consume_resource(args.name, args.quantity)
    elif args.command == 'list':
        list_resources()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
