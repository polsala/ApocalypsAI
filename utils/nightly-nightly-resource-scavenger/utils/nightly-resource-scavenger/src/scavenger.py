#!/usr/bin/env python3

import argparse
import json
import os
from typing import Dict, Any

RESOURCE_FILE = os.path.join(os.path.dirname(__file__), 'resources.json')

def load_resources() -> Dict[str, int]:
    """Loads resources from the JSON file."""
    if not os.path.exists(RESOURCE_FILE):
        return {}
    try:
        with open(RESOURCE_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {RESOURCE_FILE} is corrupted. Starting with an empty inventory.")
        return {}
    except Exception as e:
        print(f"Error loading resources: {e}. Starting with an empty inventory.")
        return {}

def save_resources(resources: Dict[str, int]):
    """Saves resources to the JSON file."""
    try:
        with open(RESOURCE_FILE, 'w') as f:
            json.dump(resources, f, indent=4)
    except Exception as e:
        print(f"Error saving resources: {e}")

def add_resource(name: str, quantity: int):
    """Adds or updates a resource."""
    if quantity <= 0:
        print("Quantity must be positive to add resources.")
        return

    resources = load_resources()
    resources[name] = resources.get(name, 0) + quantity
    save_resources(resources)
    print(f"Scavenged {quantity} units of '{name}'. Inventory updated, survivor!")

def remove_resource(name: str, quantity: int):
    """Removes a quantity of a resource."""
    if quantity <= 0:
        print("Quantity must be positive to remove resources.")
        return

    resources = load_resources()
    if name not in resources:
        print(f"'{name}' not found in inventory. Can't remove what isn't there, survivor.")
        return

    resources[name] -= quantity
    if resources[name] <= 0:
        del resources[name]
        print(f"Consumed all remaining '{name}'. Item removed from inventory.")
    else:
        print(f"Consumed {quantity} units of '{name}'. Remaining: {resources[name]}. Inventory updated, survivor!")
    save_resources(resources)

def list_resources():
    """Lists all resources in the inventory."""
    resources = load_resources()
    if not resources:
        print("Your inventory is currently empty. Time to scavenge, survivor!")
        return

    print("\n--- Current Inventory ---")
    for name, quantity in sorted(resources.items()):
        print(f"{name}: {quantity}")
    print("-------------------------")
    print("Stay vigilant, survivor!")

def clear_resources():
    """Clears all resources from the inventory."""
    save_resources({})
    print("Inventory wiped clean. A fresh start, or a grave loss? Only time will tell.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Resource Scavenger: Track your post-apocalyptic inventory."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a resource to inventory.")
    add_parser.add_argument("name", type=str, help="Name of the resource.")
    add_parser.add_argument("quantity", type=int, help="Quantity to add.")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a resource from inventory.")
    remove_parser.add_argument("name", type=str, help="Name of the resource.")
    remove_parser.add_argument("quantity", type=int, help="Quantity to remove.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all resources in inventory.")

    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear all resources from inventory.")

    args = parser.parse_args()

    if args.command == "add":
        add_resource(args.name, args.quantity)
    elif args.command == "remove":
        remove_resource(args.name, args.quantity)
    elif args.command == "list":
        list_resources()
    elif args.command == "clear":
        clear_resources()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
