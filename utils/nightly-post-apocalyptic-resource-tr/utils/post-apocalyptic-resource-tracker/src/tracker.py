import argparse
import json
import os

DATA_FILE = "resources.json"

def load_resources():
    """Loads resources from the DATA_FILE. Returns an empty dict if file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_resources(resources):
    """Saves resources to the DATA_FILE."""
    with open(DATA_FILE, 'w') as f:
        json.dump(resources, f, indent=4)

def add_resource(resources, name, quantity):
    """Adds or increases the quantity of a resource."""
    resources[name] = resources.get(name, 0) + quantity
    print(f"Added {quantity} of {name}. Current: {resources[name]}")
    save_resources(resources)

def consume_resource(resources, name, quantity):
    """Consumes a quantity of a resource, ensuring it doesn't go below zero."""
    current_quantity = resources.get(name, 0)
    if current_quantity == 0:
        print(f"No {name} to consume. Current: 0.")
        return # No change, no save

    consumed = min(quantity, current_quantity)
    resources[name] = current_quantity - consumed
    print(f"Consumed {consumed} of {name}. Remaining: {resources[name]}. " \
          + (f"(Note: You only had {current_quantity})" if consumed < quantity else ""))
    save_resources(resources) # Only save if something was actually consumed

def list_resources(resources):
    """Lists all current resources and their quantities."""
    if not resources:
        print("No resources tracked yet. Start adding some!")
        return
    print("Current Resources:")
    for name, quantity in resources.items():
        print(f"  {name}: {quantity}")

def main():
    parser = argparse.ArgumentParser(description="Post-Apocalyptic Resource Tracker")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a resource or increase its quantity')
    add_parser.add_argument('name', type=str, help='Name of the resource')
    add_parser.add_argument('quantity', type=int, help='Quantity to add')

    # Consume command
    consume_parser = subparsers.add_parser('consume', help='Consume a resource or decrease its quantity')
    consume_parser.add_argument('name', type=str, help='Name of the resource')
    consume_parser.add_argument('quantity', type=int, help='Quantity to consume')

    # List command
    list_parser = subparsers.add_parser('list', help='List all current resources')

    args = parser.parse_args()

    resources = load_resources()

    if args.command == 'add':
        add_resource(resources, args.name, args.quantity)
    elif args.command == 'consume':
        consume_resource(resources, args.name, args.quantity)
    elif args.command == 'list':
        list_resources(resources)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
