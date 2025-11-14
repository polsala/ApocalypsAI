import json
import os
import sys
from collections import defaultdict

PROVISIONS_FILE = 'provisions.json'
INVENTORY_FILE = 'inventory.json'

def load_json(filepath):
    """Loads JSON data from a file."""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}. File might be malformed.", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Error loading {filepath}: {e}", file=sys.stderr)
        return {}

def save_json(filepath, data):
    """Saves data to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving {filepath}: {e}", file=sys.stderr)

def get_shopping_list(provisions, inventory):
    """Compares provisions with inventory and returns a shopping list."""
    shopping_list = {}
    for item, details in provisions.items():
        target = details.get('target', 0)
        unit = details.get('unit', 'units')
        current = inventory.get(item, 0)

        if current < target:
            needed = target - current
            shopping_list[item] = {'quantity': needed, 'unit': unit}
    return shopping_list

def update_inventory(item_name, quantity_change, inventory):
    """Updates the inventory for a given item by quantity_change."""
    if item_name not in inventory:
        if quantity_change < 0:
            print(f"Warning: Item '{item_name}' not found in inventory. Cannot consume.", file=sys.stderr)
            return False
        else:
            inventory[item_name] = 0 # Initialize if adding a new item

    new_quantity = inventory[item_name] + quantity_change
    if new_quantity < 0:
        print(f"Error: Not enough '{item_name}' in stock to consume {abs(quantity_change)}. Current: {inventory[item_name]}", file=sys.stderr)
        return False

    inventory[item_name] = new_quantity
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/planner.py <command> [args...]", file=sys.stderr)
        print("Commands: check, consume <item_name> <quantity>, add <item_name> <quantity>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    provisions = load_json(PROVISIONS_FILE)
    inventory = load_json(INVENTORY_FILE)

    if command == 'check':
        shopping_list = get_shopping_list(provisions, inventory)
        if shopping_list:
            print("\n--- Shopping List ---")
            for item, details in shopping_list.items():
                print(f"- {item}: {details['quantity']} {details['unit']}")
            print("---------------------")
        else:
            print("All provisions are stocked! You are ready for anything.")
    elif command == 'consume':
        if len(sys.argv) != 4:
            print("Usage: python src/planner.py consume <item_name> <quantity>", file=sys.stderr)
            sys.exit(1)
        item_name = sys.argv[2]
        try:
            quantity = int(sys.argv[3])
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
        except ValueError:
            print("Error: Quantity must be a positive integer.", file=sys.stderr)
            sys.exit(1)

        if update_inventory(item_name, -quantity, inventory):
            save_json(INVENTORY_FILE, inventory)
            print(f"Consumed {quantity} of '{item_name}'. Current stock: {inventory.get(item_name, 0)}")
    elif command == 'add':
        if len(sys.argv) != 4:
            print("Usage: python src/planner.py add <item_name> <quantity>", file=sys.stderr)
            sys.exit(1)
        item_name = sys.argv[2]
        try:
            quantity = int(sys.argv[3])
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
        except ValueError:
            print("Error: Quantity must be a positive integer.", file=sys.stderr)
            sys.exit(1)

        if update_inventory(item_name, quantity, inventory):
            save_json(INVENTORY_FILE, inventory)
            print(f"Added {quantity} of '{item_name}'. Current stock: {inventory.get(item_name, 0)}")
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
