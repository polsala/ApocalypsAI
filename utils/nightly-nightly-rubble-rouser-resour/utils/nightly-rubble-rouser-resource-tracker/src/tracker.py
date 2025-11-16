import argparse
import json
import os

class ResourceTracker:
    def __init__(self, data_file='resources.json'):
        self.data_file = data_file
        self.resources = self._load_resources()

    def _load_resources(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    # Handle empty or malformed JSON file gracefully
                    return {}
        return {}

    def _save_resources(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.resources, f, indent=2)

    def add_resource(self, name, quantity):
        quantity = int(quantity)
        if quantity <= 0:
            print(f"Quantity for '{name}' must be positive to add.")
            return
        self.resources[name] = self.resources.get(name, 0) + quantity
        self._save_resources()
        print(f"Added {quantity} of {name}. New total: {self.resources[name]}")

    def remove_resource(self, name, quantity):
        quantity = int(quantity)
        if quantity <= 0:
            print(f"Quantity for '{name}' must be positive to remove.")
            return
        if name not in self.resources:
            print(f"Resource '{name}' not found in inventory.")
            return
        
        self.resources[name] -= quantity
        if self.resources[name] <= 0:
            print(f"Removed {quantity} of {name}. Resource depleted and removed from inventory.")
            del self.resources[name]
        else:
            print(f"Removed {quantity} of {name}. New total: {self.resources[name]}")
        self._save_resources()

    def set_resource(self, name, quantity):
        quantity = int(quantity)
        if quantity < 0:
            print(f"Quantity for '{name}' cannot be negative.")
            return
        if quantity == 0:
            if name in self.resources:
                del self.resources[name]
                print(f"Set {name} to 0. Resource removed from inventory.")
            else:
                print(f"Resource '{name}' not found, nothing to set to 0.")
        else:
            self.resources[name] = quantity
            print(f"Set {name} to {quantity}.")
        self._save_resources()

    def list_resources(self):
        if not self.resources:
            print("Your inventory is currently empty. Time to scavenge!")
            return
        print("Current Resources:")
        for name, quantity in sorted(self.resources.items()):
            print(f"  {name}: {quantity}")

def main():
    parser = argparse.ArgumentParser(description="Track your scavenged resources.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add quantity to a resource')
    add_parser.add_argument('name', type=str, help='Name of the resource')
    add_parser.add_argument('quantity', type=int, help='Quantity to add')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove quantity from a resource')
    remove_parser.add_argument('name', type=str, help='Name of the resource')
    remove_parser.add_argument('quantity', type=int, help='Quantity to remove')

    # Set command
    set_parser = subparsers.add_parser('set', help='Set resource quantity')
    set_parser.add_argument('name', type=str, help='Name of the resource')
    set_parser.add_argument('quantity', type=int, help='Quantity to set')

    # List command
    list_parser = subparsers.add_parser('list', help='List all resources')

    args = parser.parse_args()

    tracker = ResourceTracker()

    if args.command == 'add':
        tracker.add_resource(args.name, args.quantity)
    elif args.command == 'remove':
        tracker.remove_resource(args.name, args.quantity)
    elif args.command == 'set':
        tracker.set_resource(args.name, args.quantity)
    elif args.command == 'list':
        tracker.list_resources()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
