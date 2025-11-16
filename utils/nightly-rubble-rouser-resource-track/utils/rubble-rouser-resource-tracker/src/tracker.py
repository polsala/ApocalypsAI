import json
import os
import argparse
from typing import Dict, Any

DEFAULT_INVENTORY_FILE = "inventory.json"

class ResourceTracker:
    def __init__(self, inventory_file: str = DEFAULT_INVENTORY_FILE):
        self.inventory_file = inventory_file
        self.inventory: Dict[str, int] = self._load_inventory()

    def _load_inventory(self) -> Dict[str, int]:
        """Loads the inventory from the specified JSON file."""
        if os.path.exists(self.inventory_file):
            try:
                with open(self.inventory_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Inventory file '{self.inventory_file}' is corrupted. Starting with empty inventory.")
                return {}
        return {}

    def _save_inventory(self) -> None:
        """Saves the current inventory to the JSON file."""
        with open(self.inventory_file, 'w') as f:
            json.dump(self.inventory, f, indent=4)

    def add_resource(self, name: str, quantity: int) -> None:
        """Adds a new resource or updates its quantity by adding to existing."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.inventory[name] = self.inventory.get(name, 0) + quantity
        self._save_inventory()
        print(f"Added/Updated '{name}': {self.inventory[name]} units.")

    def update_resource(self, name: str, quantity: int) -> None:
        """Sets the quantity of an existing resource."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.inventory[name] = quantity
        self._save_inventory()
        print(f"Added/Updated '{name}': {self.inventory[name]} units.")

    def remove_resource(self, name: str) -> None:
        """Removes a resource from the inventory."""
        if name in self.inventory:
            del self.inventory[name]
            self._save_inventory()
            print(f"Removed '{name}' from inventory.")
        else:
            print(f"Resource '{name}' not found in inventory.")

    def list_resources(self) -> None:
        """Prints all resources and their quantities."""
        if not self.inventory:
            print("Inventory is empty. Time to scavenge!")
            return

        print("--- Current Inventory ---")
        for name, quantity in sorted(self.inventory.items()):
            print(f"{name}: {quantity}")
        print("-------------------------")

def main():
    parser = argparse.ArgumentParser(
        description="Rubble-Rouser Resource Tracker: Manage your scavenged inventory."
    )
    parser.add_argument(
        "--file",
        "-f",
        default=DEFAULT_INVENTORY_FILE,
        help=f"Specify the inventory file (default: {DEFAULT_INVENTORY_FILE})"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new resource or add to existing quantity.")
    add_parser.add_argument("name", type=str, help="Name of the resource.")
    add_parser.add_argument("quantity", type=int, help="Quantity to add.")

    # Update command
    update_parser = subparsers.add_parser("update", help="Set the quantity of an existing resource.")
    update_parser.add_argument("name", type=str, help="Name of the resource.")
    update_parser.add_argument("quantity", type=int, help="New quantity to set.")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a resource from the inventory.")
    remove_parser.add_argument("name", type=str, help="Name of the resource to remove.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all resources in the inventory.")

    args = parser.parse_args()

    tracker = ResourceTracker(args.file)

    if args.command == "add":
        try:
            tracker.add_resource(args.name, args.quantity)
        except ValueError as e:
            print(f"Error: {e}")
    elif args.command == "update":
        try:
            tracker.update_resource(args.name, args.quantity)
        except ValueError as e:
            print(f"Error: {e}")
    elif args.command == "remove":
        tracker.remove_resource(args.name)
    elif args.command == "list":
        tracker.list_resources()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
