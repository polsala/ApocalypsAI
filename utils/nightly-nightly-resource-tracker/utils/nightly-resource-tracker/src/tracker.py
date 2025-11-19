import argparse
import json
import os
from typing import List, Dict, Any

INVENTORY_FILE = "inventory.json"

def get_inventory_path() -> str:
    """Returns the absolute path to the inventory file."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), INVENTORY_FILE)

def load_inventory() -> List[Dict[str, Any]]:
    """Loads the inventory from the JSON file."""
    inventory_path = get_inventory_path()
    if not os.path.exists(inventory_path):
        return []
    try:
        with open(inventory_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {INVENTORY_FILE} is corrupted or empty. Starting with an empty inventory.")
        return []
    except Exception as e:
        print(f"Error loading inventory: {e}")
        return []

def save_inventory(inventory: List[Dict[str, Any]]) -> None:
    """Saves the inventory to the JSON file."""
    inventory_path = get_inventory_path()
    try:
        with open(inventory_path, 'w', encoding='utf-8') as f:
            json.dump(inventory, f, indent=4)
    except Exception as e:
        print(f"Error saving inventory: {e}")

def add_resource(name: str, quantity: int, location: str) -> None:
    """Adds a resource to the inventory or updates its quantity and location."""
    inventory = load_inventory()
    found = False
    for item in inventory:
        if item["name"].lower() == name.lower():
            item["quantity"] += quantity
            item["location"] = location # Update location if adding existing item
            found = True
            break
    if not found:
        inventory.append({"name": name, "quantity": quantity, "location": location})
    save_inventory(inventory)
    print(f"Added {quantity}x {name} at {location}.")

def remove_resource(name: str, quantity: int) -> None:
    """Removes a specified quantity of a resource from the inventory."""
    inventory = load_inventory()
    
    updated_inventory = []
    item_found = False
    final_quantity = 0
    
    for item in inventory:
        if item["name"].lower() == name.lower():
            item_found = True
            item["quantity"] -= quantity
            final_quantity = item["quantity"]
            if item["quantity"] > 0:
                updated_inventory.append(item)
        else:
            updated_inventory.append(item)
            
    if not item_found:
        print(f"Resource '{name}' not found in inventory.")
    elif final_quantity <= 0:
        print(f"Removed all {name} (quantity dropped to 0 or less).")
    else:
        print(f"Removed {quantity}x {name}. Remaining: {final_quantity}.")

    save_inventory(updated_inventory)


def list_resources() -> None:
    """Lists all resources in the inventory."""
    inventory = load_inventory()
    if not inventory:
        print("Inventory is empty. Time to start scavenging!")
        return

    print("\n--- Current Inventory ---")
    for item in inventory:
        print(f"- {item['name']} (x{item['quantity']}) at {item['location']}")
    print("-------------------------\n")

def search_resources(query: str) -> None:
    """Searches for resources by name or location."""
    inventory = load_inventory()
    results = [
        item for item in inventory
        if query.lower() in item["name"].lower() or query.lower() in item["location"].lower()
    ]

    if not results:
        print(f"No resources found matching '{query}'. Keep looking!")
        return

    print(f"\n--- Search Results for '{query}' ---")
    for item in results:
        print(f"- {item['name']} (x{item['quantity']}) at {item['location']}")
    print("----------------------------------\n")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Rubble-Rouser Resource Tracker: Manage your post-apocalyptic inventory."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new resource or update an existing one.")
    add_parser.add_argument("name", type=str, help="Name of the resource.")
    add_parser.add_argument("quantity", type=int, help="Quantity of the resource.")
    add_parser.add_argument("location", type=str, help="Location where the resource is stored.")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a quantity of an existing resource.")
    remove_parser.add_argument("name", type=str, help="Name of the resource to remove.")
    remove_parser.add_argument("quantity", type=int, help="Quantity to remove.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all resources in the inventory.")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for resources by name or location.")
    search_parser.add_argument("query", type=str, help="Search query.")

    args = parser.parse_args()

    if args.command == "add":
        add_resource(args.name, args.quantity, args.location)
    elif args.command == "remove":
        remove_resource(args.name, args.quantity)
    elif args.command == "list":
        list_resources()
    elif args.command == "search":
        search_resources(args.query)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
