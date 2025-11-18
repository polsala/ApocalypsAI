import argparse
import json
import os
from typing import Dict, Any

INVENTORY_FILE = "resources.json"

def load_inventory(file_path: str) -> Dict[str, Any]:
    """Loads the inventory from a JSON file."""
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {os.path.basename(file_path)} is corrupted or empty. Starting with an empty inventory.")
        return {}
    except Exception as e:
        print(f"Error loading inventory from {os.path.basename(file_path)}: {e}")
        return {}

def save_inventory(file_path: str, inventory: Dict[str, Any]):
    """Saves the inventory to a JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(inventory, f, indent=4)
    except Exception as e:
        print(f"Error saving inventory to {os.path.basename(file_path)}: {e}")

def add_resource(inventory: Dict[str, Any], name: str, quantity: int, location: str):
    """Adds a new resource or updates an existing one."""
    if name in inventory:
        print(f"Resource '{name}' already exists. Updating quantity and location.")
    inventory[name] = {"quantity": quantity, "location": location}
    print(f"Added/Updated: {name} (Quantity: {quantity}, Location: {location})")

def update_resource(inventory: Dict[str, Any], name: str, quantity: int):
    """Updates the quantity of an existing resource."""
    if name not in inventory:
        print(f"Error: Resource '{name}' not found.")
        return
    inventory[name]["quantity"] = quantity
    print(f"Updated: {name} (New Quantity: {quantity})")

def remove_resource(inventory: Dict[str, Any], name: str):
    """Removes a resource from the inventory."""
    if name not in inventory:
        print(f"Error: Resource '{name}' not found.")
        return
    del inventory[name]
    print(f"Removed: {name}")

def list_resources(inventory: Dict[str, Any]):
    """Lists all resources in the inventory."""
    if not inventory:
        print("Your inventory is currently empty. Time to scavenge!")
        return

    print("--- Current Inventory ---")
    for name, details in inventory.items():
        print(f"Name: {name}, Quantity: {details['quantity']}, Location: {details['location']}")
    print("-------------------------")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Resource Scavenger: Track your post-apocalyptic finds."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new resource or update an existing one.")
    add_parser.add_argument("--name", required=True, help="Name of the resource.")
    add_parser.add_argument("--quantity", type=int, required=True, help="Quantity of the resource.")
    add_parser.add_argument("--location", required=True, help="Location where the resource is stored.")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update the quantity of an existing resource.")
    update_parser.add_argument("--name", required=True, help="Name of the resource to update.")
    update_parser.add_argument("--quantity", type=int, required=True, help="New quantity of the resource.")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a resource from the inventory.")
    remove_parser.add_argument("--name", required=True, help="Name of the resource to remove.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all resources in the inventory.")

    args = parser.parse_args()

    # Determine the path to the inventory file relative to the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    inventory_file_path = os.path.join(script_dir, INVENTORY_FILE)

    inventory = load_inventory(inventory_file_path)

    if args.command == "add":
        add_resource(inventory, args.name, args.quantity, args.location)
    elif args.command == "update":
        update_resource(inventory, args.name, args.quantity)
    elif args.command == "remove":
        remove_resource(inventory, args.name)
    elif args.command == "list":
        list_resources(inventory)
    else:
        parser.print_help()
        return # Exit without saving if no command was run or help was printed

    save_inventory(inventory_file_path, inventory)

if __name__ == "__main__":
    main()
