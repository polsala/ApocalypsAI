import argparse
import json
import os
from typing import Dict, Any

INVENTORY_FILE = "inventory.json"

def _load_inventory() -> Dict[str, Any]:
    """Loads the inventory from the JSON file."""
    if not os.path.exists(INVENTORY_FILE):
        return {}
    with open(INVENTORY_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {INVENTORY_FILE} is corrupted. Starting with an empty inventory.")
            return {}

def _save_inventory(inventory: Dict[str, Any]):
    """Saves the inventory to the JSON file."""
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f, indent=2)

def add_item(name: str, quantity: int, condition: str, location: str):
    """Adds a new item or updates an existing one's quantity."""
    inventory = _load_inventory()
    if name in inventory:
        print(f"Item '{name}' already exists. Updating quantity and details.")
        inventory[name]['quantity'] += quantity
        inventory[name]['condition'] = condition # Overwrite condition/location on add if exists
        inventory[name]['location'] = location
    else:
        inventory[name] = {
            "quantity": quantity,
            "condition": condition,
            "location": location
        }
    _save_inventory(inventory)
    print(f"Added/Updated '{name}': Quantity={inventory[name]['quantity']}, Condition='{condition}', Location='{location}'")

def remove_item(name: str):
    """Removes an item from the inventory."""
    inventory = _load_inventory()
    if name in inventory:
        del inventory[name]
        _save_inventory(inventory)
        print(f"Removed '{name}' from inventory.")
    else:
        print(f"Item '{name}' not found in inventory.")

def update_item(name: str, quantity: int = None, condition: str = None, location: str = None):
    """Updates the details of an existing item."""
    inventory = _load_inventory()
    if name not in inventory:
        print(f"Item '{name}' not found in inventory. Cannot update.")
        return

    updated = False
    if quantity is not None:
        inventory[name]['quantity'] = quantity
        updated = True
    if condition is not None:
        inventory[name]['condition'] = condition
        updated = True
    if location is not None:
        inventory[name]['location'] = location
        updated = True

    if updated:
        _save_inventory(inventory)
        print(f"Updated '{name}': {inventory[name]}")
    else:
        print(f"No updates specified for '{name}'.")

def list_items():
    """Lists all items in the inventory."""
    inventory = _load_inventory()
    if not inventory:
        print("Inventory is empty.")
        return

    print("\n--- Current Inventory ---")
    for name, details in inventory.items():
        print(f"  - {name}:")
        print(f"    Quantity: {details['quantity']}")
        print(f"    Condition: {details['condition']}")
        print(f"    Location: {details['location']}")
    print("-------------------------")

def check_status(low_stock_threshold: int = 5):
    """Provides a status overview of the inventory."""
    inventory = _load_inventory()
    if not inventory:
        print("Inventory is empty. Nothing to check.")
        return

    total_items = len(inventory)
    total_quantity = sum(item['quantity'] for item in inventory.values())
    low_stock_items = {name: details['quantity'] for name, details in inventory.items() if details['quantity'] <= low_stock_threshold}
    damaged_items = {name: details['condition'] for name, details in inventory.items() if details['condition'].lower() in ['damaged', 'broken', 'poor', 'used']}

    print("\n--- Inventory Status Report ---")
    print(f"Total unique items: {total_items}")
    print(f"Total quantity of all items: {total_quantity}")

    if low_stock_items:
        print(f"\n--- Low Stock Items (<= {low_stock_threshold}) ---")
        for name, qty in low_stock_items.items():
            print(f"  - {name}: {qty}")
    else:
        print("\nNo items are currently low on stock.")

    if damaged_items:
        print("\n--- Items in Poor/Used Condition ---")
        for name, condition in damaged_items.items():
            print(f"  - {name}: {condition}")
    else:
        print("\nAll items appear to be in good or new condition.")
    print("-------------------------------")


def main():
    parser = argparse.ArgumentParser(description="Gloom-Gazer Gear Inventory Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new item to the inventory.")
    add_parser.add_argument("--name", required=True, help="Name of the item.")
    add_parser.add_argument("--quantity", type=int, required=True, help="Quantity of the item.")
    add_parser.add_argument("--condition", required=True, help="Condition of the item (e.g., New, Good, Used, Damaged).")
    add_parser.add_argument("--location", required=True, help="Location where the item is stored.")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove an item from the inventory.")
    remove_parser.add_argument("--name", required=True, help="Name of the item to remove.")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing item's details.")
    update_parser.add_argument("--name", required=True, help="Name of the item to update.")
    update_parser.add_argument("--quantity", type=int, help="New quantity of the item.")
    update_parser.add_argument("--condition", help="New condition of the item.")
    update_parser.add_argument("--location", help="New location of the item.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all items in the inventory.")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get a status overview of the inventory.")
    status_parser.add_argument("--low-stock-threshold", type=int, default=5, help="Threshold for low stock warning.")

    args = parser.parse_args()

    if args.command == "add":
        add_item(args.name, args.quantity, args.condition, args.location)
    elif args.command == "remove":
        remove_item(args.name)
    elif args.command == "update":
        update_item(args.name, args.quantity, args.condition, args.location)
    elif args.command == "list":
        list_items()
    elif args.command == "status":
        check_status(args.low_stock_threshold)

if __name__ == "__main__":
    main()
