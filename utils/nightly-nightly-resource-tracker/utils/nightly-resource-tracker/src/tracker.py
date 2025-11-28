import argparse
import json
import os
import sys

INVENTORY_FILE = "inventory.json"

def load_inventory():
    """Loads the inventory from the INVENTORY_FILE."""
    if not os.path.exists(INVENTORY_FILE):
        return {}
    try:
        with open(INVENTORY_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {INVENTORY_FILE} is corrupted or empty. Starting with an empty inventory.", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Error loading inventory: {e}", file=sys.stderr)
        return {}

def save_inventory(inventory):
    """Saves the current inventory to the INVENTORY_FILE."""
    try:
        with open(INVENTORY_FILE, 'w') as f:
            json.dump(inventory, f, indent=4)
    except Exception as e:
        print(f"Error saving inventory: {e}", file=sys.stderr)

def add_resource(inventory, item, quantity):
    """Adds or updates a resource in the inventory."""
    if not isinstance(quantity, int) or quantity <= 0:
        print("Error: Quantity must be a positive integer.", file=sys.stderr)
        return False
    inventory[item] = inventory.get(item, 0) + quantity
    print(f"Added {quantity} x {item}. Current total: {inventory[item]}")
    return True

def remove_resource(inventory, item, quantity):
    """Removes a resource from the inventory."""
    if not isinstance(quantity, int) or quantity <= 0:
        print("Error: Quantity must be a positive integer.", file=sys.stderr)
        return False
    if item not in inventory:
        print(f"Error: '{item}' not found in inventory.", file=sys.stderr)
        return False

    current_quantity = inventory[item]
    if quantity >= current_quantity:
        del inventory[item]
        print(f"Removed all {current_quantity} x {item}. Item no longer in inventory.")
    else:
        inventory[item] -= quantity
        print(f"Removed {quantity} x {item}. Remaining: {inventory[item]}")
    return True

def list_resources(inventory):
    """Lists all resources and their quantities in the inventory."""
    if not inventory:
        print("Inventory is empty.")
        return

    print("\n--- Current Inventory ---")
    for item, quantity in sorted(inventory.items()):
        print(f"- {item}: {quantity}")
    print("-------------------------")

def main():
    parser = argparse.ArgumentParser(description="Manage your post-apocalyptic resource inventory.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a resource to the inventory')
    add_parser.add_argument('--item', required=True, help='Name of the resource')
    add_parser.add_argument('--quantity', type=int, required=True, help='Quantity to add')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a resource from the inventory')
    remove_parser.add_argument('--item', required=True, help='Name of the resource')
    remove_parser.add_argument('--quantity', type=int, required=True, help='Quantity to remove')

    # List command
    list_parser = subparsers.add_parser('list', help='List all resources in the inventory')

    args = parser.parse_args()

    inventory = load_inventory()
    changed = False

    if args.command == 'add':
        changed = add_resource(inventory, args.item, args.quantity)
    elif args.command == 'remove':
        changed = remove_resource(inventory, args.item, args.quantity)
    elif args.command == 'list':
        list_resources(inventory)
    else:
        parser.print_help()

    if changed:
        save_inventory(inventory)

if __name__ == '__main__':
    main()
