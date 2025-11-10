import argparse
import json
import os

class ResourceTracker:
    def __init__(self, inventory_file='inventory.json'):
        self.inventory_file = inventory_file
        self.inventory = self._load()

    def _load(self):
        """Loads inventory from the JSON file."""
        if os.path.exists(self.inventory_file):
            try:
                with open(self.inventory_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Inventory file '{self.inventory_file}' is corrupted. Starting with empty inventory.")
                return {}
        return {}

    def _save(self):
        """Saves current inventory to the JSON file."""
        with open(self.inventory_file, 'w') as f:
            json.dump(self.inventory, f, indent=4)

    def add_resource(self, name: str, quantity: int):
        """Adds a new resource or increases the quantity of an existing one."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Resource name cannot be empty.")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")

        name = name.strip().lower() # Normalize name for internal storage
        self.inventory[name] = self.inventory.get(name, 0) + quantity
        self._save()
        print(f"Added {quantity} of '{name}'. Current total: {self.inventory[name]}")

    def update_quantity(self, name: str, quantity: int):
        """Sets the quantity of an existing resource to a specific value."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Resource name cannot be empty.")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")

        name = name.strip().lower()
        if name in self.inventory:
            self.inventory[name] = quantity
            self._save()
            print(f"Updated '{name}' to {quantity}.")
        else:
            print(f"Resource '{name}' not found. Use 'add' to create it.")

    def remove_resource(self, name: str):
        """Removes a resource from the inventory."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Resource name cannot be empty.")

        name = name.strip().lower()
        if name in self.inventory:
            del self.inventory[name]
            self._save()
            print(f"Removed '{name}' from inventory.")
        else:
            print(f"Resource '{name}' not found in inventory.")

    def get_inventory(self) -> dict:
        """Returns a copy of the current inventory."""
        return self.inventory.copy()

    def display_inventory(self):
        """Prints the current inventory in a formatted way."""
        if not self.inventory:
            print("Your inventory is empty. Time to scavenge!")
            return

        print("\n--- Current Inventory ---")
        # Sort items alphabetically for consistent display
        for name, quantity in sorted(self.inventory.items()):
            print(f"  - {name.title()}: {quantity}") # Capitalize for display
        print("-------------------------")

def main():
    parser = argparse.ArgumentParser(description="Apocalypse Resource Tracker: Manage your scavenged supplies.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new resource or increase quantity of existing.')
    add_parser.add_argument('--name', type=str, required=True, help='Name of the resource.')
    add_parser.add_argument('--quantity', type=int, required=True, help='Quantity to add.')

    # Update command
    update_parser = subparsers.add_parser('update', help='Set a new quantity for an existing resource.')
    update_parser.add_argument('--name', type=str, required=True, help='Name of the resource.')
    update_parser.add_argument('--quantity', type=int, required=True, help='New quantity for the resource.')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a resource from inventory.')
    remove_parser.add_argument('--name', type=str, required=True, help='Name of the resource to remove.')

    # List command
    list_parser = subparsers.add_parser('list', help='Display current inventory.')

    args = parser.parse_args()

    tracker = ResourceTracker()

    try:
        if args.command == 'add':
            tracker.add_resource(args.name, args.quantity)
        elif args.command == 'update':
            tracker.update_quantity(args.name, args.quantity)
        elif args.command == 'remove':
            tracker.remove_resource(args.name)
        elif args.command == 'list':
            tracker.display_inventory()
        else:
            parser.print_help()
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
